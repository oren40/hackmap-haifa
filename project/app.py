from pathlib import Path
import sqlite3

from flask import Flask, g, jsonify, render_template, request
from flask_cors import CORS

DB_PATH = Path(__file__).with_name("hackmap.db")

app = Flask(__name__)
CORS(app) 

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_=None):
    if (db := g.pop("db", None)):
        db.close()


@app.route("/")
def root():
    return "HackMap API is alive!"


@app.route("/map")
def map_page():
    return render_template("index.html")


@app.route("/api/events", methods=["GET", "POST"])
def events():
    db = get_db()

    if request.method == "POST":
        j = request.get_json(force=True)
        required = ("title", "category", "date", "lat", "lng")
        if not all(k in j and j[k] for k in required):
            return {"error": "missing field"}, 400

        db.execute(
            """
            INSERT INTO events
            (title, description, category, date, latitude, longitude)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                j["title"],
                j.get("description", ""),
                j["category"],
                j["date"],
                float(j["lat"]),
                float(j["lng"]),
            ),
        )
        db.commit()
        return {"ok": True}, 201

    rows = db.execute("SELECT * FROM events ORDER BY date").fetchall()
    return jsonify([dict(r) for r in rows])
 
if __name__ == "__main__":
    app.run(debug=True)
