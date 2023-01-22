from rest_framework import serializers
from .models import User 

class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "user", "password"]

        extra_kwargs = {
            "password":{"write_only": True}
        }