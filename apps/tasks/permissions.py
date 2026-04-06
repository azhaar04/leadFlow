from rest_framework.permissions import BasePermission


class IsAdminOrAssignedTaskAgent(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.role == "admin":
            return True

        if request.user.role == "agent" and obj.assigned_to_id == request.user.id:
            return True

        return False