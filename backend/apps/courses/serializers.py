from rest_framework import serializers
from courses.models import Course, CourseStatus
from teachers.models import Teacher
from core.models import WeekDays
from core.serializers import (
    InstructorRelationSerializer,
    CourseRelationSerializer,
    UserProfileRelationSerializer
)


class BaseCourseCreateSerializer(serializers.ModelSerializer):
    prerequisite = serializers.SlugRelatedField(
        slug_field='token',
        queryset=Course.objects.only('token'),
        required=False,
        allow_null=True
    )

    instructor = serializers.SlugRelatedField(
        slug_field='token',
        queryset=Teacher.objects.only('token')
    )
    days = serializers.MultipleChoiceField(
        choices=WeekDays.choices
    )


class CourseCreateSerializer(BaseCourseCreateSerializer):

    class Meta:
        model = Course
        fields = [
            'title',
            'description',
            'location',
            'instructor',
            'assigned_by',
            'start_date',
            'end_date',
            'schedule',
            'days',
            'session_count',
            'prerequisite',
            'get_level_display',
            'get_status_display',
            'price',
            'token'
        ]
        read_only_fields = ('assigned_by', 'token')

    def create(self, validated_data):
        # Set request.user as course assigner
        validated_data['assigned_by'] = self.context['request'].user
        try:
            return super().create(validated_data)
        except Exception as e:
            raise ValueError(str(e))


class CourseRetrieveSerializer(serializers.ModelSerializer):
    instructor = InstructorRelationSerializer()
    assigned_by = UserProfileRelationSerializer()
    prerequisite = CourseRelationSerializer()

    class Meta:
        model = Course
        fields = [
            'title',
            'description',
            'location',
            'instructor',
            'assigned_by',
            'start_date',
            'end_date',
            'schedule',
            'get_days_display',
            'session_count',
            'prerequisite',
            'get_level_display',
            'get_status_display',
            'price'
        ]


class CourseUpdateSerializer(BaseCourseCreateSerializer):
    class Meta:
        model = Course
        fields = [
            'title',
            'description',
            'location',
            'instructor',
            'start_date',
            'end_date',
            'schedule',
            'days',
            'session_count',
            'prerequisite',
            'get_level_display',
            'get_status_display',
            'price'
        ]

    def update(self, instance, validated_data):
        if instance.status != CourseStatus.ENROLLING:
            raise serializers.ValidationError(
                'You cannot change status to ENROLLING'
            )
        return super().update(instance, validated_data)


class CourseListSerializer(serializers.ModelSerializer):
    instructor = InstructorRelationSerializer()

    class Meta:
        model = Course
        fields = [
            'title',
            'location',
            'start_date',
            'end_date',
            'instructor',
            'get_days_display',
            'session_count',
            'get_level_display',
            'get_status_display',
            'token'
        ]
