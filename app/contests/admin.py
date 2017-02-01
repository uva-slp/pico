from django.contrib import admin

from .models import Contest, Submission, Problem, Participant, Notification

# @admin.register(Contest)
# class ContestAdmin(admin.ModelAdmin):
#     fieldsets = [
#         (None, {'fields': ['title']}),
#     ]
#     #inlines = [TeamsInline, QuestionInline]
#     list_display = ('title', 'date_created', 'id')
#     list_filter = ['date_created']
#     search_fields = ['title', 'creator']

admin.site.register(Contest)
admin.site.register(Submission)
admin.site.register(Problem)
admin.site.register(Participant)
admin.site.register(Notification)
