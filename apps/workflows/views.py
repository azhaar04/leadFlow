from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Workflow, WorkflowCondition, WorkflowAction, WorkflowStatus
from .permissions import IsAdminRole
from .serializers import (
    WorkflowListSerializer,
    WorkflowDetailSerializer,
    WorkflowCreateUpdateSerializer,
    WorkflowConditionSerializer,
    WorkflowActionSerializer,
)


class WorkflowListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdminRole]

    def get_queryset(self):
        return Workflow.objects.select_related("created_by").prefetch_related(
            "conditions", "actions"
        )

    def get_serializer_class(self):
        if self.request.method == "POST":
            return WorkflowCreateUpdateSerializer
        return WorkflowListSerializer


class WorkflowRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAdminRole]

    def get_queryset(self):
        return Workflow.objects.select_related("created_by").prefetch_related(
            "conditions", "actions"
        )

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return WorkflowCreateUpdateSerializer
        return WorkflowDetailSerializer


class WorkflowActivateView(APIView):
    permission_classes = [IsAdminRole]

    def post(self, request, pk):
        try:
            workflow = Workflow.objects.get(pk=pk)
        except Workflow.DoesNotExist:
            return Response({"detail": "Workflow not found."}, status=status.HTTP_404_NOT_FOUND)

        workflow.status = WorkflowStatus.ACTIVE
        workflow.save(update_fields=["status", "updated_at"])

        return Response(WorkflowDetailSerializer(workflow).data, status=status.HTTP_200_OK)


class WorkflowDeactivateView(APIView):
    permission_classes = [IsAdminRole]

    def post(self, request, pk):
        try:
            workflow = Workflow.objects.get(pk=pk)
        except Workflow.DoesNotExist:
            return Response({"detail": "Workflow not found."}, status=status.HTTP_404_NOT_FOUND)

        workflow.status = WorkflowStatus.INACTIVE
        workflow.save(update_fields=["status", "updated_at"])

        return Response(WorkflowDetailSerializer(workflow).data, status=status.HTTP_200_OK)


class WorkflowConditionCreateView(APIView):
    permission_classes = [IsAdminRole]

    def post(self, request, pk):
        try:
            workflow = Workflow.objects.get(pk=pk)
        except Workflow.DoesNotExist:
            return Response({"detail": "Workflow not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = WorkflowConditionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(workflow=workflow)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class WorkflowActionCreateView(APIView):
    permission_classes = [IsAdminRole]

    def post(self, request, pk):
        try:
            workflow = Workflow.objects.get(pk=pk)
        except Workflow.DoesNotExist:
            return Response({"detail": "Workflow not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = WorkflowActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(workflow=workflow)

        return Response(serializer.data, status=status.HTTP_201_CREATED)