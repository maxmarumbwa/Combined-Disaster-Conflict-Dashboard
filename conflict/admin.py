from django.contrib import admin

# Register your models here.
from .models import DisplacementEvent, PoliticalViolenceAdm1Monthly

admin.site.register(DisplacementEvent)
admin.site.register(PoliticalViolenceAdm1Monthly)
