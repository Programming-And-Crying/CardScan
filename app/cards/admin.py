from django.contrib import admin
from cards.models import BusinessCard, ParsedField
admin.site.register([BusinessCard, ParsedField])
