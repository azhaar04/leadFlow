from django.utils import timezone
from rest_framework import serializers
from apps.accounts.models import User
from apps.leads.models import Lead
from .models import Task, TaskStatus


class TaskListSerializer(serializers.ModelSerializer):
    lead_name = serializers.CharField(source="lead.full_name", read_only=True)
    assigned_to_name = serializers.CharField(source="assigned_to.full_name", read_only=True)
    created_by_user_name = serializers.CharField(source="created_by_user.full_name", read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "due_date",
            "completed_at",
            "is_overdue",
            "lead",
            "lead_name",
            "assigned_to",
            "assigned_to_name",
            "created_by_user",
            "created_by_user_name",
            "created_at",
            "updated_at",
        ]


class TaskDetailSerializer(serializers.ModelSerializer):
    lead_name = serializers.CharField(source="lead.full_name", read_only=True)
    assigned_to_name = serializers.CharField(source="assigned_to.full_name", read_only=True)
    created_by_user_name = serializers.CharField(source="created_by_user.full_name", read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "due_date",
            "completed_at",
            "is_overdue",
            "lead",
            "lead_name",
            "assigned_to",
            "assigned_to_name",
            "created_by_user",
            "created_by_user_name",
            "created_at",
            "updated_at",
        ]


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "lead",
            "assigned_to",
            "title",
            "description",
            "status",
            "due_date",
        ]
        read_only_fields = ["id"]

    def validate_lead(self, value):
        if not Lead.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Lead not found.")
        return value

    def validate_assigned_to(self, value):
        if value and value.role != "agent":
            raise serializers.ValidationError("Task can only be assigned to an agent.")
        return value

    def create(self, validated_data):
        validated_data["created_by_user"] = self.context["request"].user
        return super().create(validated_data)


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "status",
            "due_date",
            "assigned_to",
        ]

    def validate_assigned_to(self, value):
        if value and value.role != "agent":
            raise serializers.ValidationError("Task can only be assigned to an agent.")
        return value

    def validate(self, attrs):
        status_value = attrs.get("status")
        if status_value == TaskStatus.COMPLETED:
            attrs["completed_at"] = timezone.now()
        return attrs


class TaskCompleteSerializer(serializers.Serializer):
    status = serializers.ChoiceField(
        choices=[TaskStatus.COMPLETED],
        default=TaskStatus.COMPLETED,
    )