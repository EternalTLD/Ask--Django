from django.db import models
from django.db.models.query import QuerySet
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager

from users.models import User
    
class PublishedManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(draft=False)

class Question(models.Model):
    """Questions"""
    title = models.CharField(max_length=25, verbose_name='Заголовок')
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name= 'questions', 
        verbose_name='Автор',
    )
    date_published = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    date_updated = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    content = models.TextField(verbose_name='Содержание')
    likes = models.IntegerField(default=0, verbose_name='Лайки')
    dislikes = models.IntegerField(default=0, verbose_name='Дизлайки')
    views = models.IntegerField(default=0, verbose_name='Просмотры')
    draft = models.BooleanField(default=False, verbose_name='Черновик')
    slug = models.SlugField(max_length=25)

    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager()

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
        return reverse('questions:question_detail', kwargs={'id': self.pk, 'slug': self.slug})
    
class Answer(models.Model):
    """Answers"""
    question = models.ForeignKey(
        Question, 
        on_delete=models.CASCADE,
        related_name='answers', 
        verbose_name='Вопрос',
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='answers',
        verbose_name='Автор',
    )
    content = models.TextField(verbose_name='Содержание')
    date_published = models.DateField(auto_now_add=True, verbose_name='Дата публикации')
    likes = models.IntegerField(default=0, verbose_name='Лайки')
    dislikes = models.IntegerField(default=0, verbose_name='Дизлайки')
    best_answer = models.BooleanField(default=False, verbose_name='Лучший ответ')
    active = models.BooleanField(default=True, verbose_name='Активный')

    class Meta:
        ordering = ['likes', '-date_published']
        indexes = [
            models.Index(fields=['likes', '-date_published'])
        ]
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self) -> str:
        return f'Ответ {self.author} на вопрос {self.question}'
    
class QuestionImages(models.Model):
    """Additional images"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос')
    image = models.ImageField(blank=True, upload_to='questions_images/', verbose_name='Картинка')

    class Meta:
        verbose_name = 'Картинка к вопросу'
        verbose_name_plural = 'Картинки к вопросу'

class AnswerImages(models.Model):
    """Additional images"""
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, verbose_name='Ответ')
    image = models.ImageField(blank=True, null=True, upload_to='questions_images/', verbose_name='Картинка')

    class Meta:
        verbose_name = 'Картинка к ответу'
        verbose_name_plural = 'Картинки к ответу'