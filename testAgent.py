from agent import *
import unittest

HUNGRY_UTIL = {"apple":10, "orange":9, "water":2, "land":3, "clothes":1, "money":1}
THIRSTY_UTIL = {"apple":1, "orange":2, "water":8, "land":2, "clothes":1, "money":1}

def assignRandomStats(agent, inventory = None, utility = None):
    if (inventory==None):
        agent.inventory.setCollection(Collection.generateRandomSet())
    if (utility==None):
        agent.utility.setCollection(Utility.generateRandomSet())

def generateRandUtility():
    randomSet = Collection.generateRandomSet()
    randomSet["money"] = 1
    return randomSet

""" random_sample returns a random sample of an inventory set.  avg_count is the number of items to expect on average"""
def random_sample(set, avg_count):
    sample = inventory(dict());
    for good in set.collection:
        for item in xrange(set.collection[good]):
            rand = random.random()
            value = float(1)/self.count()*avg_count
            if (rand<value):
                sample.addItem(good)
    return sample

""" generateRandomSet generates a set of random goods in random quantities """
def generateRandomSet():
    randomSet = dict()
    for good in ALL_GOODS:
        randomSet[good] = int(random.random() * 100)
    return randomSet

class TestAgent(unittest.TestCase):
    def setUp(self):
        exchanges = Exchanges()
        self.a = Agent(exchanges)
        self.b = Agent (exchanges)

    def test_simpleAddAndRemove(self):
        self.a.addInv("orange",5)
        self.a.addInv("orange",5)
        self.a.addInv("apple",1)
        self.assertTrue(self.a.getInventory("orange") == 10)
        self.assertTrue(self.a.getInventory("apple") == 1)
        self.a.removeInv("orange",5)
        self.a.removeInv("apple",1)
        self.assertTrue(self.a.getInventory("orange") == 5)
        self.assertTrue(self.a.getInventory("apple") == 0)
        self.a.removeInv("orange",5)
        self.assertTrue(self.a.getInventory("orange") == 0)

    # Test needed for flushing agent from marketl
