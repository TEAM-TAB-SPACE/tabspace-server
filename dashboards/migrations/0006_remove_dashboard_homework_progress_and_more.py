# Generated by Django 4.1.5 on 2023-03-20 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dashboards", "0005_remove_dashboard_latest_lecture"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="dashboard",
            name="homework_progress",
        ),
        migrations.AddField(
            model_name="dashboard",
            name="notifications",
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
    ]
