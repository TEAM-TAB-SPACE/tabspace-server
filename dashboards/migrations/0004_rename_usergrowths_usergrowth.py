# Generated by Django 4.1.5 on 2023-03-14 04:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("lectures", "0001_initial"),
        ("dashboards", "0003_alter_dashboard_homework_progress"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="UserGrowths",
            new_name="UserGrowth",
        ),
    ]