from sqlalchemy.orm import backref
import logging
from flask_cors import CORS, cross_origin
from flask import Response
from flask_restful import Api
import json
from flask import Flask, Request, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import smtplib
import os
from datetime import datetime
from wtforms import SelectField
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
import base64
import random
from random import randrange
from math import fabs


subscribers = []


application = Flask(__name__)
api = Api(application)
CORS(application)
application.config['CORS_HEADERS'] = 'Content-Type'
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fights.db'
application.config['SECRET_KEY'] = 'cairocoders-ednalan'

# Initialize the database
db = SQLAlchemy(application)
# Create db model

class Fights(db.Model):

    __tablename__ = 'fighters'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    img = db.Column(db.Text, unique=True, nullable=False)
    pic_name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
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



@application.route('/fighters', methods=['POST', 'GET'])
def fighters():
    title = "Our current fighters"
    fighters = Fights.query.order_by(Fights.date_created)
    return render_template('fighters.html', fighters=fighters, title=title)

@application.route('/viewphoto/<int:id>', methods=['POST', 'GET'])
def viewphoto(id):
    user_info = Fights.query.filter_by(id=id).first()
    image = base64.b64encode(user_info.img).decode('ascii')
    records = Table.query.filter_by(id=id).first()
    return render_template('viewphoto.html', image=image, information=user_info, records=records)
    
    
@application.route('/addphoto/<int:id>', methods=['POST', 'GET'])
def addphoto(id):
    photo_to_update = Fights.query.get_or_404(id)

    if request.method == "POST":
        photo_to_update.img = request.form['file']
        try:
            db.session.commit()
            return redirect('/fighters')
        except:
            return "There was a problem updating your photo"
    else:
        return render_template('addphoto.html', photo_to_update=photo_to_update)

@application.route('/update/<int:id>', methods=['POST', 'GET'])
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

@application.route('/delete/<int:id>')
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

@application.route('/newfighter', methods=['POST', 'GET'])
def newfighter():
    title = "Create your user profile"
    
    #Push to Database
    try:
        if request.method == 'POST':
            pic = request.files['file']
            fighter_name = request.form['name']
            fighter_email = request.form['email']
            fighter_loc = request.form['location']

            if not pic or not fighter_name or not fighter_email or not fighter_loc:
                error_msg = "Please complete all fields"
                return render_template('newfighter.html', title=title, error_msg=error_msg, pic=pic, fighter_name=fighter_name,
                fighter_email=fighter_email, fighter_loc=fighter_loc)
        
        
            filename = secure_filename(pic.filename)
            mimetype = pic.mimetype
            new_fighter = Fights(name=fighter_name, email=fighter_email, 
            location=fighter_loc, img=pic.read(), pic_name=filename, mimetype=mimetype)
            new_table = Table(name=fighter_name, wins=0, draws=0, losses=0)

            db.session.add(new_fighter)
            db.session.add(new_table)
            db.session.commit()
            victory_statement = "Thank you. Your details has been recorded"
            fighters = Fights.query.order_by(Fights.date_created)
            return render_template('newfighter.html', fighters=fighters, success=victory_statement, title=title)
    except Exception as e:
        return f"There was an error adding your fighter {e}"
    else:
        return render_template('newfighter.html')



@application.route('/')
def index():
    return render_template('index.html')


def enable_logging():
    log_datefmt = '%Y-%m-%d %H:%M:%S'
    log_format = '[%(asctime)s] [fightclub_api] %(levelname)-7s %(message)s'
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger('fightclub_api')
    logger.setLevel(logging.DEBUG)
    logging.basicConfig(level=logging.INFO,
                        datefmt=log_datefmt, format=log_format)


class Form(FlaskForm):
    first_opponent = SelectField('Select fighter', choices = [])
    second_opponent = SelectField('Select opponent', choices=[])
    victor = SelectField('Select winner', choices=[])

@application.route('/addnew', methods=['GET', 'POST'])
def addnew():
    title = "Add New"

    victory_statement=""
    loss_statement=""
    draw_statement=""
    congrat_statement=""
    tie_statement=""
    playertwo_statement=""

    tables = Table.query.order_by(Table.wins.desc())
    
    form = Form()
    form.first_opponent.choices = [(Table.id, Table.name) for Table in Table.query.all()]
    form.second_opponent.choices = [(Table.id, Table.name) for Table in Table.query.all()]
 

    if request.method == 'POST':
        PlayerOne = Table.query.filter_by(id=form.first_opponent.data).first()
        PlayerTwo = Table.query.filter_by(id=form.second_opponent.data).first()

        winner = False
        draw = False
        
        user1Guess = request.form['pick_number']
        if not user1Guess:
            guess_error = "Please fill in a number"
            return render_template('addnew.html', guess_error=guess_error, title=title, form=form, tables=tables)
        user2Guess = randrange(1,11)
        try:
            user1Guess = int(user1Guess)
        except Exception as e:
            guess_error = "Guess must be a number"
            return render_template('addnew.html', guess_error=guess_error, title=title, form=form, tables=tables)
        computerGuess = randrange(1,11)
        u1diff = fabs(computerGuess-user1Guess)
        u2diff = fabs(computerGuess-user2Guess)

        if u1diff == u2diff:
            draw = True
        elif u1diff < u2diff:
            winner = True
        else:
            winner = False

        if PlayerOne == PlayerTwo:
            db_error = "You cannot fight yourself"
            return render_template('addnew.html', db_error=db_error, title=title, form=form, tables=tables)
        elif user1Guess > 10:
            guess_error = "Guess must be between 1 and 10"
            return render_template('addnew.html', guess_error=guess_error, title=title, form=form, tables=tables)
        elif user1Guess < 1:
            guess_error = "Guess must be between 1 and 10"
            return render_template('addnew.html', guess_error=guess_error, title=title, form=form, tables=tables)
        

        
        user1Guess = str(user1Guess)
        user2Guess = str(user2Guess)
        computerGuess = str(computerGuess)
        
        print(computerGuess)
        details = "You guessed %s, the hidden number was %s and your opponent guessed %s" % (user1Guess, computerGuess, user2Guess)
        if winner == True:
            victory_statement = "You win!"
            congrat_statement = "Congratulations %s! A win has been credited to your record" % (PlayerOne.name)
            PlayerOne.wins = PlayerOne.wins + 1
            PlayerTwo.losses = PlayerTwo.losses + 1
        elif draw == True:
            PlayerOne.draws = PlayerOne.draws + 1
            PlayerTwo.draws = PlayerTwo.draws + 1
            draw_statement = "It's a tie!"
            tie_statement = "%s and %s, a draw has been added to each of your records" % (PlayerOne.name, PlayerTwo.name)
        else:
            loss_statement = "You lose!"
            playertwo_statement = "Congratulations %s! A win has been credited to your record" % (PlayerTwo.name)
            PlayerOne.losses = PlayerOne.losses + 1
            PlayerTwo.wins = PlayerTwo.wins + 1
        db.session.commit()
        
        return render_template('addnew.html', victory_statement=victory_statement, title=title,
         form=form, tables=tables, loss_statement=loss_statement, draw_statement=draw_statement, details=details, congrat_statement=congrat_statement,
         tie_statement=tie_statement, playertwo_statement=playertwo_statement)
    
    return render_template('addnew.html', title=title, form=form, tables=tables)


if __name__ == '__main__':
    enable_logging()
    application.run(host='0.0.0.0', port=8080, debug=True)
