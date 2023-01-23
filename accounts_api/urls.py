from django.urls import path
from .api import *

urlpatterns = [
    path("user/signup/", UserSignUpAPIView.as_view(), name="sign-up"),
    path("verify-email/", VerifyEmail.as_view(), name="verify-email"),
    path("request-password-reset/", RequestResetPasswordAPIView.as_view(), name="request-password-reset"),
    path("reset-my-password/<uuidb64>/<token>/", ResetMyPasswordAPIView.as_view(), name="reset-password"),
]