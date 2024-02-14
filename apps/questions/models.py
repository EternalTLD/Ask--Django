from __future__ import annotations

from django.db import models
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.text import slugify
from django.core.cache import cache

from taggit.managers import TaggableManager
from taggit.models import Tag
from apps.votes.models import Vote


class PublishedManager(models.Manager):
    """Published questions manager"""

    def get_queryset(self) -> models.QuerySet[Question]:
        """Returns query set of published questions"""
        return super().get_queryset().filter(draft=False)

    def get_all_questions(self) -> models.QuerySet[Question]:
        """Returns query set of all published questions"""
        queryset = (
            self.get_queryset()
            .select_related("author", "author__profile")
            .prefetch_related("tags")
            .annotate(
                likes_count=models.Count(
                    models.Case(
                        models.When(votes__vote=1, then=1),
                        output_field=models.IntegerField(),
                    )
                ),
                dislikes_count=models.Count(
                    models.Case(
                        models.When(votes__vote=-1, then=1),
                        output_field=models.IntegerField(),
                    )
                ),
            )
            .all()
        )
        return queryset

    def get_tagged_questions(self, tag: str) -> models.QuerySet[Question]:
        """Returns query set of all published questions tagged by `tag`"""
        tag = get_object_or_404(Tag, slug=tag)
        queryset = self.get_all_questions().filter(tags__in=[tag])
        return queryset

    def get_similar_questions(
        self, question: Question, limit: int = 4
    ) -> models.QuerySet[Question]:
        """Returns query set of published questions similar to a specific question"""
        cache_key = f"similar_questions_{question.id}"
        similar_questions = cache.get(cache_key)
        if similar_questions is None:
            question_tags_ids = question.tags.values_list("id", flat=True)
            similar_questions = (
                self.get_queryset()
                .filter(tags__in=question_tags_ids)
                .exclude(id=question.id)
                .annotate(same_tags=models.Count("tags"))
                .order_by("-same_tags", "-date_published")[:limit]
            )
            cache.set(cache_key, similar_questions, timeout=3600)
        return similar_questions

    def get_popular_questions(self, limit: int = None) -> models.QuerySet[Question]:
        """Returns query set of popular published questions"""
        if limit:
            return self.get_all_questions().order_by("-views", "-votes")[:limit]
        return self.get_all_questions().order_by("-views", "-votes")

    def get_popular_tags(self, limit: int = 10) -> models.QuerySet[Tag]:
        """Returns the most popular tags"""
        cache_key = "popular_tags_list"
        tags = cache.get(cache_key)
        if tags is None:
            tags = (
                Tag.objects.filter(question__draft=False)
                .annotate(total_questions=models.Count("question"))
                .order_by("-total_questions")[:limit]
            )
            cache.set(cache_key, tags, timeout=86400)
        return tags

    def get_question_answers(self, question: Question) -> models.QuerySet[Answer]:
        """Returns query set of answers for a specific question"""
        answers = (
            Answer.objects.filter(question=question, active=True)
            .select_related("author", "author__profile")
            .annotate(
                likes_count=models.Count(
                    models.Case(
                        models.When(votes__vote=1, then=1),
                        output_field=models.IntegerField(),
                    )
                ),
                dislikes_count=models.Count(
                    models.Case(
                        models.When(votes__vote=-1, then=1),
                        output_field=models.IntegerField(),
                    )
                ),
            )
        )
        return answers

    def search(self, query: str) -> models.QuerySet[Question]:
        lookup = models.Q(title__icontains=query) | models.Q(content__icontains=query)
        return self.get_all_questions().filter(lookup)


class Question(models.Model):
    """Question model"""

    title = models.CharField(
        max_length=25,
        help_text="Max length - 25 symbols.",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="questions",
    )
    votes = GenericRelation(Vote, related_query_name="questions")
    date_published = models.DateTimeField(default=timezone.now)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    content = models.TextField(max_length=5000)
    views = models.IntegerField(default=0)
    draft = models.BooleanField(default=False)
    slug = models.SlugField(max_length=50, blank=True)

    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager()

    class Meta:
        ordering = ["-date_published"]
        indexes = [
            models.Index(fields=["-date_published", "author"]),
        ]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse("questions:detail", kwargs={"pk": self.pk, "slug": self.slug})

    def save(self, *args, **kwargs) -> None:
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class QuestionImages(models.Model):
    """Images attached to the question"""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, upload_to="questions_images/%Y/%m/%d/")


class Answer(models.Model):
    """Answer model"""

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="answers",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="answers",
    )
    votes = GenericRelation(Vote, related_query_name="answers")
    content = models.TextField(max_length=5000)
    date_published = models.DateField(auto_now_add=True)
    best_answer = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-date_published"]
        indexes = [models.Index(fields=["-date_published", "author", "question"])]

    def __str__(self) -> str:
        return f"{self.author} gives an answer on {self.question}"

    def get_absolute_url(self) -> str:
        return reverse(
            "questions:detail",
            kwargs={"pk": self.question.pk, "slug": self.question.slug},
        )
