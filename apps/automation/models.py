from django.db import models
from apps.leads.models import Lead
from apps.workflows.models import Workflow, WorkflowAction, WorkflowTriggerType


class RunStatus(models.TextChoices):
    RUNNING = "running", "Running"
    SUCCESS = "success", "Success"
    FAILED = "failed", "Failed"
    PARTIAL_SUCCESS = "partial_success", "Partial Success"


class ActionLogStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    SUCCESS = "success", "Success"
    FAILED = "failed", "Failed"


class WorkflowRun(models.Model):
    workflow = models.ForeignKey(
        Workflow,
        on_delete=models.CASCADE,
        related_name="runs",
    )
    lead = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        related_name="workflow_runs",
    )
    trigger_type = models.CharField(
        max_length=50,
        choices=WorkflowTriggerType.choices,
    )
    status = models.CharField(
        max_length=30,
        choices=RunStatus.choices,
        default=RunStatus.RUNNING,
    )
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "workflow_runs"
        ordering = ["-started_at"]

    def __str__(self):
        return f"{self.workflow.name} - {self.lead.full_name} - {self.status}"


class ActionLog(models.Model):
    workflow_run = models.ForeignKey(
        WorkflowRun,
        on_delete=models.CASCADE,
        related_name="action_logs",
    )
    workflow_action = models.ForeignKey(
        WorkflowAction,
        on_delete=models.CASCADE,
        related_name="logs",
    )
    status = models.CharField(
        max_length=20,
        choices=ActionLogStatus.choices,
        default=ActionLogStatus.PENDING,
    )
    message = models.TextField(blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)
    executed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "action_logs"
        ordering = ["id"]

    def __str__(self):
        return f"Run {self.workflow_run_id} - Action {self.workflow_action.action_type} - {self.status}"