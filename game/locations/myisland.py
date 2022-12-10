import random
from game.dialogue import converse
from game.dialogue import Character
from game import location
from game import config
from game.display import announce
from game.display import menu
from game.events import *
from game import world
from game.insult_swordfighting import Battle
from game.insult_swordfighting import Enemy


class Island (location.Location):

    def __init__ (self, x, y, w):
        super().__init__(x, y, w)
        self.name = "island"
        self.symbol = 'I'
        self.visitable = True
        self.starting_location = Port_with_ship(self)
        self.locations = {}
        self.locations["port"] = self.starting_location
        self.locations["field"] = Field(self)
        self.locations["mountain"] = Mountaintop(self)
        self.locations["tavern"] = Tavern(self)
        self.locations["house"] = House(self)

    def enter (self, ship):
        print ("You see an island approaching. Rather, You are approaching an island, but still.")

    def visit (self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()

class Port_with_ship (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "port"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self

        self.verbs['talk'] = self

    def enter (self):
        announce ("You arrive at a small port. Your ship is at anchor at a small dock to the south. There is a tall, cheerful looking man waiting at a stand on the dock.")
    
    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            announce ("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["field"]
        elif (verb == "east" or verb == "west"):
            announce ("You look off to the " + verb + ". It's an empty beach. Surely you have something better to do, right?")
        elif verb == "talk":
            announce ("You approach the man, who gleefully smiles at your approach. What would you like to say?")
            converse(Stan())
            


class Field (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "field"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self

        self.verbs['fight'] = self
    def enter (self):
        description = 'You walk into an open field, full of pirates looking for a fight. To the north, you see a large mountain. To the east, you see a winding path. To the west, you see a building with a sign that reads "Scumm Bar".'
        announce (description)
    def process_verb (self, verb, cmd_list, nouns):
        if verb == "south":
            config.the_player.next_loc = self.main_location.locations["port"]
            #eventually this is gonna just be for south, i'll have something else north east and west
        if verb == "north":
            config.the_player.next_loc = self.main_location.locations["mountain"]
        if verb == "east":
            config.the_player.next_loc = self.main_location.locations["house"]
        if verb == "west":
            config.the_player.next_loc = self.main_location.locations["tavern"]
        if verb == "fight":
            battle = Battle(Pirate())
            battle.fight()
            announce(description)

class Mountaintop (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "mountain"
        self.verbs['south'] = self
        
        self.verbs['challenge'] = self
    
    def enter(self):
        description = 'You make your way up the mountain and find yourself at a large, flat arena at its peak. The path back to the base snakes down to the south. A skilled swordswoman stands at its center, awaiting a worthy challenge.'
        announce(description)
        
    def process_verb (self, verb, cmd_list, nouns):
        if verb == "south":
            config.the_player.next_loc = self.main_location.locations["field"]
        if verb == "challenge":
            if len(Battle.known_openings) != 6:
                announce("The Sword Master laughs at your challenge. It seems that you're not even worth her time at your skill level.")

class Tavern (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "tavern"
        self.verbs['east'] = self
        
        self.verbs['talk'] = self
        self.verbs['drink'] = self
        
    def enter(self):
        description = "You enter the Scumm Bar. Unfortunately, the programmer doesn't remember what the Scumm Bar looks like at the moment, so there's nobody to talk to, and nothing to drink. Feel free to show yourself to the door and back east"
        announce(description)
    
    def process_verb (self, verb, cmd_list, nouns):
        if verb == "east":
            config.the_player.next_loc = self.main_location.locations["field"]
        if verb == "talk":
            converse(TavernKeep(False))
        if verb == "drink":
            converse(TavernKeep(True))

class House (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "house"
        self.verbs['west'] = self
        
        self.verbs['talk'] = self

    def enter(self):
        description = "You follow the path to the house of a local cartographer, who sits behind a desk studying his maps. Perhaps he has an idea where your home port is. Otherwise, the path back leads you to the west."
        announce(description)
    
    def process_verb (self, verb, cmd_list, nouns):
        if verb == "west":
            config.the_player.next_loc = self.main_location.locations["field"]
        if verb == "talk":
            converse(Cartographer())
        
#All Characters and Enemy types
class Stan(Character):
    def __init__(self):
        options = {
        "TestPlayer1":"TestStan1",
        "TestPlayer2":"TestStan2",
        "Exit":"TestStanBye"
        }
        super().__init__("Stan", options, "Hello!")

class TavernKeep(Character):
    def __init__(self, shop):
        if shop == True:
            options = {
            "":"",
            "":"",
            "Exit":""
            }
            greeting = "Whatcha buying?"
        else:
            options = {
            "":"",
            "":"",
            "Exit":""
            }
            greeting = "Here to chat?"
        super().__init__("Tavernkeep", options, greeting)

class Cartographer(Character):
    def __init__(self):
        options = {
        "":"",
        "Do you happen to know where my home port is?":"No offense to you, but I'm not exactly keen on giving out maps to random groups of obvious pirates. Perhaps if you could make a name for yourself, that could change.",
        "Exit":"Well, have a good day then, come back if you need anything!"
        }
        if Character.sword_master_beaten == True:
            options["Do you happen to know where my home port is?"] = "Well, if the Sword Master asks for a map, I suppose I can supply one\nYour home coordinates are " + "HOW THE FUCK DO I GET THE HOME COORDINATES?"
            
        super().__init__("Cartographer", options, "Well Hello!")

class Pirate(Enemy):
    def __init__(self):
        n = random.choice(["john", "jon", "jhon"])
        o = []
        r = []
        for k,v in Battle.__MASTER_LIST__.items():
            o.append(k)
            r.append(v)
        super().__init__(n, o, r, random.choice([True, False]))
 
class SwordMaster(Enemy):
    def __init__(self):
        o = ["MasterOpening1", "MasterOpening2" ]
        r = ["MasterResponse1", "MasterResponse2"]
        super().__init__("Sword Master", o, r, True)