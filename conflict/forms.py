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


from django import forms
from conflict.models import PoliticalViolenceAdm1Monthly
from regions.models import adm1


### manual entry form for political violence data ###
class PoliticalViolenceManualForm(forms.Form):
    province = forms.ModelChoiceField(
        queryset=adm1.objects.all().order_by("shapename2"), label="Province"
    )

    month = forms.ChoiceField(
        choices=[
            (1, "January"),
            (2, "February"),
            (3, "March"),
            (4, "April"),
            (5, "May"),
            (6, "June"),
            (7, "July"),
            (8, "August"),
            (9, "September"),
            (10, "October"),
            (11, "November"),
            (12, "December"),
        ]
    )

    year = forms.IntegerField(min_value=1900, max_value=2100)
    events = forms.IntegerField(min_value=0)
    fatalities = forms.IntegerField(min_value=0)
