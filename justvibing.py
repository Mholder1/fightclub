import json


def fight_stats():
    Housemates = {}
    names = input("Enter your name: ")
    matchup = input("Who was your opponent?: ")
    winner = input("Who claimed victory in this contest?: ")

    try:

        with open('fightstats.json', 'r') as f:
            Housemates = json.loads(f.read())
            

    except FileNotFoundError:
        pass

    if winner in Housemates:
        Housemates[winner] = Housemates[winner] + 1
    else:
        Housemates[winner] = 1

    fightfile = json.dumps(Housemates)
    
    with open('fightstats.json', 'w') as f:
        f.write(fightfile)




if __name__ == "__main__":
    fight_stats()




