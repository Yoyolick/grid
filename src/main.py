import sqlite3
from flask import Flask, render_template
from flask import g, request

DATABASE = "grid.db"

# connecting to our db
def get_db():
    try:
        logmaker("daily").log("database connect", "INTERNAL")
        db = getattr(g, "_database", None)
        if db is None:
            db = g._database = sqlite3.connect(DATABASE)
        return db
    except Exception as e:
        logmaker("daily").log("failure - " + str(e), "INTERNAL")
        return "bad"


# executing a db change
def execute_db(cmd):
    try:
        logmaker("daily").log("database execute", "INTERNAL")
        con = sqlite3.connect(DATABASE)
        c = con.cursor()
        c.execute(cmd)
        con.commit()
    except Exception as e:
        logmaker("daily").log("failure - " + str(e), "INTERNAL")
        return "bad"


# probing db for data
def query_db(query, args=(), one=False):
    try:
        logmaker("daily").log("database query", "INTERNAL")
        cur = get_db().execute(query, args)
        rv = cur.fetchall()
        cur.close()
        return (rv[0] if rv else None) if one else rv
    except Exception as e:
        logmaker("daily").log("failure - " + str(e), "INTERNAL")
        return "bad"


app = Flask(__name__, instance_relative_config=True)


@app.route("/")
def main():
    # create cursor to probe db with
    # cur = get_db().cursor()

    return render_template("index.html")


# on server close execute these commands
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=80, debug=True)
