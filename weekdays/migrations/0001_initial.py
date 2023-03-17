# Generated by Django 4.1.5 on 2023-03-17 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Weekday",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("month", models.CharField(max_length=2)),
                ("days", models.CharField(max_length=250)),
                ("korean_holidays", models.CharField(max_length=250)),
            ],
        ),
    ]
