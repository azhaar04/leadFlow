from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin panel
    path("admin/", admin.site.urls),

    # API v1
    path("api/v1/auth/", include("apps.accounts.urls")),
    path("api/v1/leads/", include("apps.leads.urls")),
    path("api/v1/workflows/", include("apps.workflows.urls")),
    path("api/v1/tasks/", include("apps.tasks.urls")),
    path("api/v1/notifications/", include("apps.notifications.urls")),
]