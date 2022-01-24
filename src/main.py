import sqlite3
from flask import Flask, render_template
from flask import g, request
import json

DATABASE = "grid.db"

# connecting to our db
def get_db():
    try:
        db = getattr(g, "_database", None)
        if db is None:
            db = g._database = sqlite3.connect(DATABASE)
        return db
    except Exception as e:
        return "bad"


# executing a db change
def execute_db(cmd):
    try:
        con = sqlite3.connect(DATABASE)
        c = con.cursor()
        c.execute(cmd)
        con.commit()
    except Exception as e:
        print(e)
        return "bad"


# probing db for data
def query_db(query, args=(), one=False):
    try:
        cur = get_db().execute(query, args)
        rv = cur.fetchall()
        cur.close()
        return (rv[0] if rv else None) if one else rv
    except Exception as e:
        return e


app = Flask(__name__, instance_relative_config=True)


@app.route("/")
def main():
    # create cursor to probe db with
    # cur = get_db().cursor()
    """
    for i in range(10000):
        execute_db('insert into main (color) values("#4287f5")')
    """
    return render_template("index.html")


@app.route("/get", methods=["GET", "POST"])
def get():
    return json.dumps(query_db('select * from "main"'))


@app.route("/change", methods=["GET", "POST"])
def change():
    # print("set", request.json["id"], "to", request.json["color"])
    execute_db(
        'update main set color="'
        + request.json["color"]
        + '" where id="'
        + request.json["id"]
        + '"'
    )
    return json.dumps(query_db('select * from "main"'))


# on server close execute these commands
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=80, debug=True)
