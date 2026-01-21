from django.contrib.gis.db import models
from regions.models import adm1


class DisplacementEvent(models.Model):
    DISPLACEMENT_CHOICES = [
        ("Conflict", "Conflict"),
        ("Disaster", "Disaster"),
    ]

    external_id = models.IntegerField(unique=True)  # your id column
    displacement_type = models.CharField(max_length=20, choices=DISPLACEMENT_CHOICES)
    displacement_name = models.CharField(max_length=20, null=True, blank=True)
    figure = models.IntegerField(help_text="Number of displaced persons")
    displacement_date = models.DateField()

    # Geometry (WGS84)
    location = models.PointField(srid=4326, geography=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.displacement_type} – {self.figure} ({self.displacement_date})"


from django.db import models
from regions.models import adm1


# -------------------- Sample data --------------------------#
# Province,Month,Year,Events,Fatalities
# Haut-Uele,January,1997,0,0
# Haut-Uele,February,1997,0,0


class PoliticalViolenceAdm1Monthly(models.Model):
    province = models.ForeignKey(
        adm1, on_delete=models.CASCADE, related_name="monthly_events"
    )
    month = models.PositiveSmallIntegerField()
    year = models.PositiveSmallIntegerField()
    events = models.PositiveIntegerField(default=0)
    fatalities = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["year", "month"]

    def __str__(self):
        return f"{self.province.shapename} - {self.month}/{self.year}"
