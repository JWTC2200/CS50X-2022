import csv
import cs50


db = cs50.SQL("sqlite:///artifact.db")
db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL)")
db.execute("CREATE TABLE IF NOT EXISTS artifacts(Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, user INTEGER NOT NULL, artset TEXT NOT NULL, slot TEXT NOT NULL, mainstat TEXT NOT NULL, mainvalue TEXT NOT NULL, hpf NUMERIC NOT NULL DEFAULT 0.00, hpp NUMERIC NOT NULL DEFAULT 0.00, deff NUMERIC NOT NULL DEFAULT 0.00, defp NUMERIC NOT NULL DEFAULT 0.00, attk NUMERIC NOT NULL DEFAULT 0.00, attkp NUMERIC NOT NULL DEFAULT 0.00, crtt NUMERIC NOT NULL DEFAULT 0.00, crdd NUMERIC NOT NULL DEFAULT 0.00, em NUMERIC NOT NULL DEFAULT 0.00, er NUMERIC NOT NULL DEFAULT 0.00)")

titles = ["Id", "user", "artset", "slot", "mainstat", "mainvalue", "hpf", "attk", "attkp", "deff", "defp", "crtt", "crdd", "em", "er"]


with open ("testcsv.csv", "r") as file:

    reader = csv.DictReader(file)
    for row in reader:
        id = row["Id"]
        user = row["user"]
        artset = row["artset"]
        slot = row["slot"]
        mainstat = row["mainstat"]
        mainvalue = row["mainvalue"]
        hpf = row["hpf"]
        hpp = row["hpp"]
        attk = row["attk"]
        attkp = row["attkp"]
        deff = row["deff"]
        defp = row["defp"]
        crtt = row["crtt"]
        crdd = row["crdd"]
        em = row["em"]
        er = row["er"]
        db.execute("INSERT INTO artifacts (user, artset, slot, mainstat, mainvalue, hpf, hpp, deff, defp, attk, attkp, crtt, crdd, em, er) VALUES(:user, :artset, :slot, :main, :mainvalue, :hpf, :hpp, :deff, :defp, :attk, :attkp, :crtt, :crdd, :em, :er);", user=user, artset=artset, slot=slot, main=mainstat, mainvalue=mainvalue, hpf=hpf, hpp=hpp,
        deff=deff, defp=defp, attk=attk, attkp=attkp, crtt=crtt, crdd=crdd, em=em, er=er)

