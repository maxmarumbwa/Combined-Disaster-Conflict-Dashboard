# forms.py
from django import forms
from .models import ConflictEvent


class ConflictEventForm(forms.ModelForm):
    class Meta:
        model = ConflictEvent
        fields = [
            "country",
            "iso3",
            "admin1",
            "admin2_name",
            "admin1_pcode",
            "admin2_pcode",
            "year",
            "month",
            "events",
            "fatalities",
        ]
        widgets = {
            "year": forms.NumberInput(attrs={"min": 1900, "max": 2100}),
            "month": forms.NumberInput(attrs={"min": 1, "max": 12}),
            "events": forms.NumberInput(attrs={"min": 0}),
            "fatalities": forms.NumberInput(attrs={"min": 0}),
        }
