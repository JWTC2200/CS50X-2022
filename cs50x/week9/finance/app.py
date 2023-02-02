import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

db.execute("CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, customer INTEGER NOT NULL, symbol TEXT NOT NULL, shares INTEGER NOT NULL, price REAL NOT NULL, method TEXT NOT NULL, time DATETIME NOT NULL);")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    stocks = db.execute(
        "SELECT symbol, sum(shares), sum(price) FROM transactions GROUP BY symbol HAVING customer = :id", id=session["user_id"])

    # New dict to store values
    index = []
    for stock in stocks:
        if stock["sum(shares)"] != 0:
            check = lookup(stock["symbol"])
            sumtotal = (check["price"]) * stock["sum(shares)"]
            index.append({"symbol": stock["symbol"], "name": check["name"], "shares": stock["sum(shares)"], "current": usd(
                check["price"]), "total": usd(sumtotal), "purchase": usd(stock["sum(price)"])})

    # Find cash amount
    dbcash = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
    cash = float(dbcash[0]["cash"])

    # Total value of holdings at current price
    totalv = 0
    for stock in index:
        totalv = totalv + float(sumtotal)

    totalvalue = cash + totalv

    return render_template("layout.html", index=index, cash=usd(cash), totalvalue=usd(totalvalue))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Check for valid input
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("please enter a stock symbol")

        # check stock symbol is valid
        stock = lookup(symbol)
        if not stock:
            return apology("invalid stock symbol")

        # Check for number input
        number = request.form.get("shares")
        if not number:
            return apology("please enter number of shares")

        # Check integer
        if not number.isnumeric():
            return apology("invalid input")

        # Calculate total value of stocks
        value = stock["price"] * int(number)

        dbcash = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
        cash = float(dbcash[0]["cash"])

        # Check if enough cash in wallet
        if cash < value:
            return apology("not enough cash")
        newcash = cash - value
        time = datetime.now()

        # Change db's. Update cash value. Enter into transactions
        db.execute("UPDATE users SET CASH = :newcash WHERE id = :id", newcash=newcash, id=session["user_id"])
        db.execute("INSERT INTO transactions (customer, symbol, shares, price, method, time) VALUES(:customer, :symbol, :shares, :price, :method, :time);",
                   customer=session["user_id"], symbol=stock["symbol"], shares=number, price=value, method="Buy", time=time)

        return redirect("/")

    else:
        dbcash = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
        cash = float(dbcash[0]["cash"])

        return render_template("buy.html", cash=usd(cash))


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    customer = session["user_id"]
    index = db.execute("SELECT * FROM transactions WHERE customer = ?", customer)

    return render_template("history.html", index=index)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        ticker = request.form.get("symbol")
        quote = lookup(ticker)

        # If quote is invalid and returns "none"
        if not quote:
            return apology("incorrect stock symbol")

        # If quote successful render template with values
        else:
            return render_template("quote.html", symbol=quote["symbol"], name=quote["name"], price=usd(quote["price"]))

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        username = request.form.get("username")
        if not username:
            return apology("must provide username", 400)

        # Check if username already exists in db
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) != 0:
            return apology("username already taken")

        # Check that password and confirmation have been submitted
        password = request.form.get("password")
        password2 = request.form.get("confirmation")
        if not password:
            return apology("please submit password")

        if not password2:
            return apology("please confirm password")

        # Check passwords are the same then hash and store into db
        if password == password2:
            hashword = generate_password_hash(password)
            db.execute("INSERT INTO users (username, hash) VALUES(:username, :hashword)", username=username, hashword=hashword)

            return redirect("/login")

        else:
            return apology("passwords must match", 400)

    # User reached route via GET (as by clicking link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    customer = session["user_id"]

    if request.method == "POST":
        # Get a symbol and check if present/valid held stock
        ticker = request.form.get("symbol")

        if not ticker:
            return apology("please enter a stock symbol")

        symbolcheck = db.execute(
            "SELECT symbol FROM transactions WHERE customer = :customer and symbol = :ticker", customer=customer, ticker=ticker)
        if not len(symbolcheck) > 0:
            return apology("stock not held")

        # Check share if present/valid <= held
        shares = request.form.get("shares")
        if not shares:
            return apology("please enter number of shares")

        sharecheck = db.execute(
            "SELECT SUM(shares) FROM transactions WHERE customer = :customer and symbol = :ticker", customer=customer, ticker=ticker)
        if float(sharecheck[0]["SUM(shares)"]) < float(shares):
            return apology("not enough shares held")

        time = datetime.now()
        sale = lookup(ticker)
        value = sale["price"] * float(shares)

        dbcash = db.execute("SELECT cash FROM users WHERE id = :id", id=customer)
        cash = float(dbcash[0]["cash"])
        newcash = cash + value

        # Post sale to transactions
        db.execute("INSERT INTO transactions (customer, symbol, shares, price, method, time) VALUES(:customer, :symbol, :shares, :price, :method, :time);",
                   customer=customer, symbol=sale["symbol"], shares=-int(shares), price=value, method="Sell", time=time)
        db.execute("UPDATE users SET CASH = :newcash WHERE id = :id", newcash=newcash, id=customer)

        return redirect("/")

    else:
        # Show stocks currently owned
        stocks = db.execute("SELECT symbol, sum(shares), price FROM transactions GROUP BY symbol HAVING customer = :id", id=customer)

        # New dict to store values
        index = []
        for stock in stocks:
            if stock["sum(shares)"] != 0:
                check = lookup(stock["symbol"])
                sumtotal = (check["price"]) * stock["sum(shares)"]
                index.append({"symbol": stock["symbol"], "name": check["name"], "shares": stock["sum(shares)"], "current": usd(
                    check["price"]), "total": usd(sumtotal), "purchase": usd(stock["price"])})

        # Find cash amount
        dbcash = db.execute("SELECT cash FROM users WHERE id = :id", id=customer)

        return render_template("sell.html", index=index)


# Provided a facility for the user to add or withdraw funds

@app.route("/manage", methods=["GET", "POST"])
@login_required
def manage():

    if request.method == "POST":
        customer = session["user_id"]
        method = request.form.get("manage")
        value = request.form.get("value")
        dbcash = db.execute("SELECT cash FROM users WHERE id = :id", id=customer)
        cash = float(dbcash[0]["cash"])

        if not value:
            return apology("Enter a value")

        if not method:
            return apology("Please select an option")

        if method == "addfunds":
            result = cash + float(value)

        if method == "withdraw":
            result = cash - float(value)

        db.execute("UPDATE users SET CASH = :result WHERE id = :id", result=result, id=customer)

        return redirect("/")

    else:
        return render_template("manage.html")

