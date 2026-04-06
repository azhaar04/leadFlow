from rest_framework import serializers
from .models import Workflow, WorkflowCondition, WorkflowAction


class WorkflowConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkflowCondition
        fields = ["id", "workflow", "field_name", "operator", "field_value", "created_at"]
        read_only_fields = ["id", "workflow", "created_at"]


class WorkflowActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkflowAction
        fields = [
            "id",
            "workflow",
            "action_type",
            "action_order",
            "config",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "workflow", "created_at", "updated_at"]


class WorkflowListSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source="created_by.full_name", read_only=True)

    class Meta:
        model = Workflow
        fields = [
            "id",
            "name",
            "description",
            "trigger_type",
            "status",
            "created_by",
            "created_by_name",
            "created_at",
            "updated_at",
        ]


class WorkflowDetailSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source="created_by.full_name", read_only=True)
    conditions = WorkflowConditionSerializer(many=True, read_only=True)
    actions = WorkflowActionSerializer(many=True, read_only=True)

    class Meta:
        model = Workflow
        fields = [
            "id",
            "name",
            "description",
            "trigger_type",
            "status",
            "created_by",
            "created_by_name",
            "conditions",
            "actions",
            "created_at",
            "updated_at",
        ]


class WorkflowCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workflow
        fields = ["id", "name", "description", "trigger_type", "status"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)