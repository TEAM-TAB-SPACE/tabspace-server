# Generated by Django 4.1.5 on 2023-03-21 01:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "lecture_comments",
            "0005_rename_comment_commentreply_lecture_comment_and_more",
        ),
    ]

    operations = [
        migrations.RenameField(
            model_name="commentreply",
            old_name="reply",
            new_name="comment",
        ),
    ]
