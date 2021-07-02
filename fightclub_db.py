import psycopg2
import fightclub
import app
import logging
from flask_cors import CORS, cross_origin
from flask import Response
from flask_restful import Api
import json
from flask import Flask, request, render_template, redirect, url_for


app = Flask(__name__)
api = Api(app)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
def index():
    return render_template('index.html')


POSTGRES_URL = "postgres://vtxojwza:iYRO1OEyap8wRAhe_xrGA_-w2Pgvv10p@rogue.db.elephantsql.com/vtxojwza"

connection = psycopg2.connect(POSTGRES_URL)
try:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "CREATE TABLE fight_table (name TEXT, email TEXT);")
except psycopg2.errors.DuplicateTable:
    pass


@app.route('/', methods=['POST', 'GET'])
def info():
    if request.method == "POST":
        print(request.form)
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO fight_table VALUES (%s, %s);",
                    (
                        request.form.get("name"),
                        request.form.get("email"),
                    )
                )
    return render_template("index.html")


@app.route("/logins", methods=['POST', 'GET'])
def show_login():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM fight_table;")
            fight_table = cursor.fetchall()
    return render_template("logins.html", entries=fight_table, indent=2)
