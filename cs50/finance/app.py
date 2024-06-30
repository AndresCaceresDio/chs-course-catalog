import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

stocks = {}

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


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
    if request.method == "GET":
        id = session["user_id"]
        username = alphabetize(str(db.execute('SELECT username FROM users WHERE id = ?', id))).split("username")[1]
        rows = db.execute('SELECT * FROM portfolio WHERE username = ?', username)
        if len(rows) == 0:
            return render_template("blankIndex.html")
        cash = int(digitize(str(db.execute('SELECT cash FROM users WHERE id = ?', id))))
        portfolio_id = int(digitize(str(db.execute('SELECT id FROM portfolio WHERE username = ? LIMIT 1', username))))
        stocks = []
        stock_prices = []
        shares = []
        holding_values = []
        for i in range(len(rows)):
            stocks.append(symbolize(str(db.execute('SELECT stock FROM portfolio WHERE id = ?', (portfolio_id + i)))))
            if stocks[i] == "":
                stocks.remove(stocks[i])
            stock_prices.append(int(lookup(stocks[i])['price']))
            shares.append(
                int(digitize(str(db.execute('SELECT shares FROM portfolio WHERE username = ? AND stock = ?', username, stocks[i])))))
            holding_values.append(stock_prices[i] * shares[i])
            grand_total = cash + total(holding_values)
        return render_template("index.html", usd=usd, cash=usd(cash), username=username, grand_total=usd(grand_total),
                               stocks=stocks, shares=shares, holding_values=holding_values, stock_prices=stock_prices, owned=range(len(stocks)))
    return apology("TODO")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        id = session["user_id"]
        username = alphabetize(str(db.execute('SELECT username FROM users WHERE id = ?', id))).split("username")[1]
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        try:
            if lookup(symbol) == None or symbol == "":
                return apology("invalid stock symbol")
            elif int(shares) < 1:
                return apology("Cannot buy less than 1 shares")
        except (ValueError):
            return apology("Cannot buy a fraction of a share")
        rows = db.execute('SELECT * FROM portfolio WHERE username = ?', username)
        bought_symbol = 0
        bought_shares = 0
        bought_price = 0
        if len(rows) > 0:
            bought_symbol = symbolize(
                str(db.execute('SELECT stock FROM portfolio WHERE stock = ? AND username = ? LIMIT 1', symbol, username)))
            if lookup(bought_symbol) != None:
                bought_shares = int(
                    digitize(str(db.execute('SELECT shares FROM portfolio WHERE stock = ? AND username = ?', symbol, username))))
                bought_price = int(
                    digitize(str(db.execute('SELECT price FROM portfolio WHERE stock = ? AND username = ?', symbol, username))))
        stocks = lookup(symbol)
        updated_shares = int(int(shares) + int(bought_shares))
        price = int(stocks['price']) * int(shares)
        new_price = bought_price + price
        cash = int(digitize(str(db.execute('SELECT cash FROM users WHERE id = ?', id))))
        if cash < price:
            return apology("You cannot afford this")
        elif symbol == bought_symbol:
            updated_cash = cash - price
            db.execute('UPDATE users SET cash = ? WHERE id = ?', updated_cash, id)
            db.execute('INSERT INTO purchases (stock, username, price, shares) VALUES (?, ?, ?, ?)',
                       stocks['name'], username, price, shares)
            db.execute('UPDATE portfolio SET shares = ? WHERE username = ? AND stock = ?', updated_shares, username, symbol)
            db.execute('UPDATE portfolio SET price = ? WHERE username = ? AND stock = ?', new_price, username, symbol)
            return redirect("/")
        updated_cash = cash - price
        db.execute('UPDATE users SET cash = ? WHERE id = ?', updated_cash, id)
        db.execute('INSERT INTO purchases (stock, username, price, shares) VALUES (?, ?, ?, ?)',
                   stocks['name'], username, price, shares)
        db.execute('INSERT INTO portfolio (stock, username, price, shares) VALUES (?, ?, ?, ?)',
                   stocks['name'], username, price, shares)
        return redirect("/")
    elif request.method == "GET":
        return render_template("buy.html")
    return apology("TODO")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    if request.method == "GET":
        id = session["user_id"]
        username = alphabetize(str(db.execute('SELECT username FROM users WHERE id = ?', id))).split("username")[1]
        purchased_rows = db.execute('SELECT * FROM purchases WHERE username = ?', username)
        sold_rows = db.execute('SELECT * FROM sales WHERE username = ?', username)
        if len(purchased_rows) == 0:
            return render_template("blankHistory.html")
        purchased_id = int(digitize(str(db.execute('SELECT id FROM purchases WHERE username = ? LIMIT 1', username))))
        purchased_stocks = []
        purchased_prices = []
        purchased_shares = []
        purchased_times = []
        for i in range(len(purchased_rows)):
            purchased_stocks.append(symbolize(str(db.execute('SELECT stock FROM purchases WHERE id = ?', (purchased_id + i)))))
            if lookup(purchased_stocks[i]) == None:
                purchased_stocks.remove(purchased_stocks[i])
            purchased_prices.append(int(digitize(str(db.execute('SELECT price FROM purchases WHERE id = ?', (purchased_id + i))))))
            purchased_shares.append(int(digitize(str(db.execute('SELECT shares FROM purchases WHERE id = ?', (purchased_id + i))))))
            purchased_times.append(convert_datetime(str(db.execute('SELECT time FROM purchases WHERE id = ?', (purchased_id + i)))))
            sold_stocks = []
            sold_prices = []
            sold_shares = []
            sold_times = []
        if len(sold_rows) > 0:
            sold_id = int(digitize(str(db.execute('SELECT id FROM sales WHERE username = ? LIMIT 1', username))))
            for i in range(len(sold_rows)):
                sold_stocks.append(symbolize(str(db.execute('SELECT stock FROM sales WHERE id = ?', (sold_id + i)))))
                if lookup(sold_stocks[i]) == None:
                    sold_stocks.remove(sold_stocks[i])
                sold_prices.append(int(digitize(str(db.execute('SELECT price FROM sales WHERE id = ?', (sold_id + i))))))
                sold_shares.append(int(digitize(str(db.execute('SELECT shares FROM sales WHERE id = ?', (sold_id + i))))))
                sold_times.append(convert_datetime(str(db.execute('SELECT time FROM sales WHERE id = ?', (sold_id + i)))))
        return render_template("history.html", usd=usd, purchased_action="Bought", sold_action="Sold",
                               purchased_stocks=purchased_stocks, purchased_prices=purchased_prices, purchased_shares=purchased_shares,
                               purchased_times=purchased_times, sold_stocks=sold_stocks, sold_prices=sold_prices, sold_shares=sold_shares,
                               sold_times=sold_times, purchased_total=range(len(purchased_stocks)), sold_total=range(len(sold_stocks)))
    return apology("TODO")


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
    if request.method == "POST":
        symbol = request.form.get("symbol")
        stocks = lookup(symbol)
        if stocks == None or symbol == "":
            return apology("Invalid symbol")
        return render_template("quoted.html", stocks=stocks)
    elif request.method == "GET":
        return render_template("quote.html")
    return apology("TODO")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        id = 1
        username = request.form.get("username")
        password = request.form.get("password")
        password_hash = generate_password_hash(password)
        confirmation = request.form.get("confirmation")
        if password != confirmation:
            return apology("passwords do not match")
        elif password == "" or confirmation == "":
            return apology("one or more password fields left blank")
        elif username == "":
            return apology("username field cannot be blank")
        elif "}]" in username or "'" in username or " " in username:
            return apology("one or more username characters not supported")
        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, password_hash)
        except (ValueError):
            return apology("username already in use")
        return redirect("/")
    elif request.method == "GET":
        return render_template("register.html")
    return apology("TODO")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        sold_shares = int(request.form.get("shares"))
        if symbol == "Stock Symbol":
            return apology("Must choose a stock to sell")
        elif sold_shares < 0:
            return apology("Cannot sell less than 1 shares")
        id = session["user_id"]
        username = alphabetize(str(db.execute('SELECT username FROM users WHERE id = ?', id))).split("username")[1]
        cash = int(digitize(str(db.execute('SELECT cash FROM users WHERE id = ?', id))))
        bought_shares = int(
            digitize(str(db.execute('SELECT shares FROM portfolio WHERE username = ? AND stock = ?', username, symbol))))
        price = int(digitize(str(db.execute('SELECT price FROM portfolio WHERE username = ? AND stock = ?', username, symbol))))
        sold_price = sold_shares * (int(lookup(symbol)['price']))
        updated_cash = cash + price
        updated_price = price - sold_price
        updated_shares = bought_shares - sold_shares
        if sold_shares > bought_shares:
            return apology("Cannot sell more shares than you own")
        elif sold_shares == bought_shares:
            db.execute('UPDATE users SET cash = ? WHERE id = ?', updated_cash, id)
            db.execute('INSERT INTO sales (stock, username, price, shares) VALUES (?, ?, ?, ?)',
                       symbol, username, sold_price, sold_shares)
            db.execute('DELETE FROM portfolio WHERE username = ? AND stock = ?', username, symbol)
            return redirect("/")
        elif sold_shares < bought_shares:
            db.execute('UPDATE users SET cash = ? WHERE id = ?', updated_cash, id)
            db.execute('UPDATE portfolio SET price = ? WHERE username = ? and stock = ?', updated_price, username, symbol)
            db.execute('UPDATE portfolio SET shares = ? WHERE username = ? and stock = ?', updated_shares, username, symbol)
            db.execute('INSERT INTO sales (stock, username, price, shares) VALUES (?, ?, ?, ?)',
                       symbol, username, sold_price, sold_shares)
            return redirect("/")
        return redirect("/")
    elif request.method == "GET":
        id = session["user_id"]
        username = alphabetize(str(db.execute('SELECT username FROM users WHERE id = ?', id))).split("username")[1]
        rows = db.execute('SELECT * FROM portfolio WHERE username = ?', username)
        if len(rows) == 0:
            return render_template("blankSell.html")
        portfolio_id = int(digitize(str(db.execute('SELECT id FROM portfolio WHERE username = ? LIMIT 1', username))))
        stocks = []
        for i in range(len(rows)):
            stocks.append(symbolize(str(db.execute('SELECT stock FROM portfolio WHERE id = ?', portfolio_id + i))))
            if stocks[i] == "":
                stocks.remove(stocks[i])
        return render_template("sell.html", stocks=stocks, total=range(len(stocks)))
    return apology("TODO")


@app.route("/changepassword", methods=["GET", "POST"])
@login_required
def change_password():
    """Sell shares of stock"""
    if request.method == "POST":
        id = session["user_id"]
        old_password = request.form.get("oldpassword")
        rows = db.execute("SELECT * FROM users WHERE id = ?", id)
        if not check_password_hash(rows[0]["hash"], old_password):
            return apology("please your old password correctly")
        new_password = request.form.get("newpassword")
        password_confirmation = request.form.get("confirm")
        new_password_hash = generate_password_hash(new_password)
        if new_password != password_confirmation:
            return apology("passwords do not match")
        elif new_password == "" or password_confirmation == "":
            return apology("one or more password fields left blank")
        db.execute('UPDATE users SET hash = ? WHERE id = ?', new_password_hash, id)
        session.clear()
        return redirect("/")
    elif request.method == "GET":
        return render_template("changepassword.html")


def digitize(str):
    newstr = ""
    for i in range(len(str)):
        if str[i].isnumeric():
            newstr += str[i]
    return newstr


def symbolize(str):
    newstr = ""
    for i in range(len(str)):
        if str[i].isalpha():
            if str[i].isupper():
                newstr += str[i]
    return newstr


def alphabetize(str):
    newstr = ""
    for i in range(len(str)):
        if str[i].isalpha() or str[i].isnumeric():
            newstr += str[i]
    return newstr


def convert_datetime(str):
    newstr = ""
    for i in range(len(str)):
        if str[i].isnumeric() or str[i] == " " or str[i] == "-":
            newstr += str[i]
        elif str[i] == ":" and str[i + 1].isnumeric():
            newstr += str[i]
    return newstr


def total(list):
    newint = 0
    for i in range(len(list)):
        newint += int(list[i])
    return newint
