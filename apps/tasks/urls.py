from django.urls import path
from .views import (
    TaskListCreateView,
    TaskRetrieveUpdateView,
    TaskCompleteView,
)

urlpatterns = [
    path("", TaskListCreateView.as_view(), name="task-list-create"),
    path("<int:pk>/", TaskRetrieveUpdateView.as_view(), name="task-detail-update"),
    path("<int:pk>/complete/", TaskCompleteView.as_view(), name="task-complete"),
]