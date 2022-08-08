from drf_yasg import openapi


TOKEN_PARAM_CONFIG = openapi.Parameter(
    "token", in_=openapi.IN_QUERY,
    description="Verification token",
    type=openapi.TYPE_STRING
)


