# Generated by Django 4.2.5 on 2024-01-13 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_alter_question_slug'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='answer',
            name='questions_a_date_pu_8e5856_idx',
        ),
        migrations.RemoveIndex(
            model_name='question',
            name='questions_q_date_pu_b6f501_idx',
        ),
        migrations.AddIndex(
            model_name='answer',
            index=models.Index(fields=['-date_published', 'author', 'question'], name='questions_a_date_pu_2a8463_idx'),
        ),
        migrations.AddIndex(
            model_name='question',
            index=models.Index(fields=['-date_published', 'author'], name='questions_q_date_pu_21b090_idx'),
        ),
    ]
