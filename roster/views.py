from django.shortcuts import render
from django.conf import settings
from grouping import make_random_team, calculate_win_loss

def home(request):
    result = None
    error = None
    win_result = None

    if request.method == "POST":
        action = request.POST.get("action", "build")

        if action == "calculate":
            batting_file = settings.BASE_DIR / "Batting.csv"
            teams_file = settings.BASE_DIR / "Teams.csv"

             # Get the roster saved in the session
            roster = request.session.get("roster")

            if not roster:
                error = "Please build a team first."
            else:
                win_result = calculate_win_loss(
                    roster,
                    str(batting_file),
                    str(teams_file)
                )

                if "error" in win_result:
                    error = win_result["error"]
                    win_result = None
        else:
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
                # Save the roster in the session
                request.session["roster"] = result["roster"]
                request.session["team_result"] = result

    return render(request, "roster/home.html", {
        "result": result,
        "error": error,
        "win_result": win_result,
        "has_saved_team": bool(request.session.get("roster"))
    })
