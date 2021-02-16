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
    


    with open('fightstats.json', 'r') as f:
      
        HousematesL = json.loads(f.read())
        print(type(HousematesL))
        for s in range(len(HousematesL)):
            if winner in HousematesL['contestants']['name']:
                HousematesL['contestants']['wins'] = HousematesL['contestants']['wins'] + 1
            else:
                HousematesL['contestants']['wins'] = 1

    fightfile = json.dumps(HousematesL)

    with open('fightstats.json', 'w') as f:
        f.write(fightfile, indent=2)




if __name__ == "__main__":
    fight_stats()




