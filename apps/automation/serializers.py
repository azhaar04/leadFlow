from rest_framework import serializers
from .models import WorkflowRun, ActionLog


class ActionLogSerializer(serializers.ModelSerializer):
    workflow_action_type = serializers.CharField(source="workflow_action.action_type", read_only=True)

    class Meta:
        model = ActionLog
        fields = [
            "id",
            "workflow_action",
            "workflow_action_type",
            "status",
            "message",
            "error_message",
            "executed_at",
        ]


class WorkflowRunListSerializer(serializers.ModelSerializer):
    workflow_name = serializers.CharField(source="workflow.name", read_only=True)
    lead_name = serializers.CharField(source="lead.full_name", read_only=True)

    class Meta:
        model = WorkflowRun
        fields = [
            "id",
            "workflow",
            "workflow_name",
            "lead",
            "lead_name",
            "trigger_type",
            "status",
            "started_at",
            "finished_at",
            "error_message",
        ]


class WorkflowRunDetailSerializer(serializers.ModelSerializer):
    workflow_name = serializers.CharField(source="workflow.name", read_only=True)
    lead_name = serializers.CharField(source="lead.full_name", read_only=True)
    action_logs = ActionLogSerializer(many=True, read_only=True)

    class Meta:
        model = WorkflowRun
        fields = [
            "id",
            "workflow",
            "workflow_name",
            "lead",
            "lead_name",
            "trigger_type",
            "status",
            "started_at",
            "finished_at",
            "error_message",
            "action_logs",
        ]