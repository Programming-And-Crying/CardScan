from django.urls import path

from processing.views import system_status, tasks_list

urlpatterns = [
    path("admin-ui/tasks/", tasks_list, name="tasks_list"),
    path("admin-ui/system/", system_status, name="system_status"),
]
