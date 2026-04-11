from rest_framework import generics
from apps.workflows.permissions import IsAdminRole
from .models import WorkflowRun
from .serializers import WorkflowRunListSerializer, WorkflowRunDetailSerializer


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