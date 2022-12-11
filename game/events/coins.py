from game import event
from game import config
from game.dialogue import Coinpurse
import random

class FindCoins(event.Event):
    def __init__(self):
        self.name = " crew member finds some coins"
        self.coins = random.randrange(1,16)
        
    def process(self, world):
        c = random.choice(config.the_player.get_pirates())
        result = {}
        if c.lucky == True:
            Coinpurse.coins += (self.coins*2)
            msg = c.get_name() + " found " + str(self.coins*2) + " coins lying around. How lucky!"
        else:
            Coinpurse.coins += self.coins
            msg = c.get_name() + " found " + str(self.coins) + " coins lying around."
        result["message"] = msg
        result["newevents"] = [ self ]
        return result
