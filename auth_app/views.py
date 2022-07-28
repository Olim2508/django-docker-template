from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from . import serializers


class SignUpView(CreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = serializers.SignUpSerializer
