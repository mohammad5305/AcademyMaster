from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from core.models import AbstractToken, AbstractPermission, WeekDays
from teachers.models import Teacher
from .course_status import CourseStatus
from .course_level import CourseLevel


class Course(AbstractToken, AbstractPermission):
    title = models.CharField(max_length=250)
    description = models.TextField(max_length=300)
    location = models.CharField(max_length=150)

    instructor = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        related_name='courses'
    )

    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    start_date = models.DateField()
    end_date = models.DateField()
    schedule = models.JSONField(null=True, blank=True)
    days = ArrayField(
        models.IntegerField(choices=WeekDays.choices),
        size=7,
        null=True,
        blank=True,
    )

    session_count = models.PositiveSmallIntegerField(default=1)
    prerequisite = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    level = models.CharField(
        max_length=2,
        choices=CourseLevel.choices,
        default=CourseLevel.A1
    )

    status = models.CharField(
        max_length=2,
        choices=CourseStatus.choices,
        default=CourseStatus.ENROLLING
    )

    price = models.PositiveIntegerField(default=10000)

    @property
    def get_days_display(self):
        """Returns a list representation of the selected days of the week."""
        return [
            WeekDays.choices[int(day)][1] for day in self.days
            if self.days
        ]

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            self.days = list(self.days)
            # Check user has perm for assigning classes
            self._validate_creator(creator=self.assigned_by)
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.enrollments.exists():
            raise ValidationError(
                'Cannot delete a course with enrollments.'
            )

        if self.status != CourseStatus.ENROLLING:
            raise ValidationError(
                f'Cannot delete a course with status of {self.status}.'
            )
        return super().delete(*args, **kwargs)
