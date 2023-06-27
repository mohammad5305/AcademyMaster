from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from core.models import AbstractToken, AbstractPermission, WeekDays
from teachers.models import Teacher


class Course(AbstractToken, AbstractPermission):
    title = models.CharField(max_length=250)
    description = models.TextField(max_length=300)

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
    price = models.PositiveIntegerField(default=10000)

    status = models.CharField(
        max_length=2,
        choices=CourseStatus.choices,
        default=CourseStatus.ENROLLING
    )

    instructor = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True
    )
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return self.title
