from django.contrib.gis.db import models
from django.contrib.gis.db import models


class adm1(models.Model):
    shapename = models.CharField(max_length=110, null=True)
    shapeiso = models.CharField(max_length=50, null=True)
    shapeid = models.CharField(max_length=100, null=True)
    shapegroup = models.CharField(max_length=100, null=True)
    shapetype = models.CharField(max_length=100, null=True)
    shapename2 = models.CharField(max_length=110, null=True)
    geom = models.GeometryField()

    def __str__(self):
        return self.shapename

    class Meta:
        ordering = ["shapename"]
