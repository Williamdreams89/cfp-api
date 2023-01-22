from rest_framework import status, generics, views
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import *


class UserSignUpAPIView(generics.GenericAPIView):
    serializer_class = UserSignUpSerializer

    def post(self, request):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data
        serializer.save()
        user = User.objects.get(email=serializer.data["email"])
        refresh = RefreshToken.for_user(user)
        

        return Response({
            "message": "Successfully created",
            "tokens":{
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }
        }, status=status.HTTP_201_CREATED)