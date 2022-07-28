from django.urls import path

from . import views

app_name = 'auth_app'

urlpatterns = [
    path('sign-up/', views.SignUpView.as_view(), name='sign-up'),
    path('sign-in/', views.LogInView.as_view(), name='sign-in'),
    path('log-out/', views.LogoutView.as_view(), name='log-out'),
]
