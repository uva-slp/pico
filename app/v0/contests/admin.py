from django.contrib import admin

from .models import Contest, Question, Submissions

class TeamsInline(admin.TabularInline):
    model = Contest.teams.through

class QuestionInline(admin.TabularInline):
    model = Question

@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title']}),
    ]
    inlines = [TeamsInline, QuestionInline]
    list_display = ('title', 'date_created')
    list_filter = ['date_created']
    search_fields = ['title', 'creator']
