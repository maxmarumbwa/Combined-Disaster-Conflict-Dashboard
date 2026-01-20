from django.contrib import admin

# Register your models here.
from .models import ConflictEvent

admin.site.register(ConflictEvent)
