import json


def input_fightstats():    
    names = input("Enter your name: ")
    matchup = input("Who was your opponent?: ")
    winner = input("Who claimed victory in this contest?: ")

    with open('fightstats.json', 'r') as f:
        HousematesL = json.loads(f.read())

        for person in range(len(HousematesL['contestants'])):
            
            if winner in HousematesL['contestants'][person]['name']:
                HousematesL['contestants'][person]['wins'] = HousematesL['contestants'][person]['wins'] + 1
            else:
                pass

            if matchup != winner and names == winner:
                if matchup in HousematesL['contestants'][person]['name']:
                    HousematesL['contestants'][person]['losses'] = HousematesL['contestants'][person]['losses'] + 1
            if names != winner and matchup == winner:
                if names in HousematesL['contestants'][person]['name']:
                    HousematesL['contestants'][person]['losses'] = HousematesL['contestants'][person]['losses'] + 1
            if names != winner:
                if winner != matchup:
                    if names in HousematesL['contestants'][person]['name']:
                        HousematesL['contestants'][person]['draws'] = HousematesL['contestants'][person]['draws'] + 1
                    if matchup in HousematesL['contestants'][person]['name']:
                        HousematesL['contestants'][person]['draws'] = HousematesL['contestants'][person]['draws'] + 1

    fightfile = json.dumps(HousematesL, indent = 2)

    with open('fightstats.json', 'w') as f:
        f.write(fightfile)




if __name__ == "__main__":
    input_fightstats()
    




