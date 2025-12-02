# attendance/forms.py

from django import forms
from .models import Visitor

class VisitorForm(forms.ModelForm):
    class Meta:
        model = Visitor
        fields = ["name", "title"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "border p-3 w-full rounded"
            }),
            "title": forms.TextInput(attrs={
                "class": "border p-3 w-full rounded"
            }),
        }
