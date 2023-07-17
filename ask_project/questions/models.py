from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    """Categories"""
    name = models.CharField(max_length=50, unique=True, verbose_name='Category')
    image = models.ImageField(null=True, upload_to='categories/', verbose_name='Image')
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse('questions:by_category', kwargs={'slug': self.url})

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

class Tag(models.Model):
    """Tags"""
    title = models.CharField(max_length=20, unique=True, verbose_name='Tag')
    url = models.SlugField(max_length=160, unique=True, default=title)
    
    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self):
        return reverse('questions:by_tag', kwargs={'slug': self.url})

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

class Question(models.Model):
    """Questions"""
    title = models.CharField(max_length=50, verbose_name='Title')
    category = models.ForeignKey(
        Category, 
        on_delete=models.PROTECT, 
        verbose_name='Category', 
        related_name='category'
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    date_published = models.DateField(verbose_name='Publication date')
    content = models.TextField(verbose_name='Question')
    likes = models.IntegerField(default=0, verbose_name='Likes')
    dislikes = models.IntegerField(default=0, verbose_name='Dislikes')
    viewes = models.IntegerField(default=0, verbose_name='Views')
    tags = models.ManyToManyField(Tag, verbose_name='Tag', related_name='tags')
    draft = models.BooleanField(default=False, verbose_name='Draft')
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self):
        return reverse('questions:question_detail', kwargs={'slug': self.url})

    
    class Meta:
        ordering = ['-date_published']
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
    
class Answer(models.Model):
    """Answers"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Question')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Author')
    content = models.TextField(verbose_name='Answer')
    date_published = models.DateField(verbose_name='Publication date')
    likes = models.IntegerField(default=0, verbose_name='Likes')
    dislikes = models.IntegerField(default=0, verbose_name='Dislikes')
    best_answer = models.BooleanField(default=False, verbose_name='Best answer')

    class Meta:
        ordering = ['likes']
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'
    
class QuestionImages(models.Model):
    """Additional images"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Question')
    image = models.ImageField(blank=True, upload_to='questions_images/', verbose_name='Image')

    class Meta:
        verbose_name = 'Question image'
        verbose_name_plural = 'Question images'