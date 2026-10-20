import csv

# Store the players from the selected team.
team = []

with open("SelectedTeam.csv", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        team.append(row)

# Check that the team file contains players.
if not team:
    print("SelectedTeam.csv is empty.")
    raise SystemExit

# Get the MLB team ID and year from the saved roster.
team_id = team[0]["teamID"]
selected_year = int(team[0]["yearID"])
previous_year = selected_year - 1

# Store batting runs for each player.
batting = {}

with open("Batting.csv", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        player_id = row["playerID"]
        year = int(row["yearID"])
        runs = int(row["R"] or 0)

        if year == previous_year:
            key = (player_id, year)

            if key not in batting:
                batting[key] = 0

            batting[key] += int(runs)

# Calculate the total runs for the selected team.
total_runs = 0

print(f"MLB Team: {team_id}")
print(f"Year: {selected_year}")
print(f"Using batting statistics from: {previous_year}")
print("Player Runs:")

for player in team:
    player_id = player["playerID"]
    key = (player_id, previous_year)
    runs = batting.get(key, 0)

    print(f"{player_id} - {previous_year} - Runs: {runs}")
    total_runs += runs

print(f"Total Runs for {team_id}: {total_runs}")

# Find total runs allowed by the team in the previous year.
previous_runs_allowed = 0
found_previous_year = False

with open("Teams.csv", newline="", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)

    for row in reader:
        if (
            row["teamID"] == team_id
            and int(row["yearID"]) == previous_year
        ):
            previous_runs_allowed = int(row["RA"] or 0)
            found_previous_year = True
            break

if found_previous_year:
    print(
        f"Runs Allowed by {team_id} in {previous_year}: "
        f"{previous_runs_allowed}"
    )
else:
    print(f"No team data found for {team_id} in {previous_year}.")

win_percentage = (total_runs ** 1.83) / ((total_runs ** 1.83) + (previous_runs_allowed ** 1.83))
print(f"Suggested Win Percentage for {team_id} in {selected_year}: {win_percentage:.3f}")
suggested_wins = round(win_percentage * 162)
suggested_losses = 162 - suggested_wins
print(f"Suggested Record: {suggested_wins}-{suggested_losses}")
