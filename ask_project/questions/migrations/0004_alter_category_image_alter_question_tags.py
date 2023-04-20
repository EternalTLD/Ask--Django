# Generated by Django 4.1.7 on 2023-04-20 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_alter_category_image_alter_questionimages_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(null=True, upload_to='categories/', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(related_name='question_tags', to='questions.tag', verbose_name='Tag'),
        ),
    ]
