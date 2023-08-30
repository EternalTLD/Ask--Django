from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline

from .models import Question, Answer, QuestionImages, Vote


class VoteAdmin(GenericStackedInline):
    model = Vote

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [VoteAdmin]
    list_display = ['title', 'author', 'date_published', 'draft']
    list_filter = ['draft', 'date_published', 'date_created', 'author']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'date_published'
    ordering = ['-draft', 'date_published']

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    inlines = [VoteAdmin]
    list_display = ['question', 'author', 'date_published', 'best_answer', 'active']
    list_filter = ['question', 'author', 'date_published', 'best_answer', 'active']
    search_fields = ['question', 'content']
    ordering = ['date_published']

admin.site.register(QuestionImages)