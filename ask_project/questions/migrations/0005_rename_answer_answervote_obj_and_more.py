# Generated by Django 4.2 on 2023-08-08 15:54

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("questions", "0004_answervote_questionvote_alter_answer_options_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="answervote",
            old_name="answer",
            new_name="obj",
        ),
        migrations.RenameField(
            model_name="questionvote",
            old_name="question",
            new_name="obj",
        ),
    ]
