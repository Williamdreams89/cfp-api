from rest_framework import status, generics, views
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import *
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings


class UserSignUpAPIView(generics.GenericAPIView):
    serializer_class = UserSignUpSerializer

    def post(self, request):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data
        serializer.save()
        user = User.objects.get(email=serializer.data["email"])
        refresh = RefreshToken.for_user(user)
        current_site = get_current_site(request).domain
        rel_url = reverse("verify-email")
        abs_url = "{}{}?token={}".format(current_site, rel_url, str(refresh.access_token))
        email_subject = "Verify Your Email"
        email_body = "Hi {}, \nUse the link below to sign-up to Citizen Feedback Platform:\n{}".format(user.username, abs_url)
        email_to = user.email
        data = {"email_subject":email_subject, "email_body": email_body, "email_to": email_to}
        Util.send_email(data)
        

        return Response({
            "message": "Successfully created",
            "tokens":{
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }
        }, status=status.HTTP_201_CREATED)

class VerifyEmail(views.APIView):
    def get(self, request):
        token = request.GET.get("token")
        try:
            payload = jwt.decode(jwt=token, key=settings.SECRET_kEY, algorithms="HS256")
            user = User.objects.get(id = payload["user_id"])
            if not user.is_verified:
                user.is_verified = True
                user.save()
                return Response("User has been successfully verified !!", status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response("Expired token !!", status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response("Invalid token !!", status=status.HTTP_400_BAD_REQUEST)