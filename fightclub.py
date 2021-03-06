import json

def input_fightstats():    
    name = input("Enter your name: ")
    matchup = input("Who was your opponent?: ")
    winner = input("Who claimed victory in this contest?: ")
    name = name.capitalize()
    matchup = matchup.capitalize()
    winner = winner.capitalize()

    with open('fightstats.json', 'r') as f:
        HousematesL = json.loads(f.read())

        draw = False
        if name == winner:
            loser = matchup
            winner = name
        elif matchup == winner:
            winner = matchup
            loser = name
        else:
            draw = True

        for person in range(len(HousematesL['contestants'])):  
            if winner in HousematesL['contestants'][person]['name']:
                HousematesL['contestants'][person]['wins'] = HousematesL['contestants'][person]['wins'] + 1

            if loser in HousematesL['contestants'][person]['name']:
                HousematesL['contestants'][person]['losses'] = HousematesL['contestants'][person]['losses'] + 1

            if draw:
                if name in HousematesL['contestants'][person]['name']:
                    HousematesL['contestants'][person]['draws'] = HousematesL['contestants'][person]['draws'] + 1
                if matchup in HousematesL['contestants'][person]['name']:
                    HousematesL['contestants'][person]['draws'] = HousematesL['contestants'][person]['draws'] + 1

        for value in HousematesL:
            sorted_data = sorted(HousematesL['contestants'], key = lambda numbers: numbers['wins'], reverse=True)
            fightfile = json.dumps({ 'contestants': sorted_data}, indent = 2)


        with open('fightstats.json', 'w') as f:
            f.write(fightfile)
            print(fightfile)
    



if __name__ == "__main__":
    input_fightstats()
    




