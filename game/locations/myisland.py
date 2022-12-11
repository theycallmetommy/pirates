import random
from game.dialogue import converse
from game.dialogue import shop
from game.dialogue import Character
from game.dialogue import Coinpurse
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
        
        self.verbs['coin'] = self
        self.verbs['talk'] = self
        self.verbs['debug'] = self

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
        elif verb == "coin":
            announce ("You have " + str(Coinpurse.coins) + " Macaque Island Treasure Coins.")
        elif verb == "talk":
            announce ("You approach the man, who gleefully smiles at your approach. What would you like to say?")
            converse(Stan())
        elif verb == "debug":
            for k,v in Battle.__MASTER_LIST__.items():
                if k not in Battle.known_openings:
                    Battle.known_openings.append(k)
                if v not in Battle.known_responses:
                    Battle.known_responses.append(v)
            Coinpurse.coins = 999
            announce ("Cheater Cheater Pumpkin Eater")
            


class Field (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "field"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self

        self.verbs['coin'] = self
        self.verbs['fight'] = self
    def enter (self):
        self.description = 'You walk into an open field, full of pirates looking for a fight. To the north, you see a large mountain. To the east, you see a winding path. To the west, you see a building with a sign that reads "Scumm Bar".'
        announce (self.description)
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
        elif verb == "coin":
            announce ("You have " + str(Coinpurse.coins) + " Macaque Island Treasure Coins.")
        if verb == "fight":
            battle = Battle(Pirate())
            battle.fight()
            announce(self.description)

class Mountaintop (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "mountain"
        self.verbs['south'] = self
        
        self.verbs['coin'] = self
        self.verbs['challenge'] = self
    
    def enter(self):
        description = 'You make your way up the mountain and find yourself at a large, flat arena at its peak. The path back to the base snakes down to the south.'
        if Character.sword_master_beaten == False:
            description += ' A skilled swordswoman stands at its center, awaiting a worthy challenge.'
        announce(description)
        
    def process_verb (self, verb, cmd_list, nouns):
        if verb == "south":
            config.the_player.next_loc = self.main_location.locations["field"]
        elif verb == "coin":
            announce ("You have " + str(Coinpurse.coins) + " Macaque Island Treasure Coins.")
        if verb == "challenge":
            if len(Battle.known_openings) < Battle.__SWORD__MASTER__LIMIT__:
                announce("The Sword Master laughs at your challenge. It seems that you're not even worth her time at your skill level.")
            if Character.sword_master_beaten == True:
                announce("You have already earned the title of Sword Master")
            else:
                battle = MasterBattle(SwordMaster())
                battle.fight()
class Tavern (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "tavern"
        self.verbs['east'] = self
        
        self.verbs['coin'] = self
        self.verbs['talk'] = self
        self.verbs['drink'] = self
        
    def enter(self):
        description = "You enter the Scumm Bar. Unfortunately, the programmer doesn't remember what the Scumm Bar looks like at the moment, so there's nobody to talk to, and nothing to drink. Feel free to show yourself to the door and back east"
        announce(description)
    
    def process_verb (self, verb, cmd_list, nouns):
        if verb == "east":
            config.the_player.next_loc = self.main_location.locations["field"]
        elif verb == "coin":
            announce ("You have " + str(Coinpurse.coins) + " Macaque Island Treasure Coins.")
        if verb == "talk":
            converse(TavernKeep())
        if verb == "drink":
            shop(TavernKeep())

class House (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "house"
        self.verbs['west'] = self
        
        self.verbs['coin'] = self
        self.verbs['talk'] = self

    def enter(self):
        description = "You follow the path to the house of a local cartographer, who sits behind a desk studying his maps. Perhaps he has an idea where your home port is. Otherwise, the path back leads you to the west."
        announce(description)
    
    def process_verb (self, verb, cmd_list, nouns):
        if verb == "west":
            config.the_player.next_loc = self.main_location.locations["field"]
        elif verb == "coin":
            announce ("You have " + str(Coinpurse.coins) + " Macaque Island Treasure Coins.")
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
    def __init__(self):
        options = {
        "":"",
        "":"",
        "":"",
        "Exit":""
        }
        greeting = "Here to chat?"
        super().__init__("Tavernkeep", options, greeting)
        self.shopgreeting = "Whatcha buying?"
        self.inventory = {
        "LuckyDrink":30,
        "SicknessDrink":10,
        "InsultDrink":15
        }

# class Drink:
    # def __init__(self, name, price):
        # self.name = name
        # self.price = price
# class LuckyDrink(Drink):
    # def __init__(self):
        # super().__init__("LuckyDrink", 10)
    # def order(self):
        # if Coinpurse.coins >= self.price:
            # Coinpurse.coins -= self.price
            # lucky.LuckyDay().process()
# class SicknessDrink(Drink):
    # def __init__(self):
        # super().__init__("SicknessDrink", 10)
        # #cures one crewmate of Sick
# class InsultDrink(Drink):
    # def __init__(self):
        # super().__init__("InsultDrink", 10)
        # #teaches player one new opening insult

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
        o = [
        "MasterTaunt",
        "MasterOpening1",
        "MasterOpening2",
        "MasterOpening3",
        "MasterOpening4",
        "MasterOpening5",
        "MasterOpening6",
        "MasterOpening7"
        ]
        r = []
        #self.valid_openings = []
        for k,v in Battle.__MASTER_LIST__.items():
            r.append(v)
        #    self.valid_openings.append(k)
        super().__init__("Sword Master", o, r, True)
        
        
class MasterBattle(Battle):
    def init(self, enemy):
        super().__init__(enemy)
    
    def checkFight(self):
        if self.points == 4:
            Character.sword_master_beaten = True
            announce(self.name + " accepts defeat! You earn the title of Sword Master!")
            return True
        elif self.points == -2:
            announce(self.name + " bests you in combat!")
            #punishment for failure? sickness maybe?
            return True
        else:
            return False
    def fight(self):
        points = 0
        self.used_openings = []
        self.valid_openings = []
        for k in Battle.__MASTER_LIST__.keys():
            self.valid_openings.append(k)
        announce("Challenged the Sword Master!")
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
                if choice == 0:
                    announce(self.name + ": MasterTaunt")
                    self.updateStatus("Failure")
                else:
                    player = Battle.known_openings[choice]
                    if player in self.used_openings:
                        announce(self.name + ": I see that your originality matches your skill, you poor excuse for a pirate!")
                        self.updateStatus("Failure")
                    else:
                        self.used_openings.append(player)
                        player = self.valid_openings.index(player)
                        insult = self.responses[player]
                        if random.randrange(0, 2) == 0:
                            announce(self.name + ": " + insult)
                            self.updateStatus("Failure")
                        else:
                            announce(self.name + ": A lucky blow, but you're still no match for my rapier wit!")
                            self.updateStatus("Draw")
                self.initiative = True
        