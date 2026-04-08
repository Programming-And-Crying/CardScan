from django import forms

from .models import AccessGroup


class AccessGroupForm(forms.ModelForm):
    class Meta:
        model = AccessGroup
        fields = ["name", "slug", "description", "is_active"]
