from django.contrib import admin

from .models import *

class TasksAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'content', 'deadline', 'time_create', 'status', 'added_by')
    list_editable = ('status',)
    list_filter = ('status', 'time_create')
    prepopulated_fields = {'slug': ("title",)}


admin.site.register(Tasks, TasksAdmin)



