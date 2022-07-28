from django.contrib.auth import get_user_model
from rest_framework import serializers
from .services import SignUpService

User = get_user_model()

error_messages = {
    'not_active': 'Your account is not active. Please contact Your administrator',
    'wrong_credentials': 'Entered email or password is incorrect',
    'already_registered': "User is already registered with this e-mail address",
    'password_not_match': "The two password fields didn't match",
}


class SignUpSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100, required=True)
    last_name = serializers.CharField(max_length=100, required=True)
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)

    def validate_password1(self, password):
        return password

    def validate_email(self, email):
        status, msg = SignUpService.validate_email(email)
        if not status:
            raise serializers.ValidationError(msg)
        if SignUpService.get_user_or_none(email) is not None:
            raise serializers.ValidationError(error_messages["already_registered"])
        return email

    def validate(self, data):
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError(error_messages["password_not_match"])
        return data

    def save(self):
        self.validated_data["password"] = self.validated_data.pop("password1")
        del self.validated_data["password2"]
        User.object.create(**self.validated_data)





