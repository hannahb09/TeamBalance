from django.shortcuts import render
from django.conf import settings
from grouping import make_random_team

def home(request):
    result = None
    error = None

    if request.method == "POST":

        selected_team = request.POST.get("team", "").upper()
        selected_year = request.POST.get("year", "")

        if not selected_team or not selected_year:
            error = "Please enter a team and year."

        else:
            filename = settings.BASE_DIR / "Combined.csv"

            result = make_random_team(
                str(filename),
                selected_team,
                selected_year
            )

    return render(request, "roster/home.html", {
        "result": result,
        "error": error
    })
