from django.contrib import admin
from django.urls import path
from regions import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("home/", views.index),
    path("home/<str:shapeiso>/", views.adm1region),
]
