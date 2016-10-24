from django.contrib import admin

from .models import Team

class MembersInline(admin.TabularInline):
	model = Team.members.through

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['name']}),
	]
	inlines = [MembersInline]
	list_display = ('name', 'date_created')
	list_filter = ['date_created']
	search_fields = ['name']
