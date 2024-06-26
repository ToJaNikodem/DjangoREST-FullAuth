import re
from .models import CustomUser
from .tokens import account_activation_token
from .messages import DEFAULT_ERROR_MESSAGES
from .validators import password_validator, email_validator
from rest_framework import serializers
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class PasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        required=True, error_messages=DEFAULT_ERROR_MESSAGES)
    reset_token = serializers.CharField(
        required=True, error_messages=DEFAULT_ERROR_MESSAGES)

    def validate_reset_token(self, value):
        if not default_token_generator.check_token(self.context['user'], self.context['reset_token']):
            raise serializers.ValidationError('invalid')
        return value

    def validate_new_password(self, value):
        return password_validator(value)


class EmailVerificationSerializer(serializers.Serializer):
    verification_token = serializers.CharField(
        required=True, error_messages=DEFAULT_ERROR_MESSAGES)

    def validate_verification_token(self, value):
        if not account_activation_token.check_token(self.context['user'], self.context['verification_token']):
            raise serializers.ValidationError('invalid')
        return value


class NicknameChangeSerializer(serializers.Serializer):
    new_nickname = serializers.CharField(
        required=True, error_messages=DEFAULT_ERROR_MESSAGES)

    def validate_new_nickname(self, value):
        if not re.match(r'^[a-z0-9](?:[a-z0-9]+[.\-_]?)+[a-z0-9]$', value):
            raise serializers.ValidationError('invalid')

        if len(value) < 4:
            raise serializers.ValidationError('too_short')

        if len(value) > 40:
            raise serializers.ValidationError('too_long')
        return value


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        required=True, error_messages=DEFAULT_ERROR_MESSAGES)
    new_password = serializers.CharField(
        required=True, error_messages=DEFAULT_ERROR_MESSAGES)

    def validate_old_password(self, value):
        user = self.context['user']
        if not user.check_password(value):
            raise serializers.ValidationError('invalid')
        return value

    def validate_new_password(self, value):
        return password_validator(value)


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        error_messages=DEFAULT_ERROR_MESSAGES
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value):
        return password_validator(value)

    def validate_email(self, value):
        return email_validator(value)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['nickname'] = user.nickname
        token['is_email_verified'] = user.is_email_verified

        return token
