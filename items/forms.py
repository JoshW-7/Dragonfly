from django import forms

from .models import Item
from users.models import UserProfile


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["title", "description"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "item_title",
            }),
            "description": forms.Textarea(attrs={
                "class": "item_description",
            }),
            "priority": forms.Select(attrs={
                "class": "bootstrap-select",
            })
        }

    priority = forms.CharField(widget=forms.Select(choices=[("", ""), ("low", "Low"), ("medium", "Medium"), ("high", "High")]))
    assigned_to = forms.CharField(widget=forms.Select(
        choices=sorted([
            (user_profile.user.username, user_profile.display_name) for user_profile in UserProfile.objects.all()
        ], key=lambda k: k[1]),
        attrs={
            "style": "min-width: 200px;"
        }
    ))
    tag_bug = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        "class": "tag_checkbox",
    }))
    tag_feature = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        "class": "tag_checkbox",
    }))
    tag_task = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        "class": "tag_checkbox",
    }))