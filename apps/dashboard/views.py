from django.db.models import Count
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsAdminUserRole, IsAgentUserRole
from apps.leads.models import Lead, LeadStatus
from apps.tasks.models import Task, TaskStatus
from apps.workflows.models import Workflow, WorkflowStatus
from apps.automation.models import WorkflowRun
from .serializers import AdminDashboardSerializer, AgentDashboardSerializer

class AdminDashboardView(APIView):
    permission_classes = [IsAdminUserRole]

    def get(self, request):
        total_leads = Lead.objects.count()

        lead_status_counts = Lead.objects.values("status").annotate(count=Count("id"))
        leads_by_status = {
            status_key: 0
            for status_key, _ in LeadStatus.choices
        }
        for item in lead_status_counts:
            leads_by_status[item["status"]] = item["count"]

        total_active_workflows = Workflow.objects.filter(
            status=WorkflowStatus.ACTIVE
        ).count()

        total_pending_tasks = Task.objects.filter(
            status=TaskStatus.PENDING
        ).count()

        overdue_tasks = Task.objects.filter(
            due_date__lt=timezone.now()
        ).exclude(
            status=TaskStatus.COMPLETED
        ).count()

        recent_runs_qs = WorkflowRun.objects.select_related(
            "workflow", "lead"
        ).order_by("-started_at")[:5]

        recent_workflow_runs = [
            {
                "id": run.id,
                "workflow_name": run.workflow.name,
                "lead_name": run.lead.full_name,
                "status": run.status,
                "started_at": run.started_at,
            }
            for run in recent_runs_qs
        ]

        data = {
            "total_leads": total_leads,
            "leads_by_status": leads_by_status,
            "total_active_workflows": total_active_workflows,
            "total_pending_tasks": total_pending_tasks,
            "overdue_tasks": overdue_tasks,
            "recent_workflow_runs": recent_workflow_runs,
        }

        serializer = AdminDashboardSerializer(data)
        return Response(serializer.data)
    
class AgentDashboardView(APIView):
    permission_classes = [IsAgentUserRole]

    def get(self, request):
        user = request.user

        my_assigned_leads_count = Lead.objects.filter(
            assigned_agent=user
        ).count()

        my_pending_tasks = Task.objects.filter(
            assigned_to=user,
            status=TaskStatus.PENDING,
        ).count()

        my_overdue_tasks = Task.objects.filter(
            assigned_to=user,
            due_date__lt=timezone.now(),
        ).exclude(
            status=TaskStatus.COMPLETED
        ).count()

        recent_leads_qs = Lead.objects.filter(
            assigned_agent=user
        ).order_by("-updated_at")[:5]

        recent_lead_updates = [
            {
                "id": lead.id,
                "full_name": lead.full_name,
                "status": lead.status,
                "updated_at": lead.updated_at,
            }
            for lead in recent_leads_qs
        ]

        data = {
            "my_assigned_leads_count": my_assigned_leads_count,
            "my_pending_tasks": my_pending_tasks,
            "my_overdue_tasks": my_overdue_tasks,
            "recent_lead_updates": recent_lead_updates,
        }

        serializer = AgentDashboardSerializer(data)
        return Response(serializer.data)