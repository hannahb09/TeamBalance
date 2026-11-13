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
    

# Save team as a CSV file.
# with open("SelectedTeam.csv", "w" newline="", encoding="utf-8") as file:
#     fieldnames = ["teamID", "playerID", "yearID", "POS", "salary"]
#     writer = csv.DictWriter(file, fieldnames=fieldnames)

#     writer.writeheader()

#     for player in team:
#         writer.writerow({
#             "teamID": team_id,
#             "playerID": player["playerID"],
#             "yearID": player.get("yearID", ""),
#             "POS": player["POS"],
#             "salary": player["salary"]
#         })

# print("Team saved to SelectedTeam.csv!")