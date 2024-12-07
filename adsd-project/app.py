from flask import Flask, request, jsonify, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database initialization
DATABASE = 'alumni.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alumni (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT NOT NULL,
                career TEXT NOT NULL
            );
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS career_milestones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name text not null,
                milestone TEXT NOT NULL,
                date_achieved DATE NOT NULL            );
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_name TEXT NOT NULL,
                event_date DATE NOT NULL
            );
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS event_participation (
                alumnus_id INTEGER,
                event_id INTEGER,
                FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
            );
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS donations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alumnus_id INTEGER,
                donation_amount REAL NOT NULL,
                donation_date DATE NOT NULL            );
        ''')
        conn.commit()

# Routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/view_alumni")
def view_alumni():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM alumni")
        alumni = cursor.fetchall()
    return render_template("view_alumni.html", alumni=alumni)

@app.route("/add_alumni", methods=["GET", "POST"])
def add_alumni():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        career = request.form["career"]

        try:
            with sqlite3.connect(DATABASE) as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO alumni (name, email, phone, career) VALUES (?, ?, ?, ?)",
                               (name, email, phone, career))
                conn.commit()
            return redirect(url_for('view_alumni'))
        except sqlite3.IntegrityError:
            return jsonify({"error": "Alumnus with this email already exists"}), 409

    return render_template("add_alumni.html")

@app.route("/add_milestone", methods=["GET", "POST"])
def add_milestone():
    if request.method == "POST":
        name = request.form["name"]
        milestone = request.form["milestone"]
        date_achieved = request.form["date_achieved"]

        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO career_milestones (name, milestone, date_achieved) VALUES (?, ?, ?)",
                           (name, milestone, date_achieved))
            conn.commit()

        return redirect(url_for('view_alumni'))

    return render_template("add_milestone.html")

@app.route("/add_event", methods=["GET", "POST"])
def add_event():
    if request.method == "POST":
        event_name = request.form["event_name"]
        event_date = request.form["event_date"]

        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO events (event_name, event_date) VALUES (?, ?)", 
                           (event_name, event_date))
            conn.commit()

        return redirect(url_for('view_alumni'))

    return render_template("add_event.html")

@app.route("/view_milestones")
def view_milestones():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM career_milestones")
        milestones = cursor.fetchall()
        print(milestones)
    return render_template("view_milestones.html", milestones=milestones)

if __name__ == '__main__':
    init_db()
