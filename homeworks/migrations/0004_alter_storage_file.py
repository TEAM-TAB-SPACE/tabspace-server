# Generated by Django 4.1.5 on 2023-03-17 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("homeworks", "0003_remove_submission_file_remove_submission_url_storage"),
    ]

    operations = [
        migrations.AlterField(
            model_name="storage",
            name="file",
            field=models.FileField(blank=True, null=True, upload_to=""),
        ),
    ]
