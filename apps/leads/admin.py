from django.contrib import admin
from .models import Lead, LeadNote


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ["id", "full_name", "email", "phone", "company_name", "status", "assigned_agent", "created_by", "created_at"]
    search_fields = ["full_name", "email", "phone", "company_name"]
    list_filter = ["status", "assigned_agent", "created_at"]


@admin.register(LeadNote)
class LeadNoteAdmin(admin.ModelAdmin):
    list_display = ["id", "lead", "user", "created_at"]
    search_fields = ["lead__full_name", "user__email", "note"]
    list_filter = ["created_at"]