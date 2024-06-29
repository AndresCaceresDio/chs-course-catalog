from flask import Flask, request, jsonify, render_template
from datetime import datetime

app = Flask(__name__)

questions = {0: ("A sweeping device that causes your demise.", "doombroom", "broomdoom"),
             1: ("A fun activity that makes you feel bad about yourself.", "shamegame", "gameshame"),
             2: ("A wealthy fastball", "richpitch", "pitchrich"),
             3: ("An intelligent diagram", "smartchart", "chartsmart"),
             4: ("Strange facial hair", "weirdbeard", "beardweird")}
day_of_year = datetime.now().timetuple().tm_yday
INT = (day_of_year) % len(questions)
question = questions[INT][0]


def check(cleanInput):
    if cleanInput == questions[INT][1] or cleanInput == questions[INT][2]:
        return True
    else:
        return False


@app.route('/submit-hink-pink', methods=['POST'])
def submit_hink_pink():
    cleanInput = request.form['wordOne'].strip().lower() + request.form['wordTwo'].strip().lower()
    hink_pink_correct = check(cleanInput)
    message = 'Correct!' if hink_pink_correct else 'Try again!'
    return jsonify({'message': message})


@app.route('/')
def index():
    return render_template('index.html', question=question)


if __name__ == '__main__':
    app.run(debug=True)
