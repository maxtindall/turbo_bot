import sys
import os
import sqlite3
from flask import Flask

# fix import path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import DB_PATH

app = Flask(__name__)

@app.route("/")
def home():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # ALWAYS ensure table exists
    c.execute("""
        CREATE TABLE IF NOT EXISTS trades (
            market TEXT,
            side TEXT,
            price REAL
        )
    """)

    # safely fetch data
    c.execute("SELECT * FROM trades")
    rows = c.fetchall()
    conn.close()

    html = "<h1>Turbo Bot Dashboard</h1>"
    html += "<p>Trades:</p><ul>"

    if not rows:
        html += "<li>No trades yet (run bot.py)</li>"
    else:
        for r in rows:
            html += f"<li>{r}</li>"

    html += "</ul>"
    return html


if __name__ == "__main__":
    app.run(port=5000)
