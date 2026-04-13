from rest_framework import serializers


class RecentWorkflowRunSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    workflow_name = serializers.CharField()
    lead_name = serializers.CharField()
    status = serializers.CharField()
    started_at = serializers.DateTimeField()


class RecentLeadUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    full_name = serializers.CharField()
    status = serializers.CharField()
    updated_at = serializers.DateTimeField()


class AdminDashboardSerializer(serializers.Serializer):
    total_leads = serializers.IntegerField()
    leads_by_status = serializers.DictField(child=serializers.IntegerField())
    total_active_workflows = serializers.IntegerField()
    total_pending_tasks = serializers.IntegerField()
    overdue_tasks = serializers.IntegerField()
    recent_workflow_runs = RecentWorkflowRunSerializer(many=True)


class AgentDashboardSerializer(serializers.Serializer):
    my_assigned_leads_count = serializers.IntegerField()
    my_pending_tasks = serializers.IntegerField()
    my_overdue_tasks = serializers.IntegerField()
    recent_lead_updates = RecentLeadUpdateSerializer(many=True)