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
}