from rest_framework import generics
from apps.workflows.permissions import IsAdminRole
from .models import WorkflowRun, ActionLog
from .serializers import WorkflowRunListSerializer, WorkflowRunDetailSerializer, ActionLogSerializer


class WorkflowRunListView(generics.ListAPIView):
    permission_classes = [IsAdminRole]
    serializer_class = WorkflowRunListSerializer

    def get_queryset(self):
        return WorkflowRun.objects.select_related("workflow", "lead").prefetch_related(
            "action_logs__workflow_action"
        )


class WorkflowRunDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAdminRole]
    serializer_class = WorkflowRunDetailSerializer

    def get_queryset(self):
        return WorkflowRun.objects.select_related("workflow", "lead").prefetch_related(
            "action_logs__workflow_action"
        )
    

class WorkflowRunLogsView(generics.ListAPIView):
    permission_classes = [IsAdminRole]
    serializer_class = ActionLogSerializer

    def get_queryset(self):
        workflow_run_id = self.kwargs["pk"]
        return ActionLog.objects.select_related(
            "workflow_action",
            "workflow_run",
        ).filter(
            workflow_run_id=workflow_run_id
        ).order_by("id")