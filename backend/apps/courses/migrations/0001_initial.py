# Generated by Django 4.2.1 on 2023-06-27 13:22

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('teachers', '0002_alter_teacher_contact_links'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=32, unique=True)),
                ('title', models.CharField(max_length=250)),
                ('description', models.TextField(max_length=300)),
                ('location', models.CharField(max_length=150)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('schedule', models.JSONField(blank=True, null=True)),
                ('days', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(choices=[('0', 'Saturday'), ('1', 'Sunday'), ('2', 'Monday'), ("(3, 'Tuesday')", 'Tuesday'), ('4', 'Wednesday'), ('5', 'Thursday'), ('6', 'Friday')]), blank=True, null=True, size=7)),
                ('session_count', models.PositiveSmallIntegerField(default=1)),
                ('level', models.CharField(choices=[('A1', 'Beginner'), ('A2', 'Elementary'), ('B1', 'Pre-Intermediate'), ('B2', 'Intermediate'), ('C1', 'Upper-Intermediate'), ('C2', 'Advance')], default='A1', max_length=2)),
                ('status', models.CharField(choices=[('EN', 'Enrolling'), ('IP', 'In Progress'), ('CO', 'Completed')], default='EN', max_length=2)),
                ('price', models.PositiveIntegerField(default=10000)),
                ('assigned_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('instructor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='teachers.teacher')),
                ('prerequisite', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='courses.course')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
