from flask import Flask, render_template, request, jsonify, redirect, session
import psycopg2
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "iplauctionsecret"

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

# -------------------------------
# CREATE TABLES
# -------------------------------

cur.execute("""
CREATE TABLE IF NOT EXISTS players(
id SERIAL PRIMARY KEY,
name TEXT UNIQUE,
country TEXT,
role TEXT,
runs INT,
wickets INT,
base_price INT,
current_price INT
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS teams(
id SERIAL PRIMARY KEY,
team_name TEXT UNIQUE
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS bids(
id SERIAL PRIMARY KEY,
player_id INT,
team_name TEXT,
bid_price INT,
bid_time TIMESTAMP
);
""")

conn.commit()

# -------------------------------
# INSERT INITIAL DATA
# -------------------------------

cur.execute("""
INSERT INTO players(name,country,role,runs,wickets,base_price,current_price)
VALUES
('Virat Kohli','India','Batsman',7263,4,20000000,20000000),
('Rohit Sharma','India','Batsman',6200,15,20000000,20000000),
('Jasprit Bumrah','India','Bowler',50,145,15000000,15000000),
('KL Rahul','India','Batsman',4200,0,18000000,18000000),
('Jos Buttler','England','Batsman',3500,0,15000000,15000000),
('Rashid Khan','Afghanistan','Bowler',500,130,15000000,15000000)
ON CONFLICT (name) DO NOTHING;
""")

cur.execute("""
INSERT INTO teams(team_name)
VALUES
('Mumbai Indians'),
('Chennai Super Kings'),
('Royal Challengers Bangalore'),
('Delhi Capitals'),
('Lucknow Super Giants')
ON CONFLICT DO NOTHING;
""")

conn.commit()

# -------------------------------
# LOGIN PAGE
# -------------------------------

@app.route("/", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "ipl123":

            session["user"] = username
            return redirect("/dashboard")

    return render_template("index.html")

# -------------------------------
# DASHBOARD
# -------------------------------

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/")

    country = request.args.get("country")

    if country:
        cur.execute("SELECT * FROM players WHERE country=%s",(country,))
    else:
        cur.execute("SELECT * FROM players")

    players = cur.fetchall()

    return render_template("dashboard.html",players=players)

# -------------------------------
# PLAYER DETAILS PAGE
# -------------------------------

@app.route("/player/<int:player_id>")
def player(player_id):

    cur.execute("SELECT * FROM players WHERE id=%s",(player_id,))
    player = cur.fetchone()

    cur.execute("SELECT * FROM teams")
    teams = cur.fetchall()

    return render_template("player.html",player=player,teams=teams)

# -------------------------------
# GET PLAYERS API
# -------------------------------

@app.route("/players")
def players():

    cur.execute("SELECT * FROM players")
    data = cur.fetchall()

    players = []

    for p in data:
        players.append({
            "id":p[0],
            "name":p[1],
            "country":p[2],
            "role":p[3],
            "runs":p[4],
            "wickets":p[5],
            "price":p[7]
        })

    return jsonify(players)

# -------------------------------
# BID SYSTEM
# -------------------------------

@app.route("/bid", methods=["POST"])
def bid():

    player_id = request.json["player_id"]
    bid_price = int(request.json["price"])
    team = request.json["team"]

    cur.execute(
        "SELECT current_price FROM players WHERE id=%s",
        (player_id,)
    )

    current = cur.fetchone()[0]

    if bid_price <= current:
        return jsonify({"status":"Bid too low. Enter a higher price."})

    cur.execute(
        "UPDATE players SET current_price=%s WHERE id=%s",
        (bid_price,player_id)
    )

    cur.execute(
        "INSERT INTO bids(player_id,team_name,bid_price,bid_time) VALUES(%s,%s,%s,%s)",
        (player_id,team,bid_price,datetime.now())
    )

    conn.commit()

    return jsonify({"status":"Bid accepted"})

# -------------------------------
# LOGOUT
# -------------------------------

@app.route("/logout")
def logout():

    session.clear()
    return redirect("/")

# -------------------------------

if __name__ == "__main__":
    app.run(debug=True)
