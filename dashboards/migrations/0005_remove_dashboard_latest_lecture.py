# Generated by Django 4.1.5 on 2023-03-16 13:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("dashboards", "0004_rename_usergrowths_usergrowth"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="dashboard",
            name="latest_lecture",
        ),
    ]