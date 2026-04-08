from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from dashboard.views import dashboard_view, live_health_view, ready_health_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("", dashboard_view, name="home"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("contacts/", include("contacts.urls")),
    path("cards/", include("cards.urls")),
    path("admin-ui/groups/", include("access.urls")),
    path("health/live/", live_health_view, name="health-live"),
    path("health/ready/", ready_health_view, name="health-ready"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
