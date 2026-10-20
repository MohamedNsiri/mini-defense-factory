"""Intentionally vulnerable app for training. NEVER deploy outside the isolated lab."""
import sqlite3
from flask import Flask, request

app = Flask(__name__)
SECRET_KEY = "hardcoded-secret-123"          # FLAW 1: hardcoded secret (Semgrep)

def db():
    c = sqlite3.connect(":memory:")
    c.execute("create table users(id integer, name text, role text)")
    c.execute("insert into users values (1,'alice','admin'),(2,'bob','user')")
    return c

@app.route("/")
def index():
    return "<h1>Home-made app</h1><a href='/user?name=alice'>user</a> <a href='/hello?name=x'>hello</a>"

@app.route("/user")
def user():
    name = request.args.get("name", "")
    q = f"select * from users where name = '{name}'"   # FLAW 2: SQL injection (Semgrep + ZAP)
    try:
        return str(db().execute(q).fetchall())
    except Exception as e:
        return f"error: {e}", 500

@app.route("/hello")
def hello():
    return f"<p>Hello {request.args.get('name','')}</p>"  # FLAW 3: reflected XSS (ZAP)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)        # FLAW 4: debug mode on
