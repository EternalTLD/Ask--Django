from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import Count

from taggit.managers import TaggableManager
from votes.models import Vote


class PublishedManager(models.Manager):
    """Published questions manager"""

    def get_queryset(self):
        """Returns query set of published questions"""
        return super().get_queryset().filter(draft=False)

    def get_similar_questions(self, question, limit=4):
        """Returns query set of published questions similar to a specific question"""
        question_tags_ids = question.tags.values_list("id", flat=True)
        similar_questions = (
            self.get_queryset()
            .filter(tags__in=question_tags_ids)
            .exclude(id=question.id)
            .annotate(same_tags=Count("tags"))
            .order_by("-same_tags", "-date_published")[:limit]
        )
        return similar_questions


class Question(models.Model):
    """Question model"""

    title = models.CharField(
        max_length=25,
        help_text="Максимальная длина - 25 символов.",
        verbose_name="Заголовок",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="questions",
        verbose_name="Пользователь",
    )
    votes = GenericRelation(Vote, related_query_name="questions")
    date_published = models.DateTimeField(
        default=timezone.now, verbose_name="Дата публикации"
    )
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    content = models.TextField(verbose_name="Содержание")
    views = models.IntegerField(default=0, verbose_name="Просмотры")
    draft = models.BooleanField(default=False, verbose_name="Черновик")
    slug = models.SlugField(max_length=50)

    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager()

    class Meta:
        ordering = ["-date_published"]
        indexes = [
            models.Index(fields=["-date_published"]),
        ]
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse(
            "questions:question_detail", kwargs={"pk": self.pk, "slug": self.slug}
        )


class QuestionImages(models.Model):
    """Images attached to the question"""

    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, verbose_name="Вопрос"
    )
    image = models.ImageField(
        blank=True, upload_to="questions_images/%Y/%m/%d/", verbose_name="Картинка"
    )

    class Meta:
        verbose_name = "Картинка к вопросу"
        verbose_name_plural = "Картинки к вопросу"


class Answer(models.Model):
    """Answer model"""

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="answers",
        verbose_name="Вопрос",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="answers",
        verbose_name="Пользователь",
    )
    votes = GenericRelation(Vote, related_query_name="answers")
    content = models.TextField(verbose_name="Содержание")
    date_published = models.DateField(auto_now_add=True, verbose_name="Дата публикации")
    best_answer = models.BooleanField(default=False, verbose_name="Лучший ответ")
    active = models.BooleanField(default=True, verbose_name="Активный")

    class Meta:
        ordering = ["-date_published"]
        indexes = [models.Index(fields=["-date_published"])]
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    def __str__(self) -> str:
        return f"Ответ {self.author} на вопрос {self.question}"

    def get_absolute_url(self) -> str:
        return reverse(
            "questions:question_detail",
            kwargs={"pk": self.question.pk, "slug": self.question.slug},
        )
