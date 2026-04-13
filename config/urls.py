from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin panel
    path("admin/", admin.site.urls),

    # API v1
    path("api/auth/", include("apps.accounts.urls")),
    path("api/leads/", include("apps.leads.urls")),
    path("api/workflows/", include("apps.workflows.urls")),
    path("api/tasks/", include("apps.tasks.urls")),
    path("api/notifications/", include("apps.notifications.urls")),
    path("api/automation/", include("apps.automation.urls")),
    path("api/dashboard/", include("apps.dashboard.urls")),
]