from django import forms
from .models import DisplacementEvent
from django.contrib.gis.geos import Point


class DisplacementEventForm(forms.ModelForm):
    latitude = forms.FloatField(label="Latitude")
    longitude = forms.FloatField(label="Longitude")

    class Meta:
        model = DisplacementEvent
        fields = [
            "external_id",
            "displacement_type",
            "displacement_name",
            "figure",
            "displacement_date",
        ]

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Create Point from latitude and longitude
        lat = self.cleaned_data.get("latitude")
        lon = self.cleaned_data.get("longitude")
        instance.location = Point(lon, lat)  # Note: Point(lon, lat)
        if commit:
            instance.save()
        return instance
