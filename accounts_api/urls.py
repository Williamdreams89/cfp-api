from django.urls import path
from .api import *

urlpatterns = [
    path("user/signup/", UserSignUpAPIView.as_view(), name="sign-up")
]