import os
from flask import Flask, request, redirect, session, render_template, abort, flash, url_for
from flask_login import current_user, LoginManager, login_user, logout_user
import secrets
import requests
from urllib.parse import urlencode
from model import db, User

OAUTH2_PROVIDERS = {
    # GitHub OAuth 2.0 documentation:
    # https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authorizing-oauth-apps
    'github': {
        'client_id': os.environ.get('GITHUB_CLIENT_ID'),
        'client_secret': os.environ.get('GITHUB_CLIENT_SECRET'),
        'authorize_url': 'https://github.com/login/oauth/authorize',
        'token_url': 'https://github.com/login/oauth/access_token',
        'userinfo': {
            'url': 'https://api.github.com/user',
            # 'email': 
            # NOTE: to get both email and username, we need two calls
            # See: https://stackoverflow.com/questions/35373995/github-user-email-is-null-despite-useremail-scope
            'displayName': lambda json: json['name'],
            'id': lambda json: json['login']
        },
        'scopes': ['user:email'],
    },

    # Google OAuth 2.0 documentation:
    # https://developers.google.com/identity/protocols/oauth2/web-server#httprest
    'google': {
        'client_id': os.environ.get('GOOGLE_CLIENT_ID'),
        'client_secret': os.environ.get('GOOGLE_CLIENT_SECRET'),
        'authorize_url': 'https://accounts.google.com/o/oauth2/auth',
        'token_url': 'https://accounts.google.com/o/oauth2/token',
        'userinfo': {
            'url': 'https://www.googleapis.com/oauth2/v3/userinfo',
			'id': lambda json: json['sub'],
			'displayName': lambda json: json['name']
            #'email': lambda json: json['email'], -> needs scope: https://www.googleapis.com/auth/userinfo.email
        },
        'scopes': ['https://www.googleapis.com/auth/userinfo.profile'],
    },
}

def add_authentication(app):
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        user = db.session.get(User, int(id))
        return user
    
    @app.route("/privacy")
    def privacy():
        return render_template("privacy.html", CONTACT_EMAIL = app.config['CONTACT_EMAIL'])


    @app.route('/logout')
    def logout():
        logout_user()
        flash('You have been logged out.')
        return redirect(url_for('index'))

    def create_callback_url(provider):
        # Note that app.config['PREFERRED_URL_SCHEME'] must be applied explicitly in url_for: https://stackoverflow.com/a/43288737/3306
        return url_for('oauth2_callback', provider=provider,
                                    _scheme=app.config['PREFERRED_URL_SCHEME'],
                                    _external=True)
    
    @app.route('/authorize/<provider>')
    def oauth2_authorize(provider):
        if not current_user.is_anonymous:
            return redirect(url_for('index'))

        provider_data = OAUTH2_PROVIDERS.get(provider)
        if provider_data is None:
            abort(404)

        # generate a random string for the state parameter
        session['oauth2_state'] = secrets.token_urlsafe(16)

        # create a query string with all the OAuth2 parameters
        qs = urlencode({
            'client_id': provider_data['client_id'],
            'redirect_uri': create_callback_url(provider),
            'response_type': 'code',
            'scope': ' '.join(provider_data['scopes']),
            'state': session['oauth2_state'],
        })

        # redirect the user to the OAuth2 provider authorization URL
        return redirect(provider_data['authorize_url'] + '?' + qs)

    @app.route('/callback/<provider>')
    def oauth2_callback(provider):
        if not current_user.is_anonymous:
            return redirect(url_for('index'))

        provider_data = OAUTH2_PROVIDERS.get(provider)
        if provider_data is None:
            abort(404)

        # if there was an authentication error, flash the error messages and exit
        if 'error' in request.args:
            for k, v in request.args.items():
                if k.startswith('error'):
                    flash(f'{k}: {v}')
            return redirect(url_for('index'))

        # make sure that the state parameter matches the one we created in the
        # authorization request
        if request.args['state'] != session.get('oauth2_state'):
            abort(401)

        # make sure that the authorization code is present
        if 'code' not in request.args:
            abort(401)

        # exchange the authorization code for an access token
        response = requests.post(provider_data['token_url'], data={
            'client_id': provider_data['client_id'],
            'client_secret': provider_data['client_secret'],
            'code': request.args['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': create_callback_url(provider),
        }, headers={'Accept': 'application/json'})
        if response.status_code != 200:
            abort(401)
        oauth2_token = response.json().get('access_token')
        if not oauth2_token:
            abort(401)

        # use the access token to get the user's email address
        response = requests.get(provider_data['userinfo']['url'], headers={
            'Authorization': 'Bearer ' + oauth2_token,
            'Accept': 'application/json',
        })
        if response.status_code != 200:
            abort(401)

        name = provider_data['userinfo']['displayName'](response.json())
        external_id = provider + ':' + provider_data['userinfo']['id'](response.json())

        # find or create the user in the database
        user = db.session.scalar(db.select(User).where(User.external_id == external_id))
        if user is None:
            user = User(external_id = external_id, username=name)
            db.session.add(user)
            db.session.commit()

        # log the user in
        login_user(user)
        return redirect(url_for('index'))

    # This ensures that we reload after login
    @app.after_request
    def add_header(response):
        response.vary = "Cookie"
        return response
