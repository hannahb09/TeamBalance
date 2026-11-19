import csv


salaries = {}
fielding = {}
people = {}

# Read Salaries.csv
with open("Salaries.csv", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        player_id = row["playerID"]
        year = row["yearID"]

        salaries[(player_id, year)] = {
            "playerID": row["playerID"],
            "yearID": row["yearID"],
            "salary": row["salary"]
        }


# Read Fielding.csv
with open("Fielding.csv", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        player_id = row["playerID"]
        year = row["yearID"]

        fielding[(player_id, year)] = {
            "playerID": row["playerID"],
            "yearID": row["yearID"],
            "teamID": row["teamID"],
            "POS": row["POS"]
        }

# Read People.csv to get real player names
with open("People.csv", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        player_id = row["playerID"]

        people[player_id] = {
            "nameFirst": row["nameFirst"],
            "nameLast": row["nameLast"]
        }

# Create the combined file
with open("Combined.csv", "w", newline="", encoding="utf-8") as file:
    fieldnames = [
        "playerID",
        "nameFirst",
        "nameLast",
        "yearID",
        "teamID",
        "POS",
        "salary",
    ]

    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    # If no salary found for a player, set salary to 0
    for player_id, year in fielding:
                
            salary = "0"


            if (player_id, year) in salaries:
                salary = salaries[(player_id, year)]["salary"]

            writer.writerow({
                "playerID": player_id,
                "nameFirst": people[player_id]["nameFirst"],
                "nameLast": people[player_id]["nameLast"],
                "yearID": year,
                "teamID": fielding[(player_id, year)]["teamID"],
                "POS": fielding[(player_id, year)]["POS"],
                "salary": salary,
            })


print("Combined.csv created!")