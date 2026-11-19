import csv

from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from grouping import make_random_team, calculate_win_loss

def home(request):
    result = request.session.get("team_result")
    error = None
    win_result = request.session.get("win_result")

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
                    request.session.pop("win_result", None)
                else:
                    request.session["win_result"] = win_result
        elif action == "download":
            roster = request.session.get("roster")
            team_result = request.session.get("team_result")
            win_result = request.session.get("win_result")

            if not roster or not team_result:
                error = "Please build a team first."

            elif not win_result:
                error = "Please calculate the winning percentage first."
            
            else:
                response = HttpResponse(content_type="text/csv")
                response["Content-Disposition"] = (
                    'attachment; filename="TeamBalance_Roster.csv"'
                )
                writer = csv.writer(response)

                # Team information
                writer.writerow(["TeamBalance Roster"])
                writer.writerow(["MLB Team", team_result["team_id"]])
                writer.writerow(["Season", team_result["year"]])
                writer.writerow([
                    "Previous Season",
                    win_result["previous_year"]
                ])
                writer.writerow(["Total Team Cost", team_result["total_salary"]])
                writer.writerow(["Total Runs", win_result["total_runs"]])
                writer.writerow(["Runs Allowed", win_result["runs_allowed"]])
                writer.writerow([
                    "Winning Percentage",
                    round(win_result["win_percentage"], 3)
                ])
                writer.writerow(["Suggested Wins", win_result["suggested_wins"]])
                writer.writerow(["Suggested Losses", win_result["suggested_losses"]])
                writer.writerow([
                    "Projected Record",
                    f'{win_result["suggested_wins"]}-'
                    f'{win_result["suggested_losses"]}'
                ])

                writer.writerow([])

                # Player information header
                writer.writerow([
                    "Player ID",
                    "Player Name",
                    "Year",
                    "Position",
                    "Salary",
                    "Previous Season",
                    "Previous Season Runs"
                ])
                
                  # Match previous-season runs to each roster player
                player_runs_lookup = {
                    player["playerID"]: player
                    for player in win_result["player_runs"]
                }

                # Individual player information
                for player in roster:
                    previous_player = player_runs_lookup.get(
                        player["playerID"], {}
                    )

                    writer.writerow([
                        player["playerID"],
                        f'{player["nameFirst"]} {player["nameLast"]}',
                        player["yearID"],
                        player["POS"],
                        player["salary"],
                        win_result["previous_year"],
                        previous_player.get("runs", 0)
                    ])
                
                # Total salary at the bottom
                writer.writerow([])
                writer.writerow(["Total Team Cost", team_result["total_salary"]])

                return response
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

                # Clear old winning percentage results
                request.session.pop("win_result", None)
                win_result = None
    # Restore saved team and results
    result = request.session.get("team_result", result)
    win_result = request.session.get("win_result", win_result)

    return render(request, "roster/home.html", {
        "result": result,
        "error": error,
        "win_result": win_result,
        "has_saved_team": bool(request.session.get("roster"))
    })
