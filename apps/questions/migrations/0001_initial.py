# Generated by Django 4.2.5 on 2024-01-26 14:28

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=5000)),
                ('date_published', models.DateField(auto_now_add=True)),
                ('best_answer', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['-date_published'],
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Max length - 25 symbols.', max_length=25)),
                ('date_published', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('content', models.TextField(max_length=5000)),
                ('views', models.IntegerField(default=0)),
                ('draft', models.BooleanField(default=False)),
                ('slug', models.SlugField(blank=True)),
            ],
            options={
                'ordering': ['-date_published'],
            },
        ),
        migrations.CreateModel(
            name='QuestionImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='questions_images/%Y/%m/%d/')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.question')),
            ],
        ),
    ]
