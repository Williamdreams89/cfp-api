from rest_framework import serializers
from .models import User 

class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "user_type", "password"]

        extra_kwargs = {
            "password":{"write_only": True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user 

class RequestResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        return super().validate(attrs)
    

class ResetMyPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(help_text="Enter your new password here...")

    def validate(self, attrs):
        return super().validate(attrs)
    