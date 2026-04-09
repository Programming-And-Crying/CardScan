from django.contrib import admin
from imports.models import ImportJob, ImportJobRow
admin.site.register([ImportJob, ImportJobRow])
