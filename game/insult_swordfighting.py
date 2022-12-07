from game.display import announce
from game.display import menu
import random


class Insult_Swordfight:
    known_openings = ["Arrr!", "*stab in face*"]
    known_responses = ["How dare you!", "*stab in face*"]
    __MASTER_LIST__ = {"ExampleOpen1":"ExampleResponse1", "ExampleOpen2":"ExampleResponse2"} #dictionary of all opening/response pairings
    def __init__(self, enemy):
        self.name = enemy.name
        self.openings = enemy.openings
        self.responses = enemy.responses
        self.initiative = enemy.initiative
    def fight(self):
        points = 0
        announce("Approached by " + self.name + "!")
        while points != (2 or -2):
            if self.initiative == True:
                announce(self.name + ": " + random.choice(self.openings))
                choice = menu(Insult_Swordfight.known_responses)
                if Insult_Swordfight.known_responses[choice] != "*stab in face*":
                    announce("Success")
                    points += 1
                else:
                    announce("Failure")
                    points -= 1
            else:
                choice = menu(Insult_Swordfight.known_openings)
                announce(self.name + ": " + random.choice(self.responses))
                if Insult_Swordfight.known_responses[choice] != "*stab in face*":
                    points += 1
                else:
                    points -= 1
        
        
class Enemy:
    def __init__(self, name, openings, responses, initiative):
        self.name = name
        self.openings = openings
        self.responses = responses
        self.initiative = initiative