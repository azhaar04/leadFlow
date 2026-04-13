from django.urls import path
from .views import WorkflowRunListView, WorkflowRunDetailView, WorkflowRunLogsView

urlpatterns = [
    path("runs/", WorkflowRunListView.as_view(), name="workflow-run-list"),
    path("runs/<int:pk>/", WorkflowRunDetailView.as_view(), name="workflow-run-detail"),
    path("runs/<int:pk>/logs/", WorkflowRunLogsView.as_view(), name="workflow-run-logs"),
]