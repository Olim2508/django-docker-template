import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializers
from dj_rest_auth import views as auth_views
from dj_rest_auth.registration.views import VerifyEmailView as _VerifyEmailView
from drf_yasg.utils import swagger_auto_schema
from .schemas import TOKEN_PARAM_CONFIG
from .services import SignUpService, CeleryService

User = get_user_model()


class SignUpView(CreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = serializers.SignUpSerializer


class LogInView(auth_views.LoginView):
    serializer_class = serializers.LogInSerializer


class LogoutView(auth_views.LogoutView):
    allowed_methods = ('POST', 'OPTIONS')

    def logout(self, request):
        response = SignUpService.full_logout(request)
        return response


class VerifyEmailView(APIView):

    @swagger_auto_schema(manual_parameters=[TOKEN_PARAM_CONFIG])
    def get(self, request):
        token = request.GET.get("token")
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload["user_id"])
            user.is_active = True
            user.save()
            return Response({"email": "Successfully verified"}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({"error": "Activation expired"}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
