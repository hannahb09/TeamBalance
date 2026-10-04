import csv


salaries = {}
fielding = {}

# Read Salaries.csv
with open("Salaries.csv", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        player_id = row["playerID"]

        salaries[player_id] = {
            "playerID": row["playerID"],
            "yearID": row["yearID"],
            "salary": row["salary"]
        }


# Read Fielding.csv
with open("Fielding.csv", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        player_id = row["playerID"]

        fielding[player_id] = {
            "playerID": row["playerID"],
            "yearID": row["yearID"],
            "teamID": row["teamID"],
            "POS": row["POS"]
        }


# Create the combined file
with open("Combined.csv", "w", newline="", encoding="utf-8") as file:
    fieldnames = [
        "playerID",
        "yearID",
        "teamID",
        "POS",
        "salary"
    ]

    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    # Only keep players found in both files
    for player_id in salaries:

        if player_id in fielding:

            writer.writerow({
               "playerID": player_id,
                "yearID": fielding[player_id]["yearID"],
                "teamID": fielding[player_id]["teamID"],
                "POS": fielding[player_id]["POS"],
                "salary": salaries[player_id]["salary"]
            })


print("Combined.csv created!")