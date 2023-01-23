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
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_bytes, force_str, DjangoUnicodeDecodeError




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
            payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms="HS256")
            user = User.objects.get(id = payload["user_id"])
            if not user.is_verified:
                user.is_verified = True
                user.save()
                return Response("User has been successfully verified !!", status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response("Expired token !!", status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response("Invalid token !!", status=status.HTTP_400_BAD_REQUEST)

    
class RequestResetPasswordAPIView(generics.GenericAPIView):
    serializer_class = RequestResetPasswordSerializer
    def post(self, request):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.validated_data
        if User.objects.filter(email = serializer.data["email"]).exists():
            user = User.objects.get(email = serializer.data["email"])
            try:
                token = PasswordResetTokenGenerator().make_token(user)
                uuidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            except DjangoUnicodeDecodeError as e:
                return Response("Invalid token !!!", status=status.HTTP_400_BAD_REQUEST)
            current_site = get_current_site(request).domain
            rel_url = reverse("reset-password", kwargs={"uuidb64": uuidb64,"token": token})
            abs_url = "{}{}".format(current_site, rel_url,)
            email_subject = "Reset Your Password"
            email_body = "Hi {}, \nUse the link below to reset your password:\n{}".format(user.username, abs_url)
            email_to = user.email

            data = {"email_subject":email_subject, "email_body": email_body, "email_to": email_to}
            Util.send_email(data)
            return Response(f"Reset Password link sent to {user.email}")
        else:
            user= User.objects.get(email=serializer.data["email"])     
            return Response(f"{user.email} is associated with no account!!", status=status.HTTP_400_BAD_REQUEST)


class ResetMyPasswordAPIView(generics.GenericAPIView):
    serializer_class = ResetMyPasswordSerializer
    def post(self, request, uuidb64, token):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        serializer.validated_data
        try:
            id = force_str(urlsafe_base64_decode(uuidb64))
            user = User.objects.get(id = id)
            
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response("Invalid token", status=status.HTTP_400_BAD_REQUEST)
            else:
                user.set_password(serializer.data["new_password"])
                user.save()
                return Response("Password Reset Successful !!")
        except DjangoUnicodeDecodeError as identifier:
            return Response("Token had been utilized !!!", status=status.HTTP_400_BAD_REQUEST)

        