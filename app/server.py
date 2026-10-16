import sqlite3
import subprocess

from flask import Flask, request

app = Flask(__name__)


@app.route("/ping")
def ping():
    host = request.args.get("host", "")
    if not host.replace(".", "").replace("-", "").isalnum():
        return "bad host", 400
    # No shell, arguments passed as a list, and "--" so a host cannot be read as an option.
    return subprocess.check_output(["ping", "-c1", "--", host])


@app.route("/user")
def user():
    name = request.args.get("name", "")
    db = sqlite3.connect("app.db")
    # Parameterized query: the driver keeps data separate from SQL.
    return str(db.execute("SELECT * FROM users WHERE name = ?", (name,)).fetchall())
