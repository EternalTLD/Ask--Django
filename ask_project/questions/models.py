from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    """Categories"""
    name = models.CharField(max_length=50, unique=True, verbose_name='Категория')
    image = models.ImageField(null=True, upload_to='categories/', verbose_name='Картинка')
    slug = models.SlugField(max_length=160, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse('questions:by_category', kwargs={'slug': self.slug})

class Tag(models.Model):
    """Tags"""
    title = models.CharField(max_length=20, unique=True, verbose_name='Тег')
    slug = models.SlugField(max_length=160, unique=True, default=title)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
    
    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self):
        return reverse('questions:by_tag', kwargs={'slug': self.slug})

class Question(models.Model):
    """Questions"""
    title = models.CharField(max_length=50, verbose_name='Заголовок')
    category = models.ForeignKey(
        Category, 
        on_delete=models.PROTECT, 
        verbose_name='Категория', 
        related_name='category'
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    date_published = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    date_updated = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    content = models.TextField(verbose_name='Содержание')
    likes = models.IntegerField(default=0, verbose_name='Лайки')
    dislikes = models.IntegerField(default=0, verbose_name='Дизлайки')
    viewes = models.IntegerField(default=0, verbose_name='Просмотры')
    tags = models.ManyToManyField(Tag, verbose_name='Теги', related_name='tags')
    draft = models.BooleanField(default=False, verbose_name='Черновик')
    slug = models.SlugField(max_length=160, unique=True)

    class Meta:
        ordering = ['-date_published']
        indexes = [
            models.Index(fields=['-date_published']),
        ]
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self):
        return reverse('questions:question_detail', kwargs={'slug': self.slug})
    
class Answer(models.Model):
    """Answers"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    content = models.TextField(verbose_name='Содержание')
    date_published = models.DateField(verbose_name='Дата публикации')
    likes = models.IntegerField(default=0, verbose_name='Лайки')
    dislikes = models.IntegerField(default=0, verbose_name='Дизлайки')
    best_answer = models.BooleanField(default=False, verbose_name='Лучший ответ')

    class Meta:
        ordering = ['-likes']
        indexes = [
            models.Index(fields=['-likes'])
        ]
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
    
class QuestionImages(models.Model):
    """Additional images"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос')
    image = models.ImageField(blank=True, upload_to='questions_images/', verbose_name='Картинка')

    class Meta:
        verbose_name = 'Прикрепленная картинка'
        verbose_name_plural = 'Прикрепленные картинки'