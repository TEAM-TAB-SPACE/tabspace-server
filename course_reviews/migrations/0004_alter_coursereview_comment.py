# Generated by Django 4.1.5 on 2023-03-27 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("course_reviews", "0003_alter_coursereview_comment_alter_coursereview_score"),
    ]

    operations = [
        migrations.AlterField(
            model_name="coursereview",
            name="comment",
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
    ]
