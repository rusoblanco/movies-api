import sqlite3
import flask
from flask import jsonify, request

app = flask.Flask(__name__)
app.config["DEBUG"] = True


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route("/", methods=["GET"])
def home():
    return """<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of Sitges festival films.</p>"""

@app.route("/films/all", methods=["GET"])
def api_all():
    conn = sqlite3.connect("../db/films.db")
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_films = cur.execute("SELECT * FROM films;").fetchall()

    return jsonify(all_films)


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route("/films", methods=["GET"])
def api_filter():
    query_parameters = request.args

    id = query_parameters.get("id")
    year = query_parameters.get("year")
    title = query_parameters.get("title")

    query = "SELECT * FROM films WHERE"
    to_filter = []

    if id:
        query += " id=? AND"
        to_filter.append(id)
    if year:
        query += " year=? AND"
        to_filter.append(year)
    if title:
        query += " title=? AND"
        to_filter.append(title)
    if not (id or year or title):
        return page_not_found(404)

    query = query[:-4] + ";"

    conn = sqlite3.connect("../db/films.db")
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)


app.run()
