from django.contrib import admin
from .models import Workflow, WorkflowCondition, WorkflowAction


class WorkflowConditionInline(admin.TabularInline):
    model = WorkflowCondition
    extra = 0


class WorkflowActionInline(admin.TabularInline):
    model = WorkflowAction
    extra = 0


@admin.register(Workflow)
class WorkflowAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "trigger_type", "status", "created_by", "created_at"]
    search_fields = ["name", "description"]
    list_filter = ["trigger_type", "status", "created_at"]
    inlines = [WorkflowConditionInline, WorkflowActionInline]


@admin.register(WorkflowCondition)
class WorkflowConditionAdmin(admin.ModelAdmin):
    list_display = ["id", "workflow", "field_name", "operator", "field_value", "created_at"]


@admin.register(WorkflowAction)
class WorkflowActionAdmin(admin.ModelAdmin):
    list_display = ["id", "workflow", "action_type", "action_order", "is_active", "created_at"]
    list_filter = ["action_type", "is_active"]