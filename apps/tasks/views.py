from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Task, TaskStatus
from .permissions import IsAdminOrAssignedTaskAgent
from .serializers import (
    TaskListSerializer,
    TaskDetailSerializer,
    TaskCreateSerializer,
    TaskUpdateSerializer,
    TaskCompleteSerializer,
)


class TaskListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        queryset = Task.objects.select_related(
            "lead", "assigned_to", "created_by_user"
        )

        if user.role == "admin":
            return queryset.all()

        return queryset.filter(assigned_to=user)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return TaskCreateSerializer
        return TaskListSerializer

    def create(self, request, *args, **kwargs):
        if request.user.role != "admin":
            return Response(
                {"detail": "Only admins can create tasks."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().create(request, *args, **kwargs)


class TaskRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminOrAssignedTaskAgent]

    def get_queryset(self):
        return Task.objects.select_related(
            "lead", "assigned_to", "created_by_user"
        )

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return TaskUpdateSerializer
        return TaskDetailSerializer

    def update(self, request, *args, **kwargs):
        task = self.get_object()

        if request.user.role == "agent":
            forbidden_fields = {"assigned_to"}
            sent_fields = set(request.data.keys())

            if forbidden_fields.intersection(sent_fields):
                return Response(
                    {"detail": "Agents cannot reassign tasks."},
                    status=status.HTTP_403_FORBIDDEN,
                )

        return super().update(request, *args, **kwargs)


class TaskCompleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            task = Task.objects.select_related("lead", "assigned_to", "created_by_user").get(pk=pk)
        except Task.DoesNotExist:
            return Response(
                {"detail": "Task not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if request.user.role != "admin" and task.assigned_to_id != request.user.id:
            return Response(
                {"detail": "You do not have permission to complete this task."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = TaskCompleteSerializer(data=request.data or {})
        serializer.is_valid(raise_exception=True)

        task.status = TaskStatus.COMPLETED
        task.completed_at = timezone.now()
        task.save(update_fields=["status", "completed_at", "updated_at"])

        return Response(TaskDetailSerializer(task).data, status=status.HTTP_200_OK)