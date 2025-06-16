
from rest_framework import serializers
from .models import User
from django.core.validators import validate_email 
from django.core.exceptions import ValidationError as DjangoValidationError
import re

class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    age = serializers.IntegerField(required=True)
    phone_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = User
        fields = '__all__'

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Name must be a non-empty string.")
        return value

    def validate_age(self, value):
        if not (0 <= value <= 120):
            raise serializers.ValidationError("Age must be between 0 and 120.")
        return value

    def validate_email(self, value):
        try:
            validate_email(value)
        except DjangoValidationError:
            raise serializers.ValidationError("Must be a valid email address.")

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email already exists.")
        return value

    def validate_phone_number(self, value):
            if value: 
                value = value.strip()
                if not re.fullmatch(r'\+?\d{10,15}', value):
                    raise serializers.ValidationError("Enter a valid phone number with 10 to 15 digits.")
            return value