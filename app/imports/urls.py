from django.urls import path

from imports.views import imports_list, imports_run_sample

urlpatterns = [
    path("admin-ui/imports/", imports_list, name="imports_list"),
    path("admin-ui/imports/run-sample/", imports_run_sample, name="imports_run_sample"),
]
