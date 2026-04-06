from django.urls import path
from .views import (
    WorkflowListCreateView,
    WorkflowRetrieveUpdateView,
    WorkflowActivateView,
    WorkflowDeactivateView,
    WorkflowConditionCreateView,
    WorkflowActionCreateView,
)

urlpatterns = [
    path("", WorkflowListCreateView.as_view(), name="workflow-list-create"),
    path("<int:pk>/", WorkflowRetrieveUpdateView.as_view(), name="workflow-detail-update"),
    path("<int:pk>/activate/", WorkflowActivateView.as_view(), name="workflow-activate"),
    path("<int:pk>/deactivate/", WorkflowDeactivateView.as_view(), name="workflow-deactivate"),
    path("<int:pk>/conditions/", WorkflowConditionCreateView.as_view(), name="workflow-condition-create"),
    path("<int:pk>/actions/", WorkflowActionCreateView.as_view(), name="workflow-action-create"),
]