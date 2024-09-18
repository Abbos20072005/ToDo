from django.contrib import admin
from .models import Tasks, Comment

@admin.register(Tasks)
class TasksAdmin(admin.ModelAdmin):
    list_display = ['id', "author", 'title', 'status', 'due_date']
    list_display_links = ['id', 'author', 'title']
    search_fields = ['author', 'title']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'task', 'created_at']
    list_display_links = ['id', 'author']
    search_fields = ['author', 'task']