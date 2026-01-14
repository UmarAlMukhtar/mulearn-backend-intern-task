from django.contrib import admin
from .models import Job, Skill

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'status', 'job_type', 'created_at')
    list_filter = ('status', 'job_type', 'location')
    search_fields = ('title', 'description')

admin.site.register(Skill)