from rest_framework import serializers
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from accounts.exceptions.serializers import (
    UserAlreadyExistsException,
    PendingVerificationException,
    AlreadyVerifiedException,
    DuplicationCodeException,
)

from accounts.exceptions.models import (
    DuplicationCodeException as ModelDuplicationCodeException,
    ActiveUserCodeException
)
from accounts.models import Account, VerificationCode


class AccountRegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True
    )

    class Meta:
        model = Account
        fields = ["email", "first_name", "last_name", "password"]

    def validate_email(self, value):
        # Check if email exists
        email = value
        account = Account.objects.filter(email=email).first()

        if account:
            # Raise appropriate exception
            if account.is_active:
                raise UserAlreadyExistsException()

            # If user exists and not active
            raise PendingVerificationException()

        return value

    def create(self, validated_data):
        return Account.objects.create_user(**validated_data)


class AccountVerifySerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = VerificationCode
        fields = ['email', 'code']

    def verify_code(self, email: str, code: int):
        user = get_object_or_404(Account, email=email)

        if user.is_active:
            raise AlreadyVerifiedException()

        verify_code, message = VerificationCode.objects.verify(
            user=user, code=code
        )

        if not verify_code:
            raise ValidationError(str(message))

        self._activate_user(user)
        return user

    def _activate_user(self, user):
        user.is_active = True
        user.save()
        return user


class ResendCodeSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='token',
        queryset=Account.objects.filter(is_active=False)
    )

    class Meta:
        model = VerificationCode
        fields = ['user']

    def create(self, validated_data):
        try:
            return super().create(validated_data)

        except ModelDuplicationCodeException:
            raise DuplicationCodeException()

        except ActiveUserCodeException:
            raise AlreadyVerifiedException()
