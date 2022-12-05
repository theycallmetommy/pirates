from game.dialogue import converse
from game.dialogue import Stan
from game import location
from game import config
from game.display import announce
from game.display import menu
from game.events import *

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

    def enter (self, ship):
        print ("arrived at an island")

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
            converse(Stan)
            # greetings = ["Hello.", "Arrr!", "*stab the man*"]
            # choice = menu(greetings)
            # print(choice)
            # if (choice == 0 or choice == 1):
                # announce("The man stares back at you, saying nothing, as he has not been programmed to respond yet.")
            # if choice == 2:
                # announce("The man continues to smile back at you, seemingly unaware of the sword through his stomach. You feel as though you should leave.")


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
        actually_made_people_yet = False
        description = "You walk into an open field."
        if actually_made_people_yet == False:
            description += " There's currently no one to fight, but feel free to try anyways."
        announce (description)
    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south" or verb == "north" or verb == "east" or verb == "west"):
            config.the_player.next_loc = self.main_location.locations["port"]
            #eventually this is gonna just be for south, i'll have something else north east and west
        if verb == "fight":
            announce("You wonder when people will be added to this island. Somehow, somewhere, you hear a programmer sigh.")

