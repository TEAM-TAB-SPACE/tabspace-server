# Generated by Django 4.1.5 on 2023-03-13 05:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("lectures", "0001_initial"),
        ("dashboards", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="dashboard",
            name="latest_lecture",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.CreateModel(
            name="UserGrowths",
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
                ("ability", models.PositiveIntegerField(default=0)),
                (
                    "dashboard",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="dashboards.dashboard",
                    ),
                ),
                (
                    "lecture_category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="lectures.lecturecategory",
                    ),
                ),
            ],
        ),
    ]
