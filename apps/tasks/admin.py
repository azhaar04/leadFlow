from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "lead",
        "assigned_to",
        "status",
        "due_date",
        "completed_at",
        "created_by_user",
        "created_at",
    ]
    search_fields = ["title", "description", "lead__full_name", "assigned_to__email"]
    list_filter = ["status", "assigned_to", "due_date", "created_at"]