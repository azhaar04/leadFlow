from django.contrib import admin
from .models import WorkflowRun, ActionLog


class ActionLogInline(admin.TabularInline):
    model = ActionLog
    extra = 0
    readonly_fields = ["workflow_action", "status", "message", "error_message", "executed_at"]


@admin.register(WorkflowRun)
class WorkflowRunAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "workflow",
        "lead",
        "trigger_type",
        "status",
        "started_at",
        "finished_at",
    ]
    list_filter = ["trigger_type", "status", "started_at"]
    search_fields = ["workflow__name", "lead__full_name", "lead__email"]
    inlines = [ActionLogInline]


@admin.register(ActionLog)
class ActionLogAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "workflow_run",
        "workflow_action",
        "status",
        "executed_at",
    ]
    list_filter = ["status", "executed_at"]