import json
import csv
from io import TextIOWrapper
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.gis.geos import Point
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import DisplacementEvent
from .forms import DisplacementEventForm
from .forms import CSVUploadForm
from conflict.models import PoliticalViolenceAdm1Monthly
from regions.models import adm1
from .forms import PoliticalViolenceUploadForm, PoliticalViolenceManualForm


# View to render the choropleth page with filters
def a():
    # Distinct years from database
    years = (
        PoliticalViolenceAdm1Monthly.objects.values_list("year", flat=True)
        .distinct()
        .order_by("year")
    )


a()
