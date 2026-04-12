from django.urls import path
from .views import (
    NotificationListView,
    NotificationMarkAsReadView,
    NotificationUnreadCountView,
)

urlpatterns = [
    path("", NotificationListView.as_view(), name="notification-list"),
    path("unread-count/", NotificationUnreadCountView.as_view(), name="notification-unread-count"),
    path("<int:pk>/read/", NotificationMarkAsReadView.as_view(), name="notification-mark-read"),
]