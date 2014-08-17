from agent import *
import unittest

HUNGRY_UTIL = {"apple": 10, "orange": 9,
               "water": 2, "land": 3, "clothes": 1, "money": 1}
THIRSTY_UTIL = {"apple": 1, "orange": 2,
                "water": 8, "land": 2, "clothes": 1, "money": 1}

""" random_sample returns a random sample of an inventory set.  avg_count is the number of items to expect on average"""


def random_sample(set, avg_count):
    sample = inventory(dict())
    for good in set.collection:
        for item in xrange(set.collection[good]):
            rand = random.random()
            value = float(1) / self.count() * avg_count
            if (rand < value):
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
        self.exchange = Exchange()
        self.a = Agent(self.exchange)
        self.b = Agent(self.exchange)
        self.a.utility.collection = HUNGRY_UTIL
        self.b.utility.collection = THIRSTY_UTIL

    def test_getWealthAndGetTotalWealth(self):
        self.a.addInv("orange", 5)
        self.a.addInv("orange", 5)
        self.a.addInv("apple", 5)
        self.assertTrue(self.a.getWealth() == 140)

        self.b.addInv("money", 5)
        self.assertTrue(self.b.getWealth() == 5)

        self.assertTrue(Agent.getTotalWealth([self.a, self.b]) == 145)

    def test_errorWhenRemovingTooMany(self):
        self.a.addInv("orange", 5)
        self.assertRaises(InventoryException, self.a.removeInv, "orange", 6)

    def test_errorWhenAddingOrRemovingNegativeQuantities(self):
        self.assertRaises(InventoryException, self.a.removeInv, "orange", -6)
        self.assertRaises(InventoryException, self.a.addInv, "orange", -6)

    def test_simpleAddAndRemove(self):
        self.a.addInv("orange", 5)
        self.a.addInv("orange", 5)
        self.a.addInv("apple", 1)
        self.assertTrue(self.a.getInv("orange") == 10)
        self.assertTrue(self.a.getInv("apple") == 1)
        self.a.removeInv("orange", 5)
        self.a.removeInv("apple", 1)
        self.assertTrue(self.a.getInv("orange") == 5)
        self.assertTrue(self.a.getInv("apple") == 0)
        self.a.removeInv("orange", 5)
        self.assertTrue(self.a.getInv("orange") == 0)

    def test_removeExchange(self):
        self.a.addInv("orange", 5)
        self.assertTrue(len(self.a.exchange.markets) == 7)
        self.assertTrue(self.a.exchange.getMarket("orange").isEmpty() == False)
        self.a.removeExchange(self.exchange)
        self.assertTrue(self.a.exchange == None)
        self.assertTrue(self.exchange.getMarket("orange").isEmpty() == True)

    def test_addExchange(self):
        self.a.removeExchange(self.exchange)

    # Test needed for flushing agent from marketl
