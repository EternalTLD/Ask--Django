# Generated by Django 4.2.5 on 2024-01-07 21:59

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("votes", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="vote",
            old_name="vote",
            new_name="vote_type",
        ),
    ]