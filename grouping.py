import csv
import random


def make_random_team(filename, selected_team, selected_year):
    teams = {}

    with open(filename, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            team_id = row["teamID"]
            position = row["POS"]
            yearID = row["yearID"]

            if team_id not in teams:
                teams[team_id] = {}

            if yearID not in teams[team_id]:
                teams[team_id][yearID] = {}

            if position not in teams[team_id][yearID]:
                teams[team_id][yearID][position] = []

            teams[team_id][yearID][position].append({
                "teamID": team_id,
                "playerID": row["playerID"],
                "nameFirst": row["nameFirst"],
                "nameLast": row["nameLast"],
                "yearID": row["yearID"],
                "POS": position,
                "salary": row["salary"]
            })

    # Requried positions need for team
    required_positions = [
        "P",
        "C",
        "1B",
        "2B",
        "3B",
        "SS",
        "OF",
        "OF",
        "OF"
    ]

    team = []
    selected_players = set()
    missing_positions = []

    for position in required_positions:
        available_players = [
            player
            for player in teams.get(selected_team, {}).get(selected_year, {}).get(position, [])
            if player["playerID"] not in selected_players
        ]
        if available_players:
            player = random.choice(available_players)
            team.append(player)
            selected_players.add(player["playerID"])
        else:
            missing_positions.append(position)

# Calculate total salary
    total_salary = sum(
        int(player["salary"] or 0)
        for player in team
    )

    # Salary floor and cap
    salary_floor = 171200000
    salary_cap = 245300000

    amount_remaining = max(0, salary_floor - total_salary)
    amount_over = max(0, total_salary - salary_cap)

    return {
        "team_id": selected_team,
        "year": selected_year,
        "roster": team,
        "total_salary": total_salary,
        "amount_remaining": amount_remaining,
        "amount_over": amount_over,
        "missing_positions": missing_positions
    }


def calculate_win_loss(roster, batting_file, teams_file):

    if not roster:
        return {"error": "Please build a team first."}

    team_id = roster[0]["teamID"]
    selected_year = int(roster[0]["yearID"])
    previous_year = selected_year - 1
    batting = {}

    with open(batting_file, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            player_id = row["playerID"]
            year = int(row["yearID"])
            runs = int(row["R"] or 0)

            if year == previous_year:
                key = (player_id, year)

                if key not in batting:
                    batting[key] = 0

                batting[key] += runs

    total_runs = 0
    player_runs = []

    for player in roster:
        player_id = player["playerID"]
        key = (player_id, previous_year)
        runs = batting.get(key, 0)

        player_runs.append({
            "playerID": player_id,
            "year": previous_year,
            "runs": runs
        })

        total_runs += runs

    previous_runs_allowed = 0
    found_previous_year = False

    with open(teams_file, newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if (
                row["teamID"] == team_id
                and int(row["yearID"]) == previous_year
            ):
                previous_runs_allowed = int(row["RA"] or 0)
                found_previous_year = True
                break

    if not found_previous_year:
        return {"error": f"No team data found for {team_id} in {previous_year}."}

    denominator = total_runs ** 1.83 + previous_runs_allowed ** 1.83

    if denominator == 0:
        return {"error": "Cannot calculate winning percentage."}

    win_percentage = (total_runs ** 1.83) / denominator

    suggested_wins = round(win_percentage * 162)
    suggested_losses = 162 - suggested_wins

    return {
        "team_id": team_id,
        "year": selected_year,
        "previous_year": previous_year,
        "player_runs": player_runs,
        "total_runs": total_runs,
        "runs_allowed": previous_runs_allowed,
        "win_percentage": win_percentage,
        "suggested_wins": suggested_wins,
        "suggested_losses": suggested_losses
    }
