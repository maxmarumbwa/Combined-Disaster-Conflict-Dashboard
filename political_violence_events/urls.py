# urls.py in your app (e.g., political_violence_events/urls.py)
from django.urls import path
from . import views

urlpatterns = [
    path("add-conflict-event/", views.add_conflict_event, name="add_conflict_event"),
]
