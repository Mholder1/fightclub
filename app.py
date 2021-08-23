from sqlalchemy.orm import backref
import fightclub
import logging
from flask_cors import CORS, cross_origin
from flask import Response
from flask_restful import Api
import json
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import smtplib
import os
from datetime import datetime
from wtforms import SelectField
from flask_wtf import FlaskForm


subscribers = []

app = Flask(__name__)
api = Api(app)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fights.db'
# Initialize the database
db = SQLAlchemy(app)
# Create db model

class Fights(db.Model):

    __tablename__ = 'fighters'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Name %r>' % self.id

class Table(db.Model):

    __tablename__ = 'table'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    wins = db.Column(db.Integer)
    draws = db.Column(db.Integer)
    losses = db.Column(db.Integer)

class Form(FlaskForm):
    first_opponent = SelectField('Select fighter', choices = [])
    second_opponent = SelectField('Select opponent', choices=[])
    victor = SelectField('Select winner', choices=[])

@app.route('/fighters', methods=['POST', 'GET'])
def fighters():
    title = "Here are our fighters"

    if request.method == "POST":
        fighter_name = request.form['name']
        fighter_email = request.form['email']
        fighter_loc = request.form['location']
        
        new_fighter = Fights(name=fighter_name, email=fighter_email, location=fighter_loc)
        new_table = Table(name=fighter_name, wins=0, draws=0, losses=0)

        #Push to Database
        try:
            db.session.add(new_fighter)
            db.session.add(new_table)
            db.session.commit()
            return redirect('/fighters')
        except:
            return "There was an error adding your fighter"
    else:
        fighters = Fights.query.order_by(Fights.date_created)
        return render_template('fighters.html', fighters=fighters, title=title)


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    fighter_to_update = Fights.query.get_or_404(id)
    table_to_update = Table.query.get_or_404(id)

    if request.method == "POST":
        fighter_to_update.name = request.form['name']
        table_to_update.name = request.form['name']
        try:
            db.session.commit()
            return redirect('/fighters')
        except:
            return "There was a problem updating your name"
    else:
        return render_template('update.html', fighter_to_update=fighter_to_update)

@app.route('/delete/<int:id>')
def delete(id):
    fighter_to_delete = Fights.query.get_or_404(id)
    table_to_delete = Table.query.get_or_404(id)

    try:
        db.session.delete(fighter_to_delete)
        db.session.delete(table_to_delete)
        db.session.commit()
        return redirect('/fighters')
    except:
        return "There was a problem deleting fighter"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/form', methods=['POST'])
def form():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email_name = request.form.get("email_name")

    if not first_name or not last_name or not email_name:
        error_statement = "All forms fields required..."
        return render_template("subscribe.html", error_statement=error_statement,
                               first_name=first_name,
                               last_name=last_name,
                               email_name=email_name)

    subscribers.append(f'{first_name} {last_name} | {email_name}')

    return render_template('form.html', subscribers=subscribers)


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
    name = fight_data['name']
    matchup = fight_data['matchup']
    winner = fight_data['winner']
    if winner not in [name, matchup]:
        return Response(json.dumps({"error": "Winner must be either name or opponent."}), 400, mimetype="text/plain")
    if not name or not matchup:
        return Response(json.dumps({"error": "You have not entered a name or an opponent"}), 400, mimetype="text/plain")
    get_data = fightclub.amend_table(
        name.capitalize(), matchup.capitalize(), winner.capitalize())
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

@app.route('/addnew', methods=['GET', 'POST'])
def addnew():
    title = "Add New"

    #form = Form()
    #form.first_opponent.choices = 
    return render_template('addnew.html', title=title)

if __name__ == '__main__':
    enable_logging()
    app.run(debug=True)
