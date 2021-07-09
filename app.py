import psycopg2
import fightclub
import fightclub_db
import logging
from flask_cors import CORS, cross_origin
from flask import Response
from flask_restful import Api
import json
from flask import Flask, request, render_template, redirect, url_for
import smtplib
import os
from decouple import config

API_EMAIL = config('EMAIL')
API_PASSWORD = config('PASSWORD')


subscribers = []

app = Flask(__name__)
api = Api(app)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/leaguetable')
def leaguetable():
    return render_template('leaguetable.html')


@app.route('/logins')
def logins():
    return render_template('logins.html')


@app.route('/subscribe')
def subscribe():
    return render_template('subscribe.html')


@app.route('/form', methods=['POST'])
def form():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email_name = request.form.get("email_name")

    message = (f'Thank you {first_name} for subscribing to our newsletter!')
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(API_EMAIL, API_PASSWORD)
    server.sendmail(API_EMAIL, email_name, message)

    if not first_name or not last_name or not email_name:
        error_statement = "All forms fields required..."
        return render_template("subscribe.html", error_statement=error_statement,
                               first_name=first_name,
                               last_name=last_name,
                               email_name=email_name)

    subscribers.append(f'{first_name} {last_name} | {email_name}')

    return render_template('form.html', subscribers=subscribers, message=message)


def post_params_okay(mandatory_fields, req_data):
    for field in mandatory_fields:
        if field in req_data:
            continue
        else:
            return False
    return True


@app.route('/addfight', methods=['POST'])
@cross_origin()
def addfight():
    fight_data = request.get_json(force=True)
    logging.info(f"fight data is {fight_data}")
    if fight_data is None:
        return Response("No fight data posted.", 400, mimetype="text/plain")
    if not request.is_json:
        return Response("Data is not json", 400, mimetype="text/plain")
    if not post_params_okay(("name", "winner", "matchup"), fight_data):
        return Response("Missing field data, must supply name, winner and matchup", 400, mimetype="text/plain")
    get_data = fightclub.amend_table(
        fight_data['name'], fight_data['matchup'], fight_data['winner'])
    return Response(json.dumps(get_data), 200, mimetype='application/json')


@app.route('/gettable')
def gettable():
    table = fightclub.read_table()
    return Response(json.dumps(table), 200, mimetype="application/json")


def enable_logging():
    log_datefmt = '%Y-%m-%d %H:%M:%S'
    log_format = '[%(asctime)s] [fightclub_api] %(levelname)-7s %(message)s'
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger('fightclub_api')
    logger.setLevel(logging.DEBUG)
    logging.basicConfig(level=logging.INFO,
                        datefmt=log_datefmt, format=log_format)


if __name__ == '__main__':
    enable_logging()
    app.run(debug=True)
