import re
from typing import Tuple, Union
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK
from rest_framework_simplejwt.exceptions import TokenError

User = get_user_model()


class SignUpService:

    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        re_email = r'^\w+([A-Za-z0-9])([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,30})+$'
        if not re.search(re_email, email):
            return False, "Entered email address is not valid"
        return True, ''

    @staticmethod
    def get_user_or_none(email: str) -> Union[User, None]:
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None

    @staticmethod
    def full_logout(request):
        response = Response({"detail": "Successfully logged out."}, status=HTTP_200_OK)
        if cookie_name := getattr(settings, 'JWT_AUTH_COOKIE', None):
            response.delete_cookie(cookie_name)
        refresh_cookie_name = getattr(settings, 'JWT_AUTH_REFRESH_COOKIE', None)
        refresh_token = request.COOKIES.get(refresh_cookie_name)
        if refresh_cookie_name:
            response.delete_cookie(refresh_cookie_name)
        if 'rest_framework_simplejwt.token_blacklist' in settings.INSTALLED_APPS:
            # add refresh token to blacklist
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except KeyError:
                response.data = {"detail": "Refresh token was not included in request data."}
                response.status_code = HTTP_401_UNAUTHORIZED
            except (TokenError, AttributeError, TypeError) as error:
                if hasattr(error, 'args'):
                    if 'Token is blacklisted' in error.args or 'Token is invalid or expired' in error.args:
                        response.data = {"detail": error.args[0]}
                        response.status_code = HTTP_401_UNAUTHORIZED
                    else:
                        response.data = {"detail": "An error has occurred."}
                        response.status_code = HTTP_500_INTERNAL_SERVER_ERROR

                else:
                    response.data = {"detail": "An error has occurred."}
                    response.status_code = HTTP_500_INTERNAL_SERVER_ERROR

        else:
            message = "Neither cookies or blacklist are enabled, so the token has not been deleted server side. " \
                      "Please make sure the token is deleted client side."

            response.data = {"detail": message}
            response.status_code = HTTP_200_OK
        return response



