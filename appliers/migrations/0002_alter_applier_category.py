# Generated by Django 4.1.5 on 2023-03-18 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("appliers", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="applier",
            name="category",
            field=models.CharField(
                choices=[("U", "U"), ("F", "F"), ("B", "B")], max_length=1
            ),
        ),
    ]
