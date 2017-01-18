from django.contrib import admin

from .models import Alert, Target

class TargetInline(admin.StackedInline):
    model = Target

class AlertAdmin(admin.ModelAdmin):
    inlines = [TargetInline]

admin.site.register(Alert, AlertAdmin)
