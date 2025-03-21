# Generated by Django 4.2.1 on 2023-07-09 10:01

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('teachers', '0002_alter_teacher_contact_links'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='token',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
