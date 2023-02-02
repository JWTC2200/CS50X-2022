import os
import json

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from helpers import login_required, apology, isfloat
from cs50 import SQL


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///artifact.db")

# Create users and artifacts table in database if not already exists
db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL)")
db.execute("CREATE TABLE IF NOT EXISTS artifacts(Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, user INTEGER NOT NULL, artset TEXT NOT NULL, slot TEXT NOT NULL, mainstat TEXT NOT NULL, mainvalue TEXT NOT NULL, hpf NUMERIC NOT NULL DEFAULT 0.00, hpp NUMERIC NOT NULL DEFAULT 0.00, deff NUMERIC NOT NULL DEFAULT 0.00, defp NUMERIC NOT NULL DEFAULT 0.00, attk NUMERIC NOT NULL DEFAULT 0.00, attkp NUMERIC NOT NULL DEFAULT 0.00, crtt NUMERIC NOT NULL DEFAULT 0.00, crdd NUMERIC NOT NULL DEFAULT 0.00, em NUMERIC NOT NULL DEFAULT 0.00, er NUMERIC NOT NULL DEFAULT 0.00)")

# list of supported artifacts
supported_artifact_sets = [
    "Gladiators", "Wanderers", "Emblem", "Shimenawa"
]

@app.route("/")
@login_required
def index():

    user = session["user_id"]

    index = []
    sub_index = []

    sub_dict = {
        "Health": "hpf",
        "Health%": "hpp",
        "Attack": "attk",
        "Attack%": "attkp",
        "Defence": "deff",
        "Defence%": "defp",
        "Crit Rate": "crtt",
        "Crit Damage": "crdd",
        "Elemental Mastery": "em",
        "Energy Recharge": "er",
    }

    raw_index = db.execute("SELECT * FROM artifacts WHERE user = :user ORDER BY Id DESC LIMIT 5 ", user=user)

    for raw in raw_index:
        sub_index.clear()
        for sub in sub_dict:
            if raw[sub_dict[sub]] != 0.0:
                sub_value = raw[sub_dict[sub]]
                sub_index.append([sub, sub_value])
        index.append({"Set": raw["artset"], "Slot": raw["slot"], "Main Stat": raw["mainstat"], "Main Value": raw["mainvalue"], "Sub1": sub_index[0], "Sub2": sub_index[1], "Sub3": sub_index[2], "Sub4": sub_index[3]})

    return render_template("layout.html", index=index, supported_artifact_sets=supported_artifact_sets)



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Clear any user_id
    session.clear()

    # User post details
    # Check username exists then match password
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return render_template("login.html", value="Please enter username")
        if not password:
            return render_template("login.html", value="Please enter password")
        check = db.execute("SELECT * FROM users WHERE username = :username", username=username)
        if len(check) != 1 or not check_password_hash(check[0]["hash"], password):
            return render_template("login.html", value="Invalid username and/or password")

        session["user_id"] = check[0]["id"]

        return redirect("/")

    # User used GET
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    # On submission of username and password
    # Check unique username
    # Minimum password length
    # Check passwords match
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        if not username:
            return render_template("register.html", value="Please enter username")
        if not password:
            return render_template("register.html", value="Please enter password")
        if len(password) < 5:
            return render_template("register.html", value="Password too short")
        if not confirm:
            return render_template("register.html", value="Please confirm password")
        if password != confirm:
            return render_template("register.html", value="Passwords do not match")
        # Checks passed. Generate hash and store values
        hash = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", username=username, hash=hash)

        return redirect("/login")


    else:
        return render_template("register.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/submit", methods=["GET", "POST"])
@login_required
def submit():

    user = session["user_id"]

    if request.method == "POST":
        slot = request.form.get("slot")
        mainstat = request.form.get("mainstat")
        substat1 = request.form.get("substat1")
        substat2 = request.form.get("substat2")
        substat3 = request.form.get("substat3")
        substat4 = request.form.get("substat4")
        mainstat_v = request.form.get("mainstat_value")
        substat1_v = request.form.get("substat1-value")
        substat2_v = request.form.get("substat2-value")
        substat3_v = request.form.get("substat3-value")
        substat4_v = request.form.get("substat4-value")
        artset = request.form.get("sets")

        # Dict to hold set main stat values
        main_stat = {
            "Health": 4780,
            "Health%": 46.6,
            "Attack": 311,
            "Attack%": 46.6,
            "Defence%": 58.3,
            "Elemental Mastery": 186.5,
            "Energy Recharge": 51.8,
            "Crit Rate": 31.1,
            "Crit Damage": 62.2,
            "Healing Bonus": 35.9,
        }

        # Dict to pair substat values
        sub_stat = {
            substat1: substat1_v,
            substat2: substat2_v,
            substat3: substat3_v,
            substat4: substat4_v
        }

        # base values for all possible stats before db entry
        main = mainstat
        hpf = 0.0
        hpp = 0.0
        deff = 0.0
        defp = 0.0
        attk = 0.0
        attkp = 0.0
        crtt = 0.0
        crdd = 0.0
        em = 0.0
        er = 0.0

        # Check for valid inputs
        # Sands/Goblet/Circlet substat check
        if slot in ("sands", "goblet", "circlet"):
            if not (mainstat != substat1 != substat2 != substat3 != substat4):
                return render_template("submit.html", supported_artifact_sets=supported_artifact_sets, error = "sub stat cannot be same as main stat")
        # Substats all different check
        if not (substat1 != substat2 != substat3 != substat4):
            return render_template("submit.html", supported_artifact_sets=supported_artifact_sets, error = "sub stats cannot match")
        # Check substats all have values
        if not (substat1_v or substat2_v or substat3_v or substat4_v):
            return render_template("submit.html", error="no sub stat values", supported_artifact_sets=supported_artifact_sets)

        #check substats are numbers
        for x in sub_stat:
            if isfloat(sub_stat[x]) == False:
                return render_template("submit.html", supported_artifact_sets=supported_artifact_sets, error="sub values must be numerical")
            # loop through substats and change values if appropriate
            else:
                if x == "Health":
                    hpf = float(sub_stat[x])
                if x == "Health%":
                    hpp = float(sub_stat[x])
                if x == "Defence":
                    deff = float(sub_stat[x])
                if x == "Defence%":
                    defp = float(sub_stat[x])
                if x == "Attack":
                    attk = float(sub_stat[x])
                if x == "Attack%":
                    attkp = float(sub_stat[x])
                if x == "Crit Rate":
                    crtt = float(sub_stat[x])
                if x == "Crit Damage":
                    crdd = float(sub_stat[x])
                if x == "Elemental Mastery":
                    em = float(sub_stat[x])
                if x == "Energy Recharge":
                    er = float(sub_stat[x])

        # goblet specific check. value = to mainstat dict unless its a elemental DMG goblet.
        if mainstat == "Elemental DMG":
            mainvalue = mainstat_v
        else:
            mainvalue = main_stat[mainstat]

        value = mainvalue

        db.execute("INSERT INTO artifacts (user, artset, slot, mainstat, mainvalue, hpf, hpp, deff, defp, attk, attkp, crtt, crdd, em, er) VALUES(:user, :artset, :slot, :main, :mainvalue, :hpf, :hpp, :deff, :defp, :attk, :attkp, :crtt, :crdd, :em, :er);", user=user, artset=artset, slot=slot.capitalize(), main=main, mainvalue=mainvalue, hpf=hpf, hpp=hpp, deff=deff, defp=defp, attk=attk, attkp=attkp, crtt=crtt, crdd=crdd, em=em, er=er)


        return render_template("submit.html", value="artifact entered into database", supported_artifact_sets=supported_artifact_sets)

    else:
        return render_template("submit.html", supported_artifact_sets=supported_artifact_sets)


@app.route("/artifact", methods=["GET", "POST"])
@login_required
def artifact():

    user = session["user_id"]

    index = []
    sub_index = []

    sub_dict = {
        "Health": "hpf",
        "Health%": "hpp",
        "Attack": "attk",
        "Attack%": "attkp",
        "Defence": "deff",
        "Defence%": "defp",
        "Crit Rate": "crtt",
        "Crit Damage": "crdd",
        "Elemental Mastery": "em",
        "Energy Recharge": "er",
    }

    raw_index = db.execute("SELECT * FROM artifacts WHERE user = :user", user=user)

    for raw in raw_index:
        sub_index.clear()
        for sub in sub_dict:
            if raw[sub_dict[sub]] != 0.0:
                sub_value = raw[sub_dict[sub]]
                sub_index.append([sub, sub_value])
        index.append({"Set": raw["artset"], "Slot": raw["slot"], "Main Stat": raw["mainstat"], "Main Value": raw["mainvalue"], "Sub1": sub_index[0], "Sub2": sub_index[1], "Sub3": sub_index[2], "Sub4": sub_index[3], "Id": raw["Id"],})


    if request.method == "POST":

        art_id = int(request.form.get("delete"))
        ind_len = len(raw_index)
        for i in range(ind_len):
            if art_id == raw_index[i]["Id"]:
                db.execute("DELETE FROM artifacts WHERE Id = ?", art_id)
                check = "Artifact deleted"

        return redirect("/artifact")


    else:
        return render_template("artifact.html", index=index, supported_artifact_sets=supported_artifact_sets)


@app.route("/loadout", methods=["GET", "POST"])
@login_required
def loadout():

    user = session["user_id"]

    index = []
    sub_index = []
    item_list =[]

    sub_dict = {
        "Health": "hpf",
        "Health%": "hpp",
        "Attack": "attk",
        "Attack%": "attkp",
        "Defence": "deff",
        "Defence%": "defp",
        "Crit Rate": "crtt",
        "Crit Damage": "crdd",
        "Elemental Mastery": "em",
        "Energy Recharge": "er",
    }

    raw_index = db.execute("SELECT * FROM artifacts WHERE user = ?", user)

    for raw in raw_index:
        sub_index.clear()
        for sub in sub_dict:
            if raw[sub_dict[sub]] != 0.0:
                sub_value = raw[sub_dict[sub]]
                sub_index.append([sub, sub_value])
        index.append({"Set": raw["artset"], "Slot": raw["slot"], "Main Stat": raw["mainstat"], "Main Value": raw["mainvalue"], "Sub1": sub_index[0], "Sub2": sub_index[1], "Sub3": sub_index[2], "Sub4": sub_index[3], "Id": raw["Id"],})
        item_list.append(raw["Id"])

    char_dbs = {
        "Yae Miko": ["char_yae", "Catalyst"],
        "Ganyu": ["char_ganyu", "Bow"],
    }

    character_stats = 0
    character = 0
    weapons = 0

    if request.method == "POST":
        character = request.form.get("char-selector")
        char_key = char_dbs[character][0]
        character_stats = db.execute("SELECT * FROM ?", char_key)
        weapon_key = char_dbs[character][1]
        weapons = db.execute("SELECT * FROM weapons WHERE type = ?", weapon_key)

        return render_template("loadout.html", index=index, item_list=item_list, character_stats=character_stats, character=character, weapons=weapons)

    else:
        return render_template("loadout.html", index=index, item_list=item_list, character_stats=character_stats, character=character, weapons=weapons)

@app.route("/account", methods=["GET", "POST"])
@login_required
def account():

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        user = session["user_id"]

        if not username:
            return render_template("account.html", warning = "Please enter username")
        if not password:
            return render_template("account.html", warning = "Please enter password")
        if not confirm:
            return render_template("account.html", warning = "Please confirm password")
        if password != confirm:
            return render_template("account.html", warning = "Passwords do not match")

        check = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(check) != 1 or not check_password_hash(check[0]["hash"], password):
            return render_template("account.html", warning = "Invalid username and/or password")

        db.execute("DELETE FROM artifacts WHERE user = ?", user)
        db.execute("DELETE FROM users WHERE id = ?", user)

        session.clear()

        return redirect("/")

    else:
        return render_template("account.html")