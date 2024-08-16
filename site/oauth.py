import os

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