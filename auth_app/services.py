import re
from typing import Tuple, Union

from django.contrib.auth import get_user_model

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



