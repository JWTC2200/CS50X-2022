import csv
import cs50

db = cs50.SQL("sqlite:///artifact.db")

db.execute("CREATE TABLE IF NOT EXISTS char_yae(id INTEGER PRIMARY KEY NOT NULL, level INTEGER NOT NULL, health NUMERIC NOT NULL, attack NUMERIC NOT NULL, defence NUMERIC NOT NULL, critrate NUMERIC NOT NULL, critdam NUMERIC NOT NULL, type TEXT NOT NULL, bonus NUMERIC NOT NULL)")

with open ("char_yae.csv", "r") as file:

    reader = csv.DictReader(file)
    for row in reader:
        id = row["Id"]
        level = row["Level"]
        health = row["Health"]
        attack = row["Attack"]
        defence = row["Defence"]
        critrate = row["Crit Rate"]
        critdam = row["Crit Damage"]
        type = row["Type"]
        bonus = row["Bonus"]
        db.execute("INSERT INTO char_yae (id, level, health, attack, defence, critrate, critdam, type, bonus) VALUES(:id, :level, :health, :attack, :defence, :critrate, :critdam, :type, :bonus);", id=id, level=level, health=health, attack=attack, defence=defence, critrate=critrate, critdam=critdam, type=type, bonus=bonus)