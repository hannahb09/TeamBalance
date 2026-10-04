import csv
import random


def make_random_team(filename, team_size):
    teams = {}

    with open(filename, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            team_id = row["teamID"]
            position = row["POS"]

            if team_id not in teams:
                teams[team_id] = {}

            if position not in teams[team_id]:
                teams[team_id][position] = []

            teams[team_id][position].append({
                "playerID": row["playerID"],
                "yearID": row["yearID"],
                "POS": position,
                "salary": row["salary"]
            })

    # Choose a team.
    selected_team = input("Enter the MLB team ID: ")

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

    for position in required_positions:
        if position in teams[selected_team]:
            player = random.choice(teams[selected_team][position])
            team.append(player)
    return selected_team, team


team_id, team = make_random_team("Combined.csv", 9)

print(f"MLB Team: {team_id}")

# Calculate total salary
total_salary = 0
print("Roster:")

for player in team:
    print(
        f"{player['playerID']} - "
        f"{player['yearID']} - "
        f"{player['POS']} - "
        f"{player['salary']}"
    )
    total_salary += int(player["salary"])
print(f"Total Team Cost of {team_id}: {total_salary}")
    