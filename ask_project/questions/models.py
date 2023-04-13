from django.db import models


class Category(models.Model):
    """Категории"""
    name = models.CharField(max_length=50, verbose_name='Category')
    image = models.ImageField(upload_to='static/images/categories', verbose_name='Image')
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

class User(models.User):
    """Пользователи"""
    avatar = models.ImageField(upload_to='static/images/avatars', verbose_name='Avatar')
    rating = models.IntegerField(default=0, verbose_name='Rating')
    
    def __str__(self) -> str:
        return self.username
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class Tag(models.Model):
    """Теги"""
    title = models.CharField(max_length=20, verbose_name='Tag')
    url = models.SlugField(max_length=160, unique=True)
    
    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

class Question(models.Model):
    """Вопросы"""
    title = models.CharField(max_length=50, verbose_name='Title')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Category')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    date_published = models.DateField(verbose_name='Publication date')
    content = models.TextField(verbose_name='Question')
    likes = models.IntegerField(default=0, verbose_name='Likes')
    dislikes = models.IntegerField(default=0, verbose_name='Dislikes')
    viewes = models.IntegerField(default=0, verbose_name='Views')
    additional_images = models.ForeignKey(verbose_name='AdditionalImages')
    tags = models.ManyToManyField(Tag, verbose_name='Tag')
    draft = models.BooleanField(default=False, verbose_name='Draft')
    url = models.URLField(max_length=160, unique=True)

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['-date_published']
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
    
class Answer(models.Model):
    """Ответы"""
    question = models.ForeignKey(Question, verbose_name='Question')
    author = models.ForeignKey(User, verbose_name='Author')
    content = models.TextField(verbose_name='Answer')
    date_published = models.DateField(verbose_name='Publication date')
    likes = models.IntegerField(default=0, verbose_name='Likes')
    dislikes = models.IntegerField(default=0, verbose_name='Dislikes')
    best_answer = models.BooleanField(default=False, verbose_name='Best answer')

    class Meta:
        ordering = ['-date_published']
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'
    
class QuestionImages(models.Model):
    """Прикрепленные изображения"""
    question = models.ForeignKey(Question, verbose_name='Question')
    image = models.ImageField(upload_to='static/images/questions_images', verbose_name='Image')

    class Meta:
        verbose_name = 'Question image'
        verbose_name_plural = 'Question images'