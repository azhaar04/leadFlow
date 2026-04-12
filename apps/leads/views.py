from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Lead, LeadNote
from .permissions import IsAdminOrAssignedAgent
from .serializers import (
    LeadListSerializer,
    LeadDetailSerializer,
    LeadCreateSerializer,
    LeadUpdateSerializer,
    LeadAssignSerializer,
    LeadStatusUpdateSerializer,
    LeadNoteSerializer,
    LeadNoteCreateSerializer,
)
from apps.automation.services import emit_event

class LeadListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == "admin":
            return Lead.objects.select_related("assigned_agent", "created_by").all()

        return Lead.objects.select_related("assigned_agent", "created_by").filter(
            assigned_agent=user
        )

    def get_serializer_class(self):
        if self.request.method == "POST":
            return LeadCreateSerializer
        return LeadListSerializer

    def create(self, request, *args, **kwargs):
        if request.user.role != "admin":
            return Response(
                {"detail": "Only admins can create leads."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().create(request, *args, **kwargs)
    def perform_create(self, serializer):
        lead = serializer.save()

        # trigger automation here
        emit_event(
            trigger_type="new_lead_created",
            lead=lead,
        )


class LeadRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminOrAssignedAgent]

    def get_queryset(self):
        return Lead.objects.select_related(
            "assigned_agent", "created_by"
        ).prefetch_related("notes__user")

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return LeadUpdateSerializer
        return LeadDetailSerializer


class LeadAssignView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        if request.user.role != "admin":
            return Response(
                {"detail": "Only admins can assign leads."},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            lead = Lead.objects.get(pk=pk)
        except Lead.DoesNotExist:
            return Response(
                {"detail": "Lead not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = LeadAssignSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        assigned_agent_id = serializer.validated_data["assigned_agent_id"]
        lead.assigned_agent_id = assigned_agent_id
        lead.save(update_fields=["assigned_agent", "updated_at"])

        return Response(LeadDetailSerializer(lead).data, status=status.HTTP_200_OK)


class LeadStatusUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            lead = Lead.objects.get(pk=pk)
        except Lead.DoesNotExist:
            return Response(
                {"detail": "Lead not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if request.user.role != "admin" and lead.assigned_agent_id != request.user.id:
            return Response(
                {"detail": "You do not have permission to update this lead status."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = LeadStatusUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        old_status = lead.status
        new_status = serializer.validated_data["status"]

        lead.status = new_status
        lead.save(update_fields=["status", "updated_at"])

        # trigger automation only if status actually changed
        if old_status != new_status:
            emit_event(
                trigger_type="lead_status_changed",
                lead=lead,
                context={
                    "old_status": old_status,
                    "new_status": new_status,
                    "status": new_status,
                },
            )

        return Response(LeadDetailSerializer(lead).data, status=status.HTTP_200_OK)


class LeadNoteCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            lead = Lead.objects.get(pk=pk)
        except Lead.DoesNotExist:
            return Response(
                {"detail": "Lead not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if request.user.role != "admin" and lead.assigned_agent_id != request.user.id:
            return Response(
                {"detail": "You do not have permission to add a note to this lead."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = LeadNoteCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        note = LeadNote.objects.create(
            lead=lead,
            user=request.user,
            note=serializer.validated_data["note"],
        )

        return Response(LeadNoteSerializer(note).data, status=status.HTTP_201_CREATED)