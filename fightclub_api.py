import json
from flask import Flask, request, render_template, redirect, url_for
from flask_restful import Api
from flask import Response
import fightclub

app = Flask(__name__)
api = Api(app)

@app.route('/')
def index():
  return render_template('index.html')

def post_params_okay(mandatory_fields, req_data):
    for field in mandatory_fields:
        if field in req_data:
            continue
        else:
            return False
    return True

@app.route('/addfight', methods =['POST'])
def addfight():
    get_data = fightclub.amend_table(name, matchup, winner)
    if addfight:
        return get_data
    fight_data = request.get_json(force=True)
    if fight_data is None:
        return Response("No fight data posted.", 400, mimetype="text/plain")
    if not post_params_okay(("name", "winner", "matchup"), fight_data):
        return Response("Missing field data, must supply name, winner and matchup", 400, mimetype="text/plain")
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


@app.route('/gettable')
def gettable():
    table = fightclub.read_table()
    return Response(json.dumps(table), 200, mimetype="application/json")

if __name__ == '__main__':
  app.run(debug=True)
