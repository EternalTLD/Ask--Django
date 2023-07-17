# Generated by Django 4.2 on 2023-04-13 20:54

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('avatar', models.ImageField(upload_to='static/images/avatars', verbose_name='Avatar')),
                ('rating', models.IntegerField(default=0, verbose_name='Rating')),
                ('is_activated', models.BooleanField(default=True, verbose_name="Is user's email activated?")),
                ('send_messages', models.BooleanField(default=True, verbose_name='Send notifications?')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Category')),
                ('image', models.ImageField(upload_to='static/images/categories', verbose_name='Image')),
                ('url', models.SlugField(max_length=160, unique=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Title')),
                ('date_published', models.DateField(verbose_name='Publication date')),
                ('content', models.TextField(verbose_name='Question')),
                ('likes', models.IntegerField(default=0, verbose_name='Likes')),
                ('dislikes', models.IntegerField(default=0, verbose_name='Dislikes')),
                ('viewes', models.IntegerField(default=0, verbose_name='Views')),
                ('draft', models.BooleanField(default=False, verbose_name='Draft')),
                ('url', models.URLField(max_length=160, unique=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='questions.category', verbose_name='Category')),
            ],
            options={
                'verbose_name': 'Question',
                'verbose_name_plural': 'Questions',
                'ordering': ['-date_published'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, unique=True, verbose_name='Tag')),
                ('url', models.SlugField(max_length=160, unique=True)),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
        ),
        migrations.CreateModel(
            name='QuestionImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='static/images/questions_images', verbose_name='Image')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.question', verbose_name='Question')),
            ],
            options={
                'verbose_name': 'Question image',
                'verbose_name_plural': 'Question images',
            },
        ),
        migrations.AddField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(related_name='question_tags', to='questions.tag', verbose_name='Tag'),
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='Answer')),
                ('date_published', models.DateField(verbose_name='Publication date')),
                ('likes', models.IntegerField(default=0, verbose_name='Likes')),
                ('dislikes', models.IntegerField(default=0, verbose_name='Dislikes')),
                ('best_answer', models.BooleanField(default=False, verbose_name='Best answer')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Author')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.question', verbose_name='Question')),
            ],
            options={
                'verbose_name': 'Answer',
                'verbose_name_plural': 'Answers',
                'ordering': ['likes'],
            },
        ),
    ]