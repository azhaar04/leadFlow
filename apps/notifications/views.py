from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Notification
from .serializers import NotificationSerializer


class NotificationListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.select_related("user", "lead", "task").filter(
            user=self.request.user
        )


class NotificationMarkAsReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            notification = Notification.objects.select_related("user").get(pk=pk)
        except Notification.DoesNotExist:
            return Response(
                {"detail": "Notification not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if notification.user_id != request.user.id:
            return Response(
                {"detail": "You do not have permission to modify this notification."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if not notification.is_read:
            notification.is_read = True
            notification.save(update_fields=["is_read"])

        return Response(
            {"detail": "Notification marked as read."},
            status=status.HTTP_200_OK,
        )


class NotificationUnreadCountView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        unread_count = Notification.objects.filter(
            user=request.user,
            is_read=False,
        ).count()

        return Response(
            {"unread_count": unread_count},
            status=status.HTTP_200_OK,
        )