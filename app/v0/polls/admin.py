from django.contrib import admin

from .models import Question

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
    ]
    list_display = ('question_text',)
    search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)