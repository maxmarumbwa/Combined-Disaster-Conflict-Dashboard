# View to render the choropleth page with filters
def political_violence_choropleth_page(request):
    # Distinct years from database
    years = (
        PoliticalViolenceAdm1Monthly.objects.values_list("year", flat=True)
        .distinct()
        .order_by("year")
    )
    print("Available years for filtering:", list(years))

    # Month choices (value, label)
    months = [
        (1, "January"),
        (2, "February"),
        (3, "March"),
        (4, "April"),
        (5, "May"),
        (6, "June"),
        (7, "July"),
        (8, "August"),
        (9, "September"),
        (10, "October"),
        (11, "November"),
        (12, "December"),
    ]

    # Indicators
    indicators = [
        ("fatalities", "Fatalities"),
        ("events", "Events"),
    ]

    context = {
        "years": years,
        "months": months,
        "indicators": indicators,
    }

    return render(
        request,
        "conflict/api_based/api_fatalities_choropleth.html",
        context,
    )
