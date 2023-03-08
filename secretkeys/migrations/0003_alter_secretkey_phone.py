# Generated by Django 4.1.5 on 2023-03-06 07:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("secretkeys", "0002_rename_secret_key_secretkey_key_secretkey_active"),
    ]

    operations = [
        migrations.AlterField(
            model_name="secretkey",
            name="phone",
            field=models.CharField(
                max_length=11,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(
                        code=400,
                        message="Enter a valid phone number.",
                        regex="^010([0-9]{4})([0-9]{4})$",
                    )
                ],
            ),
        ),
    ]
