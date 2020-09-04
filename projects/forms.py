from django import forms

from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["title", "description"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "item_title",
            }),
            "description": forms.Textarea(attrs={
                "class": "item_description",
            }),
        }