from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    lead_id = serializers.IntegerField(source="lead.id", read_only=True)
    lead_name = serializers.CharField(source="lead.full_name", read_only=True)
    task_id = serializers.IntegerField(source="task.id", read_only=True)
    task_title = serializers.CharField(source="task.title", read_only=True)

    class Meta:
        model = Notification
        fields = [
            "id",
            "user_id",
            "lead_id",
            "lead_name",
            "task_id",
            "task_title",
            "type",
            "title",
            "message",
            "is_read",
            "created_at",
        ]