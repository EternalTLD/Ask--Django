from django.contrib import admin

from .models import User, Category, Tag, Question, Answer, QuestionImages

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Question)
admin.site.register(Tag)
admin.site.register(Answer)
admin.site.register(QuestionImages)
