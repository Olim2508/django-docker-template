from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

app_name = 'main'

urlpatterns = [

]

urlpatterns += router.urls
