import json
import logging


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


def addNew(name, matchup, winner):
    HousematesL = read_table()
    draw = False
    if name == winner:
        loser = matchup
        winner = name
    elif matchup == winner:
        winner = matchup
        loser = name
    else:
        draw = True

    winnerFound = False
    loserFound = False

    for person in HousematesL['contestants']:
        if winner in person['name']:
            winnerFound = True
        if loser in person['name']:
            loserFound = True
    if winnerFound != True:
        HousematesL['contestants'].append({
            "name": winner,
            "wins": 1,
            "draws": 0,
            "losses": 0,
        })

    if loserFound != True:
        HousematesL['contestants'].append({
            "name": loser,
            "wins": 0,
            "draws": 0,
            "losses": 1,
        })

    HousematesDumped = json.dumps(HousematesL, indent=2)
    with open('fightstats.json', 'w') as f:
        f.write(HousematesDumped)


def addNewDraw(name, matchup):
    HousematesL = read_table()
    for person in range(len(HousematesL['contestants'])):
        if name in HousematesL['contestants'][person]['name']:
            return True
        if matchup in HousematesL['contestants'][person]['name']:
            return True

    if name != True:
        HousematesL['contestants'].append({
            "name": name,
            "wins": 0,
            "draws": 1,
            "losses": 0,
        })

    if matchup != True:
        HousematesL['contestants'].append({
            "name": matchup,
            "wins": 0,
            "draws": 1,
            "losses": 0,
        })

    HousematesDumped = json.dumps(HousematesL, indent=2)
    with open('fightstats.json', 'w') as f:
        f.write(HousematesDumped)


def amend_table(name, matchup, winner):

    HousematesL = read_table()
    # HousematesL is the file that contains the json data

    draw = False
    if name == winner:
        loser = matchup
        winner = name
        # if the name that was entered as victorious was the name of the user,
        # 'loser' variable is the opponent

    elif matchup == winner:
        winner = matchup
        loser = name
        # if the name that was entered as victorious was the name of the opponent,
        # 'loser' variable is the user
    else:
        draw = True
        # any other scenario of inputs from the user leads to a draw

    for person in range(len(HousematesL['contestants'])):
        if winner in HousematesL['contestants'][person]['name']:
            HousematesL['contestants'][person]['wins'] = HousematesL['contestants'][person]['wins'] + 1

        if loser in HousematesL['contestants'][person]['name']:
            HousematesL['contestants'][person]['losses'] = HousematesL['contestants'][person]['losses'] + 1

   # if the name of the loser is found in 'name', that persons losses increase by 1

        if draw:
            if name in HousematesL['contestants'][person]['name']:
                HousematesL['contestants'][person]['draws'] = HousematesL['contestants'][person]['draws'] + 1
            if matchup in HousematesL['contestants'][person]['name']:
                HousematesL['contestants'][person]['draws'] = HousematesL['contestants'][person]['draws'] + 1

    for value in HousematesL:
        sorted_data = sorted(
            HousematesL['contestants'], key=lambda numbers: numbers['wins'], reverse=True)
        fightfile = json.dumps({'contestants': sorted_data}, indent=2)

        # looping through each item in json data, this sorts the file by wins in descending order
        # and dumping the sorted data to a file

    with open('fightstats.json', 'w') as f:
        f.write(fightfile)
        print(fightfile)


if __name__ == "__main__":
    name, matchup, winner = input_fightstats()
    amend_table(name, matchup, winner)
    addNew(name, matchup, winner)
    addNewDraw(name, matchup)
