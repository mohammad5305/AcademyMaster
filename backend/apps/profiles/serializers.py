from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ValidationError as ModelValidationError
from profiles.models import Profile
from core.serializers import UserRelationSerializer


class ProfileUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        source='user.first_name',
        required=False
    )
    last_name = serializers.CharField(
        source='user.last_name',
        required=False
    )

    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'avatar',
            'birth_date',
            'address',
            'passport_id',
            'phone_number',
        ]

    def update(self, instance, validated_data):
        try:
            user_data = validated_data.pop('user', {})

            if user_data.get('first_name') or user_data.get('last_name'):
                instance.user.first_name = user_data.get(
                    'first_name', instance.user.first_name
                )
                instance.user.last_name = user_data.get(
                    'last_name', instance.user.last_name
                )
                instance.user.save()

            return super().update(instance, validated_data)

        except ModelValidationError as message:
            raise ValidationError(
                detail=str(*message)
            )


class ProfileRetrieveSerializer(serializers.ModelSerializer):
    user = UserRelationSerializer()

    class Meta:
        model = Profile
        fields = [
            'user',
            'avatar',
            'birth_date',
            'address',
            'passport_id',
            'phone_number',
            'age',
        ]
