from django.db import models


class ConflictEvent(models.Model):
    country = models.CharField(max_length=100)
    iso3 = models.CharField(max_length=3)

    admin1 = models.ForeignKey(
        "regions.adm1",
        on_delete=models.CASCADE,
        related_name="events",
        null=True,
        blank=True,
    )

    admin2_name = models.CharField(max_length=110)
    admin1_pcode = models.CharField(max_length=20)
    admin2_pcode = models.CharField(max_length=20)

    year = models.PositiveIntegerField()
    month = models.PositiveSmallIntegerField()  # 1–12

    events = models.PositiveIntegerField(default=0)
    fatalities = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("admin1", "year", "month", "events", "fatalities")
        ordering = ["year", "month"]

    def __str__(self):
        return f"{self.admin1} - {self.year}-{self.month}"
