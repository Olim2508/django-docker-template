import re
from typing import Tuple, Union, TYPE_CHECKING
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework.reverse import reverse_lazy
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK
from rest_framework_simplejwt.exceptions import TokenError
from src.celery import app

if TYPE_CHECKING:
    from rest_framework.request import Request


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


class CeleryService:

    @staticmethod
    def send_email_confirm(user: User, token: str, request: "Request") -> None:
        path = "auth_app:sign_up_verify"
        url = CeleryService._get_confirmation_url(path, token, request)
        kwargs = {
            'to_email': user.email,
            'content': {
                'user': user.get_full_name(),
                'activate_url': url,
            }
        }
        app.send_task('auth_app.tasks.send_verification_email', kwargs=kwargs)

    @staticmethod
    def _get_confirmation_url(path: str, token: str, request: "Request") -> str:
        url = reverse_lazy(path)
        return "http://localhost:8010" + str(url) + f"?token={token}"


def send_email(subject, template, content, to_email):
    html_content = template.render(content)
    send_mail(
        subject=subject,
        message='',
        from_email=None,
        recipient_list=[to_email] if isinstance(to_email, str) else to_email,
        html_message=html_content
    )