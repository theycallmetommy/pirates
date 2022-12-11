from game.display import announce
from game.display import menu
from game.dialogue import Coinpurse
import random


class Battle:
    known_openings = ["Arrr!"]
    known_responses = ["That the best you can do?"]
    __MASTER_LIST__ = {
    "Arrr!":"That the best you can do?",
    "ExampleOpen1":"ExampleResponse1",
    "ExampleOpen2":"ExampleResponse2",
    "ExampleOpen3":"ExampleResponse3",
    "ExampleOpen4":"ExampleResponse4",
    "ExampleOpen5":"ExampleResponse5",
    "ExampleOpen6":"ExampleResponse6",
    "ExampleOpen7":"ExampleResponse7"
    } #dictionary of all opening/response pairings
    __SWORD__MASTER__LIMIT__ = 6
    def __init__(self, enemy):
        self.name = enemy.name
        self.openings = enemy.openings
        self.responses = enemy.responses
        self.initiative = enemy.initiative
        self.points = 0

    def updateStatus(self, result):
        if result == "Success":
            self.points += 1
            announce("The duel shifts in your favor! Score = " + str(self.points))
        if result == "Failure":
            self.points -= 1
            announce("The tides turn against you! Score = " + str(self.points))
        if result == "Draw":
            announce("You hold your ground! Score = " + str(self.points))
    def checkFight(self):
        if self.points == 3:
            reward = random.randrange(1, 11)
            announce(self.name + " accepts defeat! You earn " + str(reward) + " coins!")
            Coinpurse.coins += reward
            return True
        elif self.points == -3:
            announce(self.name + " chases you off with your tail between your legs!")
            return True
        else:
            return False
    def updateKnown(self, insult):
        if insult in self.openings:
            if insult not in Battle.known_openings:
                Battle.known_openings.append(insult)
        elif insult in self.responses:
            if insult not in Battle.known_responses:
                Battle.known_responses.append(insult)
            
    def fight(self):
        points = 0
        announce("Approached by " + self.name + "!")
        while self.checkFight() != True:
            if self.initiative == True:
                insult = random.choice(self.openings[1:])
                announce(self.name + ": " + insult)
                choice = menu(Battle.known_responses)
                player = Battle.known_responses[choice]
                player = self.responses.index(player)
                if player == self.openings.index(insult):
                    self.updateStatus("Success")
                else:
                    self.updateStatus("Failure")
                self.initiative = False
            else:
                choice = menu(Battle.known_openings)
                player = Battle.known_openings[choice]
                player = self.openings.index(player)
                insult = self.responses[player]
                if choice == 0:
                    announce(self.name + ": " + insult)
                    self.updateStatus("Failure")
                elif insult in Battle.known_responses:
                    announce(self.name + ": How dare you!")
                    self.updateStatus("Success")
                else:
                    announce(self.name + ": " + insult)
                    self.updateStatus("Failure")
                self.initiative = True
            self.updateKnown(insult)
                    
class Enemy:
    def __init__(self, name, openings, responses, initiative):
        self.name = name
        self.openings = openings
        self.responses = responses
        self.initiative = initiative