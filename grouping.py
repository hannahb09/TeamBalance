import csv
import random


def make_random_team(filename, team_size):
    teams = {}

    with open(filename, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            team_id = row["teamID"]
            position = row["POS"]
            year = row["yearID"]

            if team_id not in teams:
                teams[team_id] = {}

            if year not in teams[team_id]:
                teams[team_id][year] = {}

            if position not in teams[team_id]:
                teams[team_id][year][position] = []

            teams[team_id][year][position].append({
                "playerID": row["playerID"],
                "nameFirst": row["nameFirst"],
                "nameLast": row["nameLast"],
                "year": row["yearID"],
                "POS": position,
                "salary": row["salary"]
            })

    # Choose a team.
    selected_team = input("Enter the MLB team ID: ")
    selected_year = input("Enter the year: ")

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
        if position in teams[selected_team][selected_year]:
            player = random.choice(teams[selected_team][selected_year][position])
            team.append(player)
    return selected_team, team, selected_year

# Trade deadline for any player in MLB around first Monday of August
# month = int(input("Enter the month: "))
# day = int(input("Enter the day: "))
# year = int(input("Enter the year: "))

# print(f"Date: {month}/{day}/{year}")

# if (year, day, month) >= (2027, 2, 8):
#     print("Trade deadline has passed.")

team_id, team, selected_year = make_random_team("Combined.csv", 9
)

print(f"MLB Team: {team_id}")
print(f"Year: {selected_year}")

# Calculate total salary
total_salary = 0
print("Roster:")

for player in team:
    print(
        f"{player['playerID']} - "
        f"{player['nameFirst']} {player['nameLast']} - "
        f"{player['year']} - "
        f"{player['POS']} - "
        f"{player['salary']}"
    )
    total_salary += int(player["salary"])
print(f"Total Team Cost of {team_id}: {total_salary}")

if total_salary < 171200000:
    print(f"Team has not hit salary floor. Amount remaining: ${171200000 - total_salary:,}")
    add_player = input("Would you like to add another player? (yes/no): ").lower()
    if add_player == "yes":
        position = input("Enter the position you want (P, C, 1B, 2B, 3B, SS, OF): ").upper()

    with open("Combined.csv", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        available_players = [
            row for row in reader
            if row["teamID"] == team_id
            and row["POS"] == position
            and row["salary"].isdigit()
            and row["playerID"] not in [
            player["nameFirst"] == row["nameFirst"]
            and player["nameLast"] == row["nameLast"]
        for player in team
            ]
        ]

    if available_players:
        player = random.choice(available_players)

        team.append({
            "playerID": player["playerID"],
            "nameFirst": player["nameFirst"],
            "nameLast": player["nameLast"],
            "yearID": player["yearID"],
            "POS": player["POS"],
            "salary": player["salary"]
        })

        total_salary += int(player["salary"])

        print(f"Added: {player['nameFirst']} {player['nameLast']} - {position} - ${int(player['salary']):,}")
        print(f"New Total Team Cost: ${total_salary:,}")
    else:
        print("No additional players found at that position.")
        

if total_salary > 245300000:
    print(f"Team has exceeded salary cap. Amount over: ${total_salary - 245300000:,}")

# Save team as a CSV file.
with open("SelectedTeam.csv", "w", newline="", encoding="utf-8") as file:
    fieldnames = ["playerID","year", "POS", "salary"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()

    for player in team:
        writer.writerow({
            "playerID": player["playerID"],
            "year": player.get("year", player.get("yearID", "")),
            "POS": player["POS"],
            "salary": player["salary"]
        })

print("Team saved to SelectedTeam.csv!")