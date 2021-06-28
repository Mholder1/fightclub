import json
import logging
from os import read


def read_table():
    with open('fightstats.json', 'r') as f:
        return json.loads(f.read())


def input_fightstats():
    # Command line asks user for their name, the name of their opponent and who the victor was
    name = input("Enter your name: ")
    matchup = input("Who was your opponent?: ")
    winner = input("Who claimed victory in this contest?: ")
    name = name.capitalize()
    matchup = matchup.capitalize()
    winner = winner.capitalize()
    return name, matchup, winner


def findPlayer(name):
    HousematesL = read_table()
    nameFound = False
    for person in HousematesL['contestants']:
        if name in person['name']:
            nameFound = True
    return nameFound


def findOpponent(matchup):
    HousematesL = read_table()
    matchupFound = False
    for person in HousematesL['contestants']:
        if matchup in person['name']:
            matchupFound = True
    return matchupFound


def addNew(name):
    HousematesL = read_table()
    HousematesL['contestants'].append({
        "name": name,
        "wins": 0,
        "draws": 0,
        "losses": 0,
    })
    HousematesDumped = json.dumps(HousematesL, indent=2)
    with open('fightstats.json', 'w') as f:
        f.write(HousematesDumped)


def AddOpponent(matchup):
    HousematesL = read_table()
    HousematesL['contestants'].append({
        "name": matchup,
        "wins": 0,
        "draws": 0,
        "losses": 0,
    })
    HousematesDumped = json.dumps(HousematesL, indent=2)
    with open('fightstats.json', 'w') as f:
        f.write(HousematesDumped)


def amend_table(name, matchup, winner):

    HousematesL = read_table()

    for person in HousematesL['contestants']:
        if not findPlayer(name):
            addNew(name)

    for person in HousematesL['contestants']:
        if not findOpponent(matchup):
            AddOpponent(matchup)

    Housemates = read_table()

    draw = False
    if name == winner:
        loser = matchup
        winner = name
    elif matchup == winner:
        winner = matchup
        loser = name
    else:
        draw = True

    for person in Housemates['contestants']:
        if winner in person['name']:
            person['wins'] = person['wins'] + 1

        if loser in person['name']:
            person['losses'] = person['losses'] + 1

        if draw:
            if name in person['name']:
                person['draws'] = person['draws'] + 1
            if matchup in person['name']:
                person['draws'] = person['draws'] + 1

    for value in Housemates:
        sorted_data = sorted(
            Housemates['contestants'], key=lambda numbers: numbers['wins'], reverse=True)
        fightfile = json.dumps({'contestants': sorted_data}, indent=2)

    with open('fightstats.json', 'w') as f:
        f.write(fightfile)

    return read_table()


def log_table():
    loadFile = read_table()
    loadFile = json.dumps(loadFile, indent=2)
    print(loadFile)


def determine_leader():
    loadFile = read_table()
    for person in loadFile['contestants']:
        print("The leader of fightclub is",
              person['name'], "with", person['wins'], "wins")
        break


if __name__ == "__main__":
    name, matchup, winner = input_fightstats()
    amend_table(name, matchup, winner)
    log_table()
    determine_leader()
