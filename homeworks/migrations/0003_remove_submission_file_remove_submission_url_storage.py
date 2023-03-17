# Generated by Django 4.1.5 on 2023-03-17 07:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("homeworks", "0002_submission"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="submission",
            name="file",
        ),
        migrations.RemoveField(
            model_name="submission",
            name="url",
        ),
        migrations.CreateModel(
            name="Storage",
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
                ("url", models.CharField(max_length=100)),
                ("file", models.FileField(upload_to="")),
                (
                    "submission",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="storages",
                        to="homeworks.submission",
                    ),
                ),
            ],
        ),
    ]
