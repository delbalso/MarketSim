import random
import pprint

ALL_GOODS = ["apple", "banana", "orange", "water", "land", "clothes", "pear"]

class Collection(object):
    def __init__(self, collection):
        if (collection == None):
            collection = dict()
        self.collection = collection

    def count(self):
        return sum(self.collection.values())

    def printfull(self):
        pprint.pprint(vars(self), indent=5)

    def setValue(self, good, value):
        self.collection[good]=value;

    def getValue(self, good):
        if (self.collection.has_key(good)):
            value = self.collection[good]
        else:
            value = 0
        return value

    def setCollection(self, collection):
        self.collection = collection

    def add_collection(self, collection):
        for good, value in collection.collection.iteritems():
            self.add_item(good, value)

    def remove_collection(self, collection, canBeNegative=False):
        for good, value in collection.collection.iteritems():
            self.add_item(good, -1*value)
            if (canBeNegative==False):
                assert(self.getValue(good)>=0)

    def add_item(self, item, count=1):
        """This is for adding a particular item to the set of possessions, consider upgrading this to a list"""
        if (self.collection.has_key(item)):
            self.setValue(item, self.collection[item] + count)
        else:
            self.setValue(item, count)
        assert(self.getValue(item)>=0)

    @staticmethod
    def generateRandomSet():
        randomSet = dict()
        for good in ALL_GOODS:
            randomSet[good] = int(random.random() * 100)
        return randomSet

class Utility(Collection):
    HUNGRY_UTIL = {"apple":10, "orange":12, "water":2, "land":3, "clothes":1, "pear":9}
    THIRSTY_UTIL = {"apple":1, "orange":2, "water":8, "land":2, "clothes":1, "pear":2}


    def remove_collection(self, collection):
        super(Utility, self).remove_collection(self, collection, canBeNegative=True)

    def __init__(self,util):
        super(Utility,self).__init__(util)

class Possessions(Collection):
    """The set of possessions and actions on a possession for an agent"""
    def __init__(self,possessions):
        super(Possessions,self).__init__(possessions)

    def verifyInventoryForRemove(self, removing_set):
        """Verify that this agent has sufficient inventory to make this trade, i.e. ensure there
        is no negative inventory"""
        for good, quantity in removing_set.collection.iteritems():
            if (self.getValue(good)<quantity):
                return False
        return True

    def random_sample(self, avg_count):
        """Create a random set of possessions, average count is the number of items to expect on average"""
        sample = Possessions(dict());
        for good in self.collection:
            for item in xrange(self.collection[good]):
                rand = random.random()
                value = float(1)/self.count()*avg_count
                if (rand<value):
                    sample.add_item(good)
        return sample


class Agent(object):
    """The basic market agent"""

    def __init__(self,util=None,possessions=None):
        self.utility = Utility(util)
        self.possessions = Possessions(possessions)

    @staticmethod
    def getTotalWealth(agents):
        return sum (agent.getWealth() for agent in agents)

    def assignRandomStats(self, possessions = None, utility = None):
        if (possessions==None):
            self.possessions.setCollection(Collection.generateRandomSet())
        if (utility==None):
            self.utility.setCollection(Collection.generateRandomSet())


    def getWealth(self):
        """This doesn't work given the new possessions class"""
        return self.appraise(self.possessions)

    def appraise(self, goods):
        """Appraises this collection of goods using agent's utility"""
        value = 0
        for good in goods.collection:
            value += goods.getValue(good) * self.utility.getValue(good)
        return value

    def printAgent (self):
        print "     Utility"
        self.utility.printfull()
        print "     Possessions"
        self.possessions.printfull()
        print "\n\n"

    def proposeTrade (self, giving_goods, receiving_goods):
        giving_value = self.appraise(giving_goods)
        receiving_value = self.appraise(receiving_goods)
        if (receiving_value>=giving_value and
                self.possessions.verifyInventoryForRemove(giving_goods)):
            return True
        else:
            return False

    def tradeWith(self, partner, self_package=None, partner_package=None):
        #set self_package to be random if not specified
        if (self_package==None):
            self_items=0
            while(self_items==0):
                self_package = self.possessions.random_sample(1);
                self_items = self_package.count();

        #set partner package to be random if not specified
        if (partner_package==None):
            partner_items=0
            while(partner_items==0):
                partner_package = partner.possessions.random_sample(1);
                partner_items = partner_package.count()

        if (self.proposeTrade(self_package, partner_package) and partner.proposeTrade(partner_package, self_package)):
            #trade
            self.possessions.add_collection(partner_package);
            self.possessions.remove_collection(self_package)

            partner.possessions.add_collection(self_package);
            partner.possessions.remove_collection(partner_package)
            return True

        else:
            #Don't Trade
            return False
        #idea here is to get a random set of possesssions from each party and compare if it would make sense for them to trade.

