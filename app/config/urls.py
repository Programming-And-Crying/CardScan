from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path

from dashboard.views import dashboard, health_live, health_ready

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("login/", LoginView.as_view(template_name="auth/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("", dashboard, name="dashboard"),
    path("dashboard/", dashboard, name="dashboard_page"),
    path("health/live/", health_live, name="health_live"),
    path("health/ready/", health_ready, name="health_ready"),
    path("", include("contacts.urls")),
    path("", include("cards.urls")),
    path("", include("comments.urls")),
    path("", include("history.urls")),
    path("", include("imports.urls")),
    path("", include("accounts.urls")),
    path("", include("access.urls")),
    path("", include("processing.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
