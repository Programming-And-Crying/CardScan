from django import forms

from accounts.models import User
from access.models import AccessGroup


class UserAdminForm(forms.ModelForm):
    access_groups = forms.ModelMultipleChoiceField(queryset=AccessGroup.objects.all(), required=False)

    class Meta:
        model = User
        fields = ["username", "email", "role", "is_active", "access_groups"]
