from game.display import announce
from game.display import menu
import random

class Insult_Swordfight():
    greetings = ["Arrr!", "*stab in face*"]
    known_openings = ["Arrr!", "*stab in face*"]
    known_responses = []
    __MASTER_LIST__ = {} #dictionary of all opening/response pairings
    def __init__(self, enemy):
        self.name = enemy.name
        self.openings = enemy.openings
        self.responses = enemy.responses
        self.initiative = enemy.initiative
    def converse(self):
        if self.name == "Sword Master"
            announce("Challenged by the Sword Master!")
        else:
            announce("Approached by Wanding Pirate " + self.name + "!")
            if self.initiative == True:
                announce(self.name + ": " + random.choice(openings))
                choice = menu(known_responses)
            else:
                choice = menu(known_openings)
                announce(self.name + ": " + random.choice(responses))
            
        
        
class Enemy:
    def __init__(self, name, openings, responses, initiative):
        self.name = name
        self.openings = openings
        self.responses = responses
        self.initiative = initiative
        
class Pirate(Enemy):
    names = ["john", "jon", "jhon"]
    def __init__(self, name = random.choice(names)):
        openings = ["This is a test!"]
        responses = ["This is a different test!"]
        super().__init__(name, openings, responses, random.choice([True, False])
 
 class SwordMaster(Enemy):
    def __init__(self):
        openings = ["This is a test!"]
        responses = ["This is a different test!"]
        super().__init__("Sword Master", openings, responses, random.choice([True, False])