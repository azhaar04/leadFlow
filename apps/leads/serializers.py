from rest_framework import serializers
from apps.accounts.models import User
from .models import Lead, LeadNote


class LeadNoteSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    user_name = serializers.CharField(source="user.full_name", read_only=True)

    class Meta:
        model = LeadNote
        fields = ["id", "lead", "user_id", "user_name", "note", "created_at"]
        read_only_fields = ["id", "lead", "user_id", "user_name", "created_at"]


class LeadListSerializer(serializers.ModelSerializer):
    assigned_agent_name = serializers.CharField(source="assigned_agent.full_name", read_only=True)
    created_by_name = serializers.CharField(source="created_by.full_name", read_only=True)

    class Meta:
        model = Lead
        fields = [
            "id",
            "full_name",
            "email",
            "phone",
            "company_name",
            "source",
            "status",
            "assigned_agent",
            "assigned_agent_name",
            "created_by",
            "created_by_name",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_by", "created_at", "updated_at"]


class LeadDetailSerializer(serializers.ModelSerializer):
    assigned_agent_name = serializers.CharField(source="assigned_agent.full_name", read_only=True)
    created_by_name = serializers.CharField(source="created_by.full_name", read_only=True)
    notes = LeadNoteSerializer(many=True, read_only=True)

    class Meta:
        model = Lead
        fields = [
            "id",
            "full_name",
            "email",
            "phone",
            "company_name",
            "source",
            "status",
            "assigned_agent",
            "assigned_agent_name",
            "created_by",
            "created_by_name",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_by", "created_at", "updated_at"]


class LeadCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = [
            "id",
            "full_name",
            "email",
            "phone",
            "company_name",
            "source",
            "status",
            "assigned_agent",
        ]
        read_only_fields = ["id"]

    def validate_assigned_agent(self, value):
        if value and value.role != "agent":
            raise serializers.ValidationError("Assigned user must be an agent.")
        return value

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)


class LeadUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = [
            "full_name",
            "email",
            "phone",
            "company_name",
            "source",
            "status",
            "assigned_agent",
        ]

    def validate_assigned_agent(self, value):
        if value and value.role != "agent":
            raise serializers.ValidationError("Assigned user must be an agent.")
        return value


class LeadAssignSerializer(serializers.Serializer):
    assigned_agent_id = serializers.IntegerField()

    def validate_assigned_agent_id(self, value):
        try:
            user = User.objects.get(id=value, role="agent", is_active=True)
        except User.DoesNotExist:
            raise serializers.ValidationError("Valid active agent not found.")
        return value


class LeadStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Lead._meta.get_field("status").choices)


class LeadNoteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadNote
        fields = ["id", "note"]
        read_only_fields = ["id"]