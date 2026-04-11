from django.urls import path
from .views import WorkflowRunListView, WorkflowRunDetailView

urlpatterns = [
    path("runs/", WorkflowRunListView.as_view(), name="workflow-run-list"),
    path("runs/<int:pk>/", WorkflowRunDetailView.as_view(), name="workflow-run-detail"),
]