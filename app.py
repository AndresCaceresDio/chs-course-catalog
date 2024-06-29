from flask import Flask, render_template
import sqlite3

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route("/")
def home_page():
    conn = sqlite3.connect("courses.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM chs_catalog")

    rows = cursor.fetchall()

    course_catalog = {row[0]: (row[1], row[2], row[3], row[4], row[5]) for row in rows}

    conn.close()
    return render_template(
        "home_page.html", results=course_catalog, total=range(len(course_catalog))
    )


if __name__ == "__main__":
    app.run(debug=True)
