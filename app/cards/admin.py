from django.contrib import admin

from .models import BusinessCard, ChangeHistory, Comment, ImportJob, ImportJobRow, ParsedField, ProcessingTask

admin.site.register(BusinessCard)
admin.site.register(ParsedField)
admin.site.register(Comment)
admin.site.register(ChangeHistory)
admin.site.register(ProcessingTask)
admin.site.register(ImportJob)
admin.site.register(ImportJobRow)
