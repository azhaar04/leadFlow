from django.urls import path
from .views import AdminDashboardView, AgentDashboardView

urlpatterns = [
    path("admin/", AdminDashboardView.as_view(), name="admin-dashboard"),
    path("agent/", AgentDashboardView.as_view(), name="agent-dashboard"),
]