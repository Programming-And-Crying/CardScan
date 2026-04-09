from django.contrib import admin
from contacts.models import Contact, ContactAlias, ContactPhone, ContactEmail, ContactWebsite, ContactAddress
admin.site.register([Contact, ContactAlias, ContactPhone, ContactEmail, ContactWebsite, ContactAddress])
