# Generated by Django 4.2 on 2023-08-27 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='read_at',
            field=models.DateTimeField(default=None, null=True, verbose_name='Прочитано'),
        ),
    ]
