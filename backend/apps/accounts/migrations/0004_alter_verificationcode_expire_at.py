# Generated by Django 4.2.1 on 2023-06-07 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_verificationcode_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificationcode',
            name='expire_at',
            field=models.DateTimeField(),
        ),
    ]
