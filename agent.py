from orderBook import OrderBook, Order
from exchange import Exchange, Exchanges
import random
import operator
import pprint


class Collection(object):
    def __init__(self, collection):
        if (collection == None):
            collection = dict()
        self.collection = collection

    def count(self):
        return sum(self.collection.values())

    def printFull(self):
        pprint.pprint(vars(self), indent=5)

    def setValue(self, good, value):
        self.collection[good]=value;

    def getValue(self, good):
        if (self.collection.has_key(good)):
            value = self.collection[good]
        else:
            value = 0
        return value

    def addCollection(self, collection):
        for good, value in collection.collection.iteritems():
            self.addItem(good, value)

    def removeCollection(self, collection, canBeNegative=False):
        for good, value in collection.collection.iteritems():
            self.addItem(good, -1*value)
            if (canBeNegative==False):
                assert(self.getValue(good)>=0)

    """This is for adding a particular item to the set of inventory, consider upgrading this to a list"""
    def addItem(self, item, count):
        if (self.collection.has_key(item)):
            assert(self.getValue(item)>=0)
            self.setValue(item, self.collection[item] + count)
        else:
            self.setValue(item, count)
        assert(self.getValue(item)>=0)

    """ removeItem removes items from the inventory """
    def removeItem(self, item, count):
        assert self.getValue(item)>=count, "Tried to remove more items than agent has"
        self.setValue(item, self.collection[item] - count)

class Utility(Collection):
    def __init__(self,util):
        super(Utility,self).__init__(util)

"""The set of inventory and actions on a possession for an agent"""
class Inventory(Collection):
    def __init__(self,inventory):
        super(Inventory,self).__init__(inventory)

    def verifyInventoryForRemove(self, removing_set):
        """Verify that this agent has sufficient inventory to make this trade, i.e. ensure there
        is no negative inventory"""
        for good, quantity in removing_set.collection.iteritems():
            if (self.getValue(good)<quantity):
                return False
        return True


class Agent(object):
    """The basic market agent"""

    def __init__(self, exchanges, util=None, inventory=None):
        self.utility = Utility(util)
        self.inventory = Inventory(inventory)
        self.exchanges = exchanges

    @staticmethod
    def getTotalWealth(agents):
        return sum (agent.getWealth() for agent in agents)

    def getWealth(self):
        """This doesn't work given the new inventory class"""
        return self.appraise(self.inventory)

    """Appraises this collection of goods using agent's utility"""
    def appraise(self, goods):
        value = 0
        for good in goods.collection:
            value += goods.getValue(good) * self.utility.getValue(good)
        return value

    """Prints all members of an agent"""
    def printAgent (self):
        print "*** Utility ***"
        self.utility.printFull()
        print "*** Inventory ***"
        self.inventory.printFull()
        print "\n\n"

    def getUtility (self, good):
        return self.utility.getValue(good)

    """ getInventory returns the number of 'good' in self's inventory """
    def getInventory (self, good):
        return self.inventory.getValue(good)

    """ addInventory adds a good to the agent's inventory. It also adds the order to the the
        releveant exchange if addToExchange is true. addToExchange should almost always be
        true """
    def addInv (self, good, quantity, addToExchange=True):
        self.inventory.addItem(good, quantity)
        if addToExchange:
            order = Order(self, good, self.getUtility(good), quantity, orderType="ask")
            self.exchanges.getExchange(good).addOrder(order)

    def removeInv(self, good, quantity):
        self.inventory.removeItem(good, quantity)

    """ tradeCompleted is called from the exchanges when one of this Agent's orders has been met
        and the trade has been executed. tradeComplete is responsible for adjusting the Agent's
        inventory and self-tracked orders. """
    def tradeCompleted(self, myOrder, otherOrder, good):
        self.exchanges[good].removeOrderNoMatch(myOrder)
        self.removeInv(myOrder.good, myOrder.quantity)

