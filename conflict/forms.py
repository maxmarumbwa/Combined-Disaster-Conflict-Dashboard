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


class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(label="Upload CSV file")


from django import forms


### upload monthly political violence data via csv file ###
class PoliticalViolenceUploadForm(forms.Form):
    csv_file = forms.FileField(
        label="Select a CSV file",
        help_text="Upload a CSV with Province, Month, Year, Events, Fatalities",
    )
    reset = forms.BooleanField(
        required=False,
        label="Reset table before import",
        help_text="Delete all existing records before import",
    )
