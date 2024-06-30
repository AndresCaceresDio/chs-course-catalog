import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps


# Configure application
app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///taskLy.db")


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        id = 0
        try:
            id = int(digitize(str(db.execute('SELECT MAX(id) FROM users'))))
        except (ValueError):
            print("")
        usernames = []
        for i in range(id):
            try:
                usernames.append((alphabetize(str(db.execute('SELECT username FROM users WHERE id = ?', (i + 1)))).split("username")[1]).strip())
            except (IndexError):
                print("")
        new_id = id + 1
        username = request.form.get("username")
        password = request.form.get("password")
        password_hash = generate_password_hash(password)
        confirmation = request.form.get("confirmation")
        if password != confirmation:
            return render_template("error.html", text="PASSWORDS DO NOT MATCH")
        elif username == "":
            return render_template("error.html", text="USERNAME CANNOT BE BLANK")
        elif password == "" or confirmation == "":
            return render_template("error.html", text="ONE OR MORE PASSWORD FIELDS LEFT BLANK")
        elif "}]" in username or "'" in username or " " in username:
            return render_template("error.html", text="ONE OR MORE USERNAME CHARACTERS NOT SUPPORTED")
        elif username in usernames:
            return render_template("error.html", text="USERNAME ALREADY IN USE")
        db.execute("INSERT INTO users (id, username, password_hash) VALUES (?, ?, ?)", new_id, username, password_hash)
        return redirect("/")
    elif request.method == "GET":
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()
    if request.method == "POST":
        if not request.form.get("username"):
            return render_template("error.html", text="USERNAME FIELD CANNOT BE BLANK")
        elif not request.form.get("password"):
            return render_template("error.html", text="PASSWORD FIELD CANNOT BE BLANK")
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rows) != 1 or not check_password_hash(rows[0]["password_hash"], request.form.get("password")):
            return render_template("error.html", text="INVALID USERNAME AND/OR PASSWORD")
        session["user_id"] = rows[0]["id"]
        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/")
@login_required
def tasks():
    """See all of your current tasks"""
    if request.method == "GET":
        id = session["user_id"]
        username = (alphabetize(str(db.execute('SELECT username FROM users WHERE id = ?', id))).split("username")[1]).strip()
        try:
            rows = int(digitize(str(db.execute('SELECT MAX(id) FROM tasks'))))
        except (ValueError):
            return render_template("tasks.html")
        tasks = []
        descriptions = []
        tags = []
        priorities = []
        due_dates = []
        times = []
        for i in range(rows):
            try:
                tasks.append(alphabetize(str(db.execute('SELECT task FROM tasks WHERE id = ? AND username = ?', (i + 1), username))).split("task")[1])
                descriptions.append(alphabetize(str(db.execute('SELECT description FROM tasks WHERE id = ? AND username = ?', (i + 1), username))).split("description")[1])
                tags.append(alphabetize(str(db.execute('SELECT tag FROM tasks WHERE id = ? AND username = ?', (i + 1), username))).split("tag")[1])
                priorities.append(alphabetize(str(db.execute('SELECT priority FROM tasks WHERE id = ? AND username = ?', (i + 1), username))).split("priority")[1])
                due_dates.append(convert_datetime(str(db.execute('SELECT due_date FROM tasks WHERE id = ? AND username = ?', (i + 1), username))))
                times.append(convert_datetime(str(db.execute('SELECT time FROM tasks WHERE id = ? AND username = ?', (i + 1), username))))
            except (IndexError):
                print("")
        for i in range(rows):
            try:
                due_dates[i] = str(due_dates[i])
                due_dates[i] += " "
                due_dates[i] += times[i]
            except (IndexError):
                print("")
        return render_template("tasks.html", total=range(len(tasks)), tasks=tasks, descriptions=descriptions,
                               tags=tags, priorities=priorities, due_dates=due_dates)


@app.route("/add-tasks", methods=["GET", "POST"])
@login_required
def add_tasks():
    """Add new tasks to your schedule"""
    if request.method == "POST":
        id = session["user_id"]
        username = (alphabetize(str(db.execute('SELECT username FROM users WHERE id = ?', id))).split("username")[1]).strip()
        title = request.form.get("title")
        due_date = request.form.get("date")
        time = request.form.get("time")
        description = request.form.get("description")
        category = (request.form.get("category")).strip()
        priority = request.form.get("inlineRadioOptions")
        if title == "" or due_date == "" or time == "":
            return render_template("error.html", text="ONE OR MORE REQUIRED FIELDS LEFT BLANK")
        db.execute('INSERT INTO tasks (username, task, description, tag, priority, due_date, time) VALUES (?, ?, ?, ?, ?, ?, ?)',
                   username, title, description, category, priority, due_date, time)
        return redirect("/")
    elif request.method == "GET":
        id = session["user_id"]
        username = (alphabetize(str(db.execute('SELECT username FROM users WHERE id = ?', id))).split("username")[1]).strip()
        try:
            rows = int(digitize(str(db.execute('SELECT MAX(id) FROM categories WHERE username = ?', username))))
        except (ValueError):
            return render_template("add-tasks.html")
        categories = []
        for i in range(rows):
            try:
                categories.append(alphabetize(str(db.execute('SELECT category FROM categories WHERE username = ? AND id = ?', username, (i + 1))).split("category")[1]))
            except (IndexError):
                print("")
        return render_template("add-tasks.html", categories=categories, total=range(len(categories)))


@app.route("/manage-categories", methods=["GET", "POST"])
@login_required
def manage_categories():
    """Manage your task categories"""
    if request.method == "POST":
        id = session["user_id"]
        username = (alphabetize(str(db.execute('SELECT username FROM users WHERE id = ?', id))).split("username")[1]).strip()
        try:
            rows = int(digitize(str(db.execute('SELECT MAX(id) FROM categories'))))
        except (ValueError):
            return render_template("manage-categories.html")
        categories = []
        action = (request.form.get("action")).strip()
        name = str((request.form.get("name")).strip())
        for i in range(rows):
            try:
                categories.append((alphabetize(str(db.execute('SELECT category FROM categories WHERE id = ? AND username = ?', (i + 1), username))).split("category")[1]).strip())
            except (IndexError):
                print("")
        if name == "":
            return render_template("error.html", text="CATEGORY NAME CANNOT BE BLANK")
        elif action == "Add" and name in categories:
            return render_template("error.html", text="CATEGORY YOU ARE TRYING TO ADD ALREADY EXISTS")
        elif action == "Remove" and name == "No Category":
            return render_template("error.html", text="YOU CANNOT REMOVE THAT CATEGORY")
        elif action == "Remove" and name not in categories:
            return render_template("error.html", text="CATEGORY YOU ARE TRYING TO REMOVE DOES NOT EXIST")
        elif action == "Remove" and name in categories:
            db.execute('DELETE FROM categories WHERE category = ? AND username = ?', name, username)
            db.execute('UPDATE tasks SET tag = ? WHERE tag = ?', "No Category", name)
        elif action == "Add":
            db.execute('INSERT INTO categories (username, category) VALUES (?, ?)', username, name)
        return redirect("/")
    elif request.method == "GET":
        id = session["user_id"]
        username = (alphabetize(str(db.execute('SELECT username FROM users WHERE id = ?', id))).split("username")[1]).strip()
        try:
            rows = int(digitize(str(db.execute('SELECT MAX(id) FROM categories WHERE username = ?', username))))
        except (ValueError):
            return render_template("manage-categories.html")
        categories = []
        string = ""
        for i in range(rows):
            try:
                categories.append(alphabetize(str(db.execute('SELECT category FROM categories WHERE username = ? AND id = ?', username, (i + 1))).split("category")[1]))
            except (IndexError):
                print("")
        for i in range(len(categories)):
            try:
                if i == 0:
                    string += ", "
                if categories[i + 1] != "":
                    string += categories[i]
                    string += ", "
            except (IndexError):
                string += categories[i]
        return render_template("manage-categories.html", categories=string)


@app.route("/change-category", methods=["GET", "POST"])
@login_required
def change_category():
    if request.method == "POST":
        id = session["user_id"]
        username = (alphabetize(str(db.execute('SELECT username FROM users WHERE id = ?', id))).split("username")[1]).strip()
        task = (request.form.get("task")).strip()
        category = request.form.get("category").strip()
        db.execute("UPDATE tasks SET tag = ? WHERE task = ? AND username = ?", category, task, username)
        return redirect("/")
    elif request.method == "GET":
        id = session["user_id"]
        username = (alphabetize(str(db.execute('SELECT username FROM users WHERE id = ?', id))).split("username")[1]).strip()
        try:
            task_rows = int(digitize(str(db.execute('SELECT MAX(id) FROM tasks'))))
            category_rows = int(digitize(str(db.execute('SELECT MAX(id) FROM categories'))))
        except (ValueError):
            return render_template("change-category.html")
        tasks = []
        categories = []
        for i in range(task_rows):
            try:
                tasks.append(alphabetize(str(db.execute('SELECT task FROM tasks WHERE id = ? AND username = ?', (i + 1), username))).split("task")[1])
            except (IndexError):
                print("")
        for i in range(category_rows):
            try:
                categories.append((alphabetize(str(db.execute('SELECT category FROM categories WHERE id = ? AND username = ?', (i + 1), username))).split("category")[1]).strip())
            except (IndexError):
                print("")
        return render_template("change-category.html", tasks=tasks, task_total=range(len(tasks)), categories=categories,
                               category_total=range(len(categories)))


@app.route("/manage-tasks", methods=["GET", "POST"])
@login_required
def manage_tasks():
    """Remove or change tasks"""
    if request.method == "POST":
        id = session["user_id"]
        username = (alphabetize(str(db.execute('SELECT username FROM users WHERE id = ?', id))).split("username")[1]).strip()
        task = (request.form.get("task").strip())
        action = (request.form.get("action").strip())
        due_day = convert_datetime(str(db.execute('SELECT due_date FROM tasks WHERE task = ? AND username = ?', task, username)))
        due_time = convert_datetime(str(db.execute('SELECT time FROM tasks WHERE task = ? AND username = ?', task, username)))
        if action == "Change Category":
            return redirect("/change-category")
        elif action == "Remove":
            db.execute("DELETE FROM tasks WHERE task = ? AND username = ?", task, username)
            return redirect("/")
        elif action == "Mark as Complete":
            db.execute("DELETE FROM tasks WHERE task = ? AND username = ?", task, username)
            db.execute("INSERT INTO completed_tasks (username, task, due_day, due_time) VALUES (?, ?, ?, ?)", username, task, due_day, due_time)
            return redirect("/")
    elif request.method == "GET":
        id = session["user_id"]
        username = (alphabetize(str(db.execute('SELECT username FROM users WHERE id = ?', id))).split("username")[1]).strip()
        try:
            rows = int(digitize(str(db.execute('SELECT MAX(id) FROM tasks'))))
        except (ValueError):
            return render_template("manage-tasks.html")
        tasks = []
        for i in range(rows):
            try:
                tasks.append(alphabetize(str(db.execute('SELECT task FROM tasks WHERE id = ? AND username = ?', (i + 1), username))).split("task")[1])
            except (IndexError):
                print("")
        return render_template("manage-tasks.html", tasks=tasks, total=range(len(tasks)))


@app.route("/history")
@login_required
def history():
    """Look at the history of your completed tasks"""
    if request.method == "GET":
        id = session["user_id"]
        username = (alphabetize(str(db.execute('SELECT username FROM users WHERE id = ?', id))).split("username")[1]).strip()
        try:
            rows = int(digitize(str(db.execute('SELECT MAX(id) FROM completed_tasks'))))
        except (ValueError):
            return render_template("history.html")
        tasks = []
        completed_days = []
        completed_times = []
        due_days = []
        due_times = []
        for i in range(rows):
            try:
                tasks.append(alphabetize(str(db.execute('SELECT task FROM completed_tasks WHERE id = ? AND username = ?', (i + 1), username))).split("task")[1])
                completed_days.append(convert_datetime(str(db.execute('SELECT completed_day FROM completed_tasks WHERE id = ? AND username = ?', (i + 1), username))))
                completed_times.append(convert_datetime(str(db.execute('SELECT completed_time FROM completed_tasks WHERE id = ? AND username = ?', (i + 1), username))))
                due_days.append(convert_datetime(str(db.execute('SELECT due_day FROM completed_tasks WHERE id = ? AND username = ?', (i + 1), username))))
                due_times.append(convert_datetime(str(db.execute('SELECT due_time FROM completed_tasks WHERE id = ? AND username = ?', (i + 1), username))))
            except (IndexError):
                print("")
        for i in range(len(tasks)):
            completed_days[i] = str(completed_days[i])
            completed_days[i] += " "
            completed_days[i] += completed_times[i]
        for i in range(len(tasks)):
            due_days[i] = str(due_days[i])
            due_days[i] += " "
            due_days[i] += due_times[i]
        return render_template("history.html", total=range(len(tasks)), tasks=tasks, completed_dates=completed_days, due_dates=due_days)


@app.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    """Change your password"""
    if request.method == "POST":
        id = session["user_id"]
        old_password = request.form.get("oldpassword")
        rows = db.execute("SELECT * FROM users WHERE id = ?", id)
        if not check_password_hash(rows[0]["password_hash"], old_password):
            return render_template("error.html", text="OLD PASSWORD IS INCORRECT")
        new_password = request.form.get("newpassword")
        password_confirmation = request.form.get("confirm")
        new_password_hash = generate_password_hash(new_password)
        if new_password != password_confirmation:
            return render_template("error.html", text="PASSWORDS DO NOT MATCH")
        elif new_password == "" or password_confirmation == "":
            return render_template("error.html", text="ONE OR MORE PASSWORD FIELDS LEFT BLANK")
        db.execute('UPDATE users SET password_hash = ? WHERE id = ?', new_password_hash, id)
        session.clear()
        return redirect("/")
    elif request.method == "GET":
        return render_template("change-password.html")


@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/")


def digitize(str):
    newstr = ""
    for i in range(len(str)):
        if str[i].isnumeric():
            newstr += str[i]
    return newstr


def alphabetize(str):
    newstr = ""
    for i in range(len(str)):
        if str[i] != "]" and str[i] != "[" and str[i] != "{" and str[i] != "}" and str[i] != ":" and str[i] != "'":
            newstr += str[i]
    return newstr.strip()


def convert_datetime(str):
    newstr = ""
    for i in range(len(str)):
        if str[i].isnumeric() or str[i] == "-":
            newstr += str[i]
        elif str[i] == ":" and str[i + 1].isnumeric():
            newstr += str[i]
    return newstr
