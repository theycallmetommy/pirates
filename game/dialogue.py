from game.display import announce
from game.display import menu

def converse(character):
    responses = character.options.values()
    choice = menu(character.options.keys())
    announce(responses[choice])
    


class Character:
    #each character should have a name, and a dictionary of options and responses to choose from
    def __init__(self, name, options):
        self.name = name
        self.options = options

class Stan(Character):
    def __init__(self):
        self.name = "Stan"
        self.options = {"TestPlayer1":"TestStan1", "TestPlayer2":"TestStan2"}