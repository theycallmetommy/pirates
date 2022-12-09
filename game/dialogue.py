from game.display import announce
from game.display import menu

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
            break
    


class Character:
    #each character should have a name, and a dictionary of options and responses to choose from
    def __init__(self, name, options, greeting):
        self.name = name
        self.options = options
        self.greeting = greeting