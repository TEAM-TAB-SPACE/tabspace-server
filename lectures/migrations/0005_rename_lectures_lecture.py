# Generated by Django 4.1.5 on 2023-03-07 07:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("lectures", "0004_alter_lectures_date"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Lectures",
            new_name="Lecture",
        ),
    ]
