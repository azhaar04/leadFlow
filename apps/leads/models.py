from django.conf import settings
from django.db import models


class LeadStatus(models.TextChoices):
    NEW = "new", "New"
    CONTACTED = "contacted", "Contacted"
    QUALIFIED = "qualified", "Qualified"
    WON = "won", "Won"
    LOST = "lost", "Lost"


class Lead(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    source = models.CharField(max_length=100, blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=LeadStatus.choices,
        default=LeadStatus.NEW,
    )

    assigned_agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_leads",
        limit_choices_to={"role": "agent"},
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_leads",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "leads"
        ordering = ["-created_at"]

    def __str__(self):
        return self.full_name


class LeadNote(models.Model):
    lead = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        related_name="notes",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="lead_notes",
    )
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "lead_notes"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Note by {self.user.email} on {self.lead.full_name}"