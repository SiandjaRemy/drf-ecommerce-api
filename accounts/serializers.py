from rest_framework import serializers
from rest_framework.validators import ValidationError
from .models import User


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(default="")
    username = serializers.CharField(max_length=100, default="")
    password = serializers.CharField(min_length=4, default="", write_only=True)
    
    class Meta:
        model = User
        fields = ["email", "username", "password"]
    
    def validate(self, attrs):
        email_exists = User.objects.filter(email=attrs["email"]).exists()

        if email_exists:
            raise ValidationError("Email is already used")

        return super().validate(attrs)
    
    def create(self, validated_data):
        password = validated_data.pop("password")

        user=super().create(validated_data)

        user.set_password(password)

        user.save()

        return user


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(default="")
    password = serializers.CharField(min_length=4, default="", write_only=True)
    class Meta:
        model = User
        fields = ["email", "password"]
