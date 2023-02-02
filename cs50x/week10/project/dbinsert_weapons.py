import csv
import cs50


db = cs50.SQL("sqlite:///artifact.db")
db.execute("CREATE TABLE IF NOT EXISTS weapons(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT NOT NULL, type TEXT NOT NULL, base NUMERICAL NOT NULL, mainstat TEXT NOT NULL, mainvalue NUMERICAL NOT NULL, substat TEXT NOT NULL, subvalue NUMERICAL NOT NULL)")


with open ("weapons.csv", "r") as file:

    reader = csv.DictReader(file)
    for row in reader:
        id = row['id']
        name = row['name']
        base = row['base']
        type = row['type']
        mainstat = row['mainstat']
        mainvalue = row['mainvalue']
        substat = row['substat']
        subvalue = row['subvalue']

        db.execute("INSERT INTO weapons (id, name, type, base, mainstat, mainvalue, substat, subvalue) VALUES(:id, :name, :type, :base, :mainstat, :mainvalue, :substat, :subvalue);", id=id, name=name, type=type, base=base, mainstat=mainstat, mainvalue=mainvalue, substat=substat, subvalue=subvalue)

