# Generated by Django 4.2 on 2023-08-02 14:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0002_rename_viewes_question_views'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='category',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]