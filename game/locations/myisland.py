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
        
        self.event_chance = 50
        self.events.append (seagull.Seagull())
        
        self.talked_to_stan = False

    def enter (self):
        description = "You arrive at a small port. Your ship is at anchor at a small dock to the south, and a path forward to the north. There is a tall, cheerful looking man to TALK to waiting at a stand on the dock."
        if self.talked_to_stan == False:
            description += '\nThe man is wearing a bright purple and blue plaid jacket, and wearing an oversized white hat. He stands at a stand with a sign that says "Stan\'s Previously Owned Islands".'
        announce (description)
    
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
            self.talked_to_stan = True
            announce ("As you approach Stan's Previously Owned Islands, you swear you hear infomercial music coming from somewhere.")
            converse(Stan())
            self.enter()
        elif verb == "debug":
            for k,v in Battle.__MASTER_LIST__.items():
                if k not in Battle.known_openings:
                    Battle.known_openings.append(k)
                if v not in Battle.known_responses:
                    Battle.known_responses.append(v)
            Coinpurse.coins = 999
            announce ("Hey, don't you know that's cheating?")
            


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
        
        self.event_chance = 50
        self.events.append (coins.FindCoins())
        
    def enter (self):
        description = 'You walk into an open field, full of pirates looking for a FIGHT. To the north, you see a large mountain. To the east, you see a winding path towards some houses. To the west, you see a building with a sign that reads "Scumm Bar".'
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
        elif verb == "coin":
            announce ("You have " + str(Coinpurse.coins) + " Macaque Island Treasure Coins.")
        if verb == "fight":
            battle = Battle(Pirate())
            battle.fight()
            self.enter()

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
            description += ' A skilled swordswoman stands at its center, awaiting a worthy CHALLENGE.'
        else:
            description += ' the Former Sword Master sits on the sidelines, still ready for a CHALLENGE.'
        announce(description)
        
    def process_verb (self, verb, cmd_list, nouns):
        if verb == "south":
            config.the_player.next_loc = self.main_location.locations["field"]
        elif verb == "coin":
            announce ("You have " + str(Coinpurse.coins) + " Macaque Island Treasure Coins.")
        if verb == "challenge":
            if len(Battle.known_openings) < Battle.__SWORD__MASTER__LIMIT__:
                announce("The Sword Master laughs at your CHALLENGE. It seems that you're not even worth her time at your skill level.")
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
        
        self.event_chance = 50
        self.events.append (coins.FindCoins())
        
    def enter(self):
        description = "You enter the Scumm Bar. A rotund man in a chef's hat an apron stands behind the bar, if you're looking for someone to TALK to. Otherwise, you can have a seat and get a DRINK. The door behind you leads east back to the field."
        announce(description)
    
    def process_verb (self, verb, cmd_list, nouns):
        if verb == "east":
            config.the_player.next_loc = self.main_location.locations["field"]
        elif verb == "coin":
            announce ("You have " + str(Coinpurse.coins) + " Macaque Island Treasure Coins.")
        if verb == "talk":
            converse(TavernKeep())
        if verb == "drink":
            item = shop(TavernKeep())
            if item != None:
                if item == "Golden Ale":
                    LuckyDrink().order()
                if item == "Medical Swill":
                    SicknessDrink().order()
                if item == "Gasoline Grog":
                    InsultDrink().order()

class House (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "house"
        self.verbs['west'] = self
        
        self.verbs['coin'] = self
        self.verbs['talk'] = self

    def enter(self):
        description = "You follow the path to the house of a local cartographer, who sits behind a desk studying his maps. Perhaps you can TALK to hime and ask if he has an idea where your home port is. Otherwise, the path back leads you to the west."
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
        if len(Battle.known_openings) < Battle.__SWORD__MASTER__LIMIT__:
            hint = "Maybe you should try fighting some of our fine assortment of dangerous pirates. There are plenty of them out there just asking for a battle of wits, and you look like you can use some yourself! Oh, uh, no offense."
        elif Character.sword_master_beaten == False:
            hint = "Have you tried your luck at besting the Sword Master yet? It'll take alot of skill, wit, and maybe a little bit of luck, but I think you've got what it takes to best the challenges of Macaque Island!"
        else:
            hint = "Would you look at that? The Sword Master themself is asking little old Stan here for help! You've just about done all there is to do on Macaque Island for now, I reckon, but I hope you continue to have a great time around here!"
        options = {
        "What is this place?":"It's your lucky day, because you've just landed on the world famous Macaque Island! Currently under the ownership of one Stan S Stanman, but I'm always happy to look at buyers!",
        "What is there to do here?":"The island's still under renovation from the previous owners, but there's still plenty of activities to sink your teeth into. You can test your wit against the dastardly pirates roaming the place, have a drink at the SCUMM Bar, or even challenge the legendary Sword Master herself!",
        "Do you know where my home port is?":"I barely know who YOU are! I'm Stan by the way, pleasure to meet you! Anyways, I suppose that maybe the local cartographer might be able to help you out with that. But why would you need some dusty old map, when you've got all the fun you can ask for on Macaque Island?",
        "Do you have anything to trade?":"Oh no, not me at the very least. The SCUMM Bar is always open though, just be sure to stock up on Macaque Island Treasure Coins from the pirates. It's the only kind of coin we take out here!",
        "I need some help, Stan.":hint,
        "Goodbye":"You folk have fun now, enjoy the wonderful Macaque Island!"
        }
        super().__init__("Stan", options, "Well, don't you look like a interesting cast of characters? The name's Stan!")

class TavernKeep(Character):
    def __init__(self):
        options = {
        "I'm here for a drink!":"Well then, how's about you actually sit down and ask for a DRINK, 'stead of walkin' up and talkin' to me like this?",
        "What kind of drinks do you serve here?":"Well, We've got a few good drinks 'round here, all me own personal recipes too! There's one that I sprinkle a bit o' gold in to give you some good luck. There's one I mix with the medicine we pick up from Stan's place, just be careful about the expired stuff. Then there's my favorite one, mixed it in with some gasoline to really give ye that flamin' tongue, ye see!",
        "What's a Macaque Island Treasure Coin?":"Issat what 'e wants to call 'em now? Sounds like one of Stan's ol' schemes to make some money offa this place. We take em just like ordinary coin 'round here, so feel free to bring all ye manage to get here.",
        "Goodbye":"Come back when ye feel like gettin' a DRINK next time!"
        }
        greeting = "Welcome to the SCUMM Bar, mate. You 'ere to chat?"
        super().__init__("Tavernkeep", options, greeting)
        self.shop_greeting = "Whatcha' buying?"
        self.inventory = {
        "Golden Ale":30,
        "Medical Swill":10,
        "Gasoline Grog":15
        }

class Drink:
    def __init__(self, description, effect):
        self.description = description
        self.effect = effect
    def order(self):
        announce(self.description)
        announce(self.effect)
        
class LuckyDrink(Drink):
    def __init__(self):
        c = random.choice(config.the_player.get_pirates())
        c.lucky = True
        effect = c.get_name() + " is feeling lucky!"
        super().__init__("The crew finishes up their drinks, picking some flecks of edible gold out of their teeth", effect)
class SicknessDrink(Drink):
    def __init__(self):
        cured = []
        sickened = []
        effect = ""
        for c in config.the_player.get_pirates():
            if random.randrange(1, 101) > 80:
                if c.sick == False:
                    c.set_sickness(True)
                    sickened.append(c.get_name())
            else:
                if c.sick == True:
                    c.set_sickness(False)
                    cured.append(c.get_name())
        if cured != []:
            effect += " and ".join(cured)
            effect += " felt better! "
        if sickened != []:
            effect += " and ".join(sickened)
            effect += " felt worse!"
        if effect == "":
            effect = "You don't think anything happened..."
        super().__init__("The drink tastes like toothpaste, but it goes down easy enough.", effect)
class InsultDrink(Drink):
    def __init__(self):
        effect = ""
        learned = False
        for k in Battle.__MASTER_LIST__.keys():
            if learned == False:
                if k not in Battle.known_openings:
                    learned = True
                    Battle.known_openings.append(k)
                    Battle.known_responses.append(Battle.__MASTER_LIST__[k])
                    effect = "You feel like you've gotten better at insulting people."
        if effect == "":
            effect = "You don't feel like anything happened..."
        super().__init__("You're not sure if a drink can taste insulting, but if it could, it would taste like this.", effect)

class Cartographer(Character):
    def __init__(self):
        options = {
        'Can I buy a map from you?":"With what? Stan\'s fancy "Treasure Coins"? No thank you, I think I\'ll be fine without them.',
        "Do you happen to know where my home port is?":"No offense to you, but I'm not exactly keen on giving out maps to random groups of obvious pirates. Perhaps if you could make a name for yourself, that could change.",
        "Exit":"Well, have a good day then, come back if you need anything!"
        }
        if Character.sword_master_beaten == True:
            options["Do you happen to know where my home port is?"] = "Well, if the Sword Master asks for a map, I suppose I can supply one\nYour home coordinates are " + "HOW THE FUCK DO I GET THE HOME COORDINATES?"
            
        super().__init__("Cartographer", options, "Well Hello!")

class Pirate(Enemy):
    def __init__(self):
        n = random.choice(["John", "Carla", "Cobb", "Otis", "Biff", "Estevan", "Meathook", "Lemonhead"])
        o = []
        r = []
        for k,v in Battle.__MASTER_LIST__.items():
            o.append(k)
            r.append(v)
        super().__init__(n, o, r, random.choice([True, False]))
 
class SwordMaster(Enemy):
    def __init__(self):
        if Character.sword_master_beaten == False:
            n = "Sword Master"
        else:
            n = "Former Sword Master"
        o = [
        "Placeholder",
        "I will milk every drop of blood from your body!",
        "My wisest enemies run away at the first sight of me!",
        "Only once have I met such a coward!",
        "No one will ever catch ME fighting as badly as you do.",
        "There are no clever moves that can help you now.",
        "My sword is famous all over the Caribbean!",
        "Every word you say to me is stupid."
        ]
        r = []
        #self.valid_openings = []
        for k,v in Battle.__MASTER_LIST__.items():
            r.append(v)
        #    self.valid_openings.append(k)
        super().__init__(n, o, r, True)
        
        
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
        if Character.sword_master_beaten == False:
            announce("Challenged the Sword Master!")
        else:
            announce("Rematched the Former Sword Master!")
        points = 0
        self.used_openings = []
        self.valid_openings = []
        for k in Battle.__MASTER_LIST__.keys():
            self.valid_openings.append(k)
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
                    announce(self.name + ": Do you truly have no wit left in your arsenal?")
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
                        if self.lucky == True:
                            if random.randrange(0, 5) == 0:
                               announce(self.name + ": " + insult)
                               self.updateStatus("Failure")
                            else:
                                announce(self.name + ": A lucky blow, but you're still no match for my rapier wit!")
                                self.updateStatus("Draw")
                        else:   
                            if random.randrange(0, 2) == 0:
                                announce(self.name + ": " + insult)
                                self.updateStatus("Failure")
                            else:
                                announce(self.name + ": A lucky blow, but you're still no match for my rapier wit!")
                                self.updateStatus("Draw")
                self.initiative = True
        