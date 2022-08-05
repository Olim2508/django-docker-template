from datetime import timedelta


REST_USE_JWT = True
REST_AUTH_TOKEN_MODEL = None
JWT_AUTH_REFRESH_COOKIE = 'refresh'
JWT_AUTH_COOKIE = 'jwt-auth'


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(minutes=15),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',
}
