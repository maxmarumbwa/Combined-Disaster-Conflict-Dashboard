from django.contrib.gis.db import models


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
