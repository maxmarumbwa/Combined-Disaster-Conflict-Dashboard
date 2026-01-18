from django.shortcuts import render
from regions.models import adm1


def index(request):
    adm_1 = adm1.objects.all()
    context = {}
    context["adm1"] = adm_1
    return render(request, "index.html", context)


def adm1region(request, shapeiso):
    province = adm1.objects.get(shapeiso=shapeiso)
    context = {}
    context["province"] = province
    print(province)
    return render(request, "provinces.html", context)
