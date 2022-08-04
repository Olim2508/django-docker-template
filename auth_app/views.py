from django.shortcuts import render
from django.contrib.auth import logout as django_logout, get_user_model
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView, RetrieveAPIView, GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from . import serializers
from dj_rest_auth import views as auth_views

from .services import SignUpService
User = get_user_model()

class SignUpView(CreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = serializers.SignUpSerializer


class LogInView(auth_views.LoginView):
    serializer_class = serializers.LogInSerializer


class LogoutView(auth_views.LogoutView):
    allowed_methods = ('POST', 'OPTIONS')

    # def session_logout(self):
    #     django_logout(self.request)

    def logout(self, request):
        response = SignUpService.full_logout(request)
        return response
