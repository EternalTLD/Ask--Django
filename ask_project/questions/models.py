from django.db import models
from django.db.models.query import QuerySet
from django.urls import reverse
from django.utils import timezone

from taggit.managers import TaggableManager
from users.models import User

    
class PublishedManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(draft=False)
    
class QuestionVote(models.Model):
    LIKE = 1
    DISLIKE = -1

    VOTES = (
        (LIKE, 'like'),
        (DISLIKE, 'dislike')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    vote = models.SmallIntegerField(choices=VOTES, verbose_name='Голос')
    voted_at = models.DateTimeField(auto_now_add=True)

class Question(models.Model):
    """Questions"""
    title = models.CharField(
        max_length=25, 
        help_text='Максимальная длина - 25 символов.',
        verbose_name='Заголовок'
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name= 'questions', 
        verbose_name='Пользователь',
    )
    votes = models.ManyToManyField(
        User,
        blank=True,
        related_name='question_user',
        through=QuestionVote,
        verbose_name='Голос',
    )
    date_published = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    date_updated = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    content = models.TextField(verbose_name='Содержание')
    views = models.IntegerField(default=0, verbose_name='Просмотры')
    draft = models.BooleanField(default=False, verbose_name='Черновик')
    slug = models.SlugField(max_length=50)

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
    
class QuestionImages(models.Model):
    """Additional images"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос')
    image = models.ImageField(blank=True, upload_to='questions_images/', verbose_name='Картинка')

    class Meta:
        verbose_name = 'Картинка к вопросу'
        verbose_name_plural = 'Картинки к вопросу'
    
class AnswerVote(models.Model):
    LIKE = 1
    DISLIKE = -1

    VOTES = (
        (LIKE, 'like'),
        (DISLIKE, 'dislike')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE)
    vote = models.SmallIntegerField(choices=VOTES, verbose_name='Голос')
    voted_at = models.DateTimeField(auto_now_add=True)
    
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
        verbose_name='Пользователь',
    )
    votes = models.ManyToManyField(
        User,
        blank=True,
        related_name='answer_user',
        through=AnswerVote,
        verbose_name='Голос',
    )
    content = models.TextField(verbose_name='Содержание')
    date_published = models.DateField(auto_now_add=True, verbose_name='Дата публикации')
    best_answer = models.BooleanField(default=False, verbose_name='Лучший ответ')
    active = models.BooleanField(default=True, verbose_name='Активный')

    class Meta:
        ordering = ['-date_published']
        indexes = [
            models.Index(fields=['-date_published'])
        ]
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self) -> str:
        return f'Ответ {self.author} на вопрос {self.question}'

class AnswerImages(models.Model):
    """Additional images"""
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, verbose_name='Ответ')
    image = models.ImageField(blank=True, null=True, upload_to='questions_images/', verbose_name='Картинка')

    class Meta:
        verbose_name = 'Картинка к ответу'
        verbose_name_plural = 'Картинки к ответу'