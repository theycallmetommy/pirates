from game.display import announce
from game.display import menu
import random

class Dialogue():
    greetings = ["Arrr!", "*stab in face*"]
    known_openings = ["Arrr!", "*stab in face*"]
    known_insults = []
    def __init__(self, character):
        self.name = character.name
        self.openings = character.openings
        self.insults = character.insults
        self.initiative = character.initiative
    def converse(self):
        if self.name == "Stan":
            pass
        if self.name == "Sword Master"
            pass
        else:
            announce("Approached by Wanding Pirate " + self.name + "!")
            if self.initiative == True:
                announce(self.name + ": " + random.choice(openings))
                choice = menu(known_insults)
                
                
            
        
        
class Character:
    def __init__(self, name, openings, insults, initiative):
        self.name = name
        self.openings = openings
        self.insults = insults
        self.initiative = initiative
    
class Stan(Character):
    def __init__(self):
        openings = ["Well howdy there, welcome to Macaque Island! My name is Stan, and I run this stand here."]
        insults = ["Sounds like you've got some real pirate spirit, that's good! You're gonna need that if you want to make it around here! Enjoy your stay!", "Whoa there, buckaroo! Looks like someone needs to learn the rules around here. Swordfights aren't won with brute strength on this island, they're won by rapier wit! Go get some fights under your belt, you'll see what I mean!"]
        super().__init__("Stan", openings, insults, True)
        
class Pirate(Character):
    names = ["john", "jon", "jhon"]
    def __init__(self, name = random.choice(names)):
        openings = ["This is a test!"]
        insults = ["This is a different test!"]
        super().__init__(name, openings, insults, random.choice([True, False])
 
 class SwordMaster(Character):
    def __init__(self):
        openings = ["This is a test!"]
        insults = ["This is a different test!"]
        super().__init__("Sword Master", openings, insults, random.choice([True, False])