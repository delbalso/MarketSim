from loggingSetup import *
from orderBook import *
from exchange import Market, Exchange
import random
import operator
import uuid
import pprint


class InventoryException(Exception):
    pass


class Collection(object):

    def __init__(self, collection):
        if (collection == None):
            collection = dict()
        self.collection = dict(collection)

    """ Count returns the number of items in the collection """

    def count(self):
        return sum(self.collection.values())

    """ goods returns the list of all the goods in the collection """

    def goods(self):
        return self.collection.keys()

    def printFull(self):
        pprint.pprint(vars(self), indent=5)

    def setValue(self, good, value):
        self.collection[good] = value

    def getValue(self, good):
        if (self.collection.has_key(good)):
            value = self.collection[good]
        else:
            value = 0
        return value

    def modifyValue(self, item, delta):
        if (self.collection.has_key(item)):
            self.setValue(item, self.collection[item] + delta)
        else:
            self.setValue(item, delta)

    """ empty removes all items from the collection """

    def empty(self):
        for good in self.collection.keys():
            self.collection[good] = 0

    """ addCollection adds all the contents to one collection to another """

    def addCollection(self, collection):
        for good, value in collection.iteritems():
            self.modifyValue(good, value)

    """ removeCollection removes all the contents of one collection from another. This function will crash with an error if you try to remove more of an item than the collection already contains unless canBeNegative is true. """

    def removeCollection(self, collection, canBeNegative=False):
        for good, value in collection.collection.iteritems():
            self.addItem(good, max(-1 * value, 0))
            if (canBeNegative == False):
                assert(self.getValue(good) >= 0)

    """ modifyValue increments/decrements the quantity of item by delta """


class Utility(Collection):

    def __init__(self, util=None):
        super(Utility, self).__init__(util)

"""The set of inventory and actions on a possession for an agent"""


class Inventory(Collection):

    def __init__(self, inventory=None):
        super(Inventory, self).__init__(inventory)

    """ VerifyInventoryForRemove that this agent has sufficient inventory to make this trade, i.e. ensure there is no negative inventory"""

    def verifyInventoryForRemove(self, removing_set):
        for good, quantity in removing_set.collection.iteritems():
            if (self.getValue(good) < quantity):
                return False
        return True


class Agent(object):

    """ Agent is basic market actor """

    def __init__(self, utility=None, inventory=None, location=None):
        self.id = uuid.uuid4()
        self.utility = Utility(utility)
        self.inventory = Inventory()
        self.location = None
        self.exchange = None
        self.setLocation(location)
        if inventory != None:
            for good in inventory.goods():
                self.addInv(good, inventory.getValue(good))

    @staticmethod
    def getTotalWealth(agents):
        return sum(agent.getWealth() for agent in agents)

    def getWealth(self):
        return self.appraise(self.inventory)

    """ setLocation sets where this agent is. It calls methods in Location to update that location's population and updates this agent's exchanges with the exchange that is found in the location being set """

    def setLocation(self, location, world=None):
        assert self.location == None or self in self.location.population
        if self.location != None:
            self.location.removeAgent(self)
            assert self not in self.location.population
        self.location = location
        if self.location != None:
            location.addAgent(self)
        self.removeExchange(self.exchange)
        if self.location != None:
            self.introduceExchange(self.location.exchange)

    def getLocation(self):
        return self.location

    """ appraise returns the value of goods (a collection of goods) according to this agent's utility"""

    def appraise(self, goods):
        value = 0
        for good in goods.collection:
            value += goods.getValue(good) * self.utility.getValue(good)
        return value

    """Prints all members of an agent"""

    def printAgent(self):
        print "Agent: " + str(self.id)
        print "---Utility"
        self.utility.printFull()
        print "---Inventory"
        self.inventory.printFull()
        print "\n\n"

    """ introduceExchange gives the agent access to a new exchange and puts the agents goods for sale on its markets """

    def introduceExchange(self, exchange):
        if self.exchange != None:  # can only have one exchange
            self.removeExchange(self.exchange)
        self.exchange = exchange
        for good in self.inventory.goods():
            if good != "money":
                market = self.exchange.getMarket(good)
                orderToAdd = Order(
                    self, good, self.getUtility(good) + 1, self.getInv(good), ASK_ORDER)
                market.addOrder(orderToAdd)

    """ removeExchange makes an agent no longer able to access that exchange and removes all of the agent's orders from those markets """

    def removeExchange(self, exchange):
        if exchange == None:
            return
        if (self.exchange != exchange):
            # Assumes Agent can only access one exchange
            logging.warning(
                "Tried to remove an exchange from an agent that does not have access to this exchange")
        for market in exchange.markets.values():
            logging.debug(
                "Removing orders for an agent from " + market.good + " market")
            market.removeAllAgentOrders(self)
        self.exchange = None

    def getUtility(self, good):
        return self.utility.getValue(good)

    """ getInv returns the number of 'good' in self's inventory """

    def getInv(self, good):
        return self.inventory.getValue(good)

    """ addInv adds a good to the agent's inventory. It also adds the order to the the
        releveant market if addToExchange is true. addToExchange should almost always be
        true """

    def addInv(self, good, quantity, addToExchange=True):
        if quantity < 0:
            raise InventoryException(
                "Tried to add a negative quantity of " + good)
        self.inventory.modifyValue(good, quantity)
        if addToExchange and good != "money" and self.exchange != None:
            market = self.exchange.getMarket(good)
            if market != None:
                order = Order(
                    self, good, self.getUtility(good) + 1, quantity, orderType=ASK_ORDER)
                market.addOrder(order)

    def removeInv(self, good, quantity):
        if quantity < 0:
            raise InventoryException(
                "Tried to remove a negative quantity of " + good)
        if quantity > self.getInv(good):
            raise InventoryException(
                "Tried to remove more " + good + " than user has")
        # quantity is positive, but need delta to be negative
        self.inventory.modifyValue(good, -1 * quantity)
