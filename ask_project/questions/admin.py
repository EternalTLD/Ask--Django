from django.contrib import admin
from .models import Question, Answer, QuestionImages


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'date_published', 'draft']
    list_filter = ['draft', 'date_published', 'date_created', 'author']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'date_published'
    ordering = ['-draft', 'date_published']

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['question', 'author', 'date_published', 'best_answer', 'active']
    list_filter = ['question', 'author', 'date_published', 'best_answer', 'active']
    search_fields = ['question', 'content']
    ordering = ['date_published']

admin.site.register(QuestionImages)
