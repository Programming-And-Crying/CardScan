from django import forms

from cards.models import BusinessCard


class CardUploadForm(forms.ModelForm):
    class Meta:
        model = BusinessCard
        fields = ["contact", "original_file"]
        widgets = {
            "original_file": forms.ClearableFileInput(
                attrs={"accept": "image/jpeg,image/png,image/webp", "capture": "environment"}
            )
        }

    def clean_original_file(self):
        f = self.cleaned_data["original_file"]
        allowed = {"image/jpeg", "image/png", "image/webp"}
        if f.content_type not in allowed:
            raise forms.ValidationError("Only JPEG/PNG/WEBP images are supported in MVP upload.")
        if f.size > 15 * 1024 * 1024:
            raise forms.ValidationError("File too large (max 15MB).")
        return f


class CardReviewForm(forms.ModelForm):
    class Meta:
        model = BusinessCard
        fields = ["contact", "needs_manual_review", "human_verified", "parsed_text"]
