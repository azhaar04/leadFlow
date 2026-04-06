from django.conf import settings
from django.db import models


class WorkflowTriggerType(models.TextChoices):
    NEW_LEAD_CREATED = "new_lead_created", "New Lead Created"
    LEAD_STATUS_CHANGED = "lead_status_changed", "Lead Status Changed"


class WorkflowStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"


class WorkflowConditionOperator(models.TextChoices):
    EQUALS = "equals", "Equals"
    NOT_EQUALS = "not_equals", "Not Equals"


class WorkflowActionType(models.TextChoices):
    ASSIGN_AGENT = "assign_agent", "Assign Agent"
    CREATE_TASK = "create_task", "Create Task"
    SEND_NOTIFICATION = "send_notification", "Send Notification"
    SEND_EMAIL = "send_email", "Send Email"


class Workflow(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    trigger_type = models.CharField(
        max_length=50,
        choices=WorkflowTriggerType.choices,
    )
    status = models.CharField(
        max_length=20,
        choices=WorkflowStatus.choices,
        default=WorkflowStatus.INACTIVE,
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="workflows",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "workflows"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class WorkflowCondition(models.Model):
    workflow = models.ForeignKey(
        Workflow,
        on_delete=models.CASCADE,
        related_name="conditions",
    )
    field_name = models.CharField(max_length=100)
    operator = models.CharField(
        max_length=30,
        choices=WorkflowConditionOperator.choices,
        default=WorkflowConditionOperator.EQUALS,
    )
    field_value = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "workflow_conditions"
        ordering = ["id"]

    def __str__(self):
        return f"{self.workflow.name}: {self.field_name} {self.operator} {self.field_value}"


class WorkflowAction(models.Model):
    workflow = models.ForeignKey(
        Workflow,
        on_delete=models.CASCADE,
        related_name="actions",
    )
    action_type = models.CharField(
        max_length=50,
        choices=WorkflowActionType.choices,
    )
    action_order = models.PositiveIntegerField()
    config = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "workflow_actions"
        ordering = ["action_order", "id"]
        unique_together = ("workflow", "action_order")

    def __str__(self):
        return f"{self.workflow.name} - {self.action_type} ({self.action_order})"