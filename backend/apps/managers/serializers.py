from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from managers.models import Manager


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['codename']


class ManagerCreateSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='token',
        queryset=get_user_model().objects.all()
    )
    permissions = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False
    )

    token = serializers.CharField(read_only=True)

    class Meta:
        model = Manager
        fields = ['user', 'permissions', 'token']

    def validate_user(self, value):
        '''Checks if the user is not already a manager or an admin.'''
        if value.is_admin():
            raise ValidationError('Admins cannot become managers.')

        if value.is_manager():
            raise ValidationError('Managers cannot become managers twice.')

        return value

    def create(self, validated_data):
        manager = Manager.objects.create_with_permissions(
            user=validated_data['user'],
            promoted_by=self.context['request'].user,
            codenames=validated_data.get('permissions', None),
        )

        return manager


class ManagerUpdateSerializer(serializers.ModelSerializer):
    permissions = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Manager
        fields = ['permissions']

    def update(self, instance, validated_data):
        Manager.objects.update_permission(
                user=instance.user,
                permissions=[],
                codenames=validated_data.get('permissions', None)
        )
        return super().update(instance, validated_data)


class ManagerRetrieveSerializer(serializers.ModelSerializer):
    # list of manager's permissions
    permissions = serializers.SerializerMethodField(
        method_name='get_permissions'
    )

    class Meta:
        model = Manager
        fields = [
            'user',
            'promoted_by',
            'promotion_date',
            'permissions'
        ]

    def get_permissions(self, value):
        permissions = Permission.objects.filter(
            user=value.user,
        )

        serializer = PermissionSerializer(permissions, many=True)
        return serializer.data


class ManagerListSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Manager
        fields = [
            'user',
            'token'
        ]
