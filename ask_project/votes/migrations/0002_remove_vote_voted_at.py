# Generated by Django 4.2 on 2023-08-30 15:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('votes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vote',
            name='voted_at',
        ),
    ]