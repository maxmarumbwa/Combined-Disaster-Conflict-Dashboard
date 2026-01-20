# views.py
from django.shortcuts import render, redirect
from .forms import ConflictEventForm


def add_conflict_event(request):
    success = False  # flag to show message on the same page
    if request.method == "POST":
        form = ConflictEventForm(request.POST)
        if form.is_valid():
            form.save()
            success = True  # form saved successfully
            form = ConflictEventForm()  # reset the form
    else:
        form = ConflictEventForm()

    return render(
        request, "add_conflict_event.html", {"form": form, "success": success}
    )
