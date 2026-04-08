from django import forms

from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            "full_name",
            "first_name",
            "last_name",
            "middle_name",
            "company",
            "position",
            "notes",
            "access_groups",
        ]
