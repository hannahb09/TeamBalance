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
                "nameFirst": row["nameFirst"],
                "nameLast": row["nameLast"],
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

# Trade deadline for any player in MLB around first Monday of August
month = int(input("Enter the month: "))
day = int(input("Enter the day: "))
year = int(input("Enter the year: "))

print(f"Date: {month}/{day}/{year}")

if (month, day, year) > (8, 2, 2027):
    print("Trade deadline has passed.")

team_id, team = make_random_team("Combined.csv", 9
)

print(f"MLB Team: {team_id}")

# Calculate total salary
total_salary = 0
print("Roster:")

for player in team:
    print(
        f"{player['nameFirst']} {player['nameLast']} - "
        f"{player['yearID']} - "
        f"{player['POS']} - "
        f"{player['salary']}"
    )
    total_salary += int(player["salary"])
print(f"Total Team Cost of {team_id}: {total_salary}")
if total_salary < 171200000:
    print(f"Team has not hit salary floor. Amount remaining: ${171200000 - total_salary:,}")
if total_salary > 245300000:
    print(f"Team has exceeded salary cap. Amount over: ${total_salary - 245300000:,}")