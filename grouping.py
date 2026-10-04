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

    # Find team with enough different positions.
    possible_teams = [
        team_id
        for team_id in teams
        if len(teams[team_id]) >= team_size
    ]

    # Randomly choose a team.
    selected_team = input("Enter the team ID: ")

    # Randomly choose different positions.
    positions = list(teams[selected_team].keys())
    random.shuffle(positions)

    team = []

    for position in positions[:team_size]:
        player = random.choice(teams[selected_team][position])
        team.append(player)

    return selected_team, team


team_id, team = make_random_team("Combined.csv", 9)

print(f"Team: {team_id}")

# Calculate total salary
total_salary = 0

for player in team:
    print(
        f"{player['playerID']} - "
        f"{player['yearID']} - "
        f"{player['POS']} - "
        f"{player['salary']}"
    )
    total_salary += int(player["salary"])
print(f"Total Salary: {total_salary}")
    