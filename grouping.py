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
                "year": row["yearID"],
                "position": position
            })

    # Find team with enough different positions.
    possible_teams = [
        team_id
        for team_id in teams
        if len(teams[team_id]) >= team_size
    ]

    # Randomly choose a team.
    selected_team = random.choice(possible_teams)

    # Randomly choose different positions.
    positions = list(teams[selected_team].keys())
    random.shuffle(positions)

    team = []

    for position in positions[:team_size]:
        player = random.choice(teams[selected_team][position])
        team.append(player)

    return selected_team, team


team_id, team = make_random_team("Fielding.csv", 9)

print(f"Random Team: {team_id}")

for player in team:
    print(
        f"{player['playerID']} - "
        f"{player['year']} - "
        f"{player['position']}"
    )