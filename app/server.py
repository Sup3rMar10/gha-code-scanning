# DELIBERATELY VULNERABLE, for demonstrating code scanning. Do not reuse.
import sqlite3
import subprocess

from flask import Flask, request

app = Flask(__name__)


@app.route("/ping")
def ping():
    host = request.args.get("host", "")
    # Untrusted input is concatenated into a shell command: command injection.
    return subprocess.check_output("ping -c1 " + host, shell=True)


@app.route("/user")
def user():
    name = request.args.get("name", "")
    db = sqlite3.connect("app.db")
    # Untrusted input is formatted into SQL: SQL injection.
    return str(db.execute("SELECT * FROM users WHERE name = '%s'" % name).fetchall())
