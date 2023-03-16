# Generated by Django 4.1.5 on 2023-03-14 14:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("lectures", "0001_initial"),
        ("lecture_comments", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="lecturecomment",
            name="lecture",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="lectures.lecture",
            ),
            preserve_default=False,
        ),
    ]