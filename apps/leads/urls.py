from django.urls import path
from .views import (
    LeadListCreateView,
    LeadRetrieveUpdateView,
    LeadAssignView,
    LeadStatusUpdateView,
    LeadNoteCreateView,
)

urlpatterns = [
    path("", LeadListCreateView.as_view(), name="lead-list-create"),
    path("<int:pk>/", LeadRetrieveUpdateView.as_view(), name="lead-detail-update"),
    path("<int:pk>/assign/", LeadAssignView.as_view(), name="lead-assign"),
    path("<int:pk>/change-status/", LeadStatusUpdateView.as_view(), name="lead-change-status"),
    path("<int:pk>/notes/", LeadNoteCreateView.as_view(), name="lead-add-note"),
]