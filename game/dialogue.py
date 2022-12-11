from game.display import announce
from game.display import menu

class Coinpurse:
    coins = 0

def converse(character):
    choices = []
    responses = []
    for k,v in character.options.items():
        choices.append(k)
        responses.append(v)
    announce(character.name + ' says: "' + character.greeting + '"')
    while True:
        choice = menu(choices)
        announce(character.name + ' says: "' + responses[choice] + '"')
        if choices[choice] == "Exit":
            return

def shop(character):
    choices = []
    items = []
    for k,v in character.inventory.items():
        items.append(k)
        choices.append(str(k) + " - " + str(v))
    announce(character.name + ' says: "' + character.shopgreeting + '"')
    choice = menu(choices)
    if choices[choice] == "Exit":
        announce("TestBye")
        return None
    else:
        item = items[choice]
        price = character.inventory[item]
        if Coinpurse.coins >= price:
            Coinpurse.coins -= price
            announce(character.name + 'says: "Here\'s your ' + item + '"')
            return item
        else:
            announce(character.name + 'says: Not enough coin')
            return None
                
        
    


class Character:
    sword_master_beaten = False
    def __init__(self, name, options, greeting): #each character should have a name, and a dictionary of options and responses to choose from
        self.name = name
        self.options = options
        self.greeting = greeting
        