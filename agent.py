import random
import pprint
import goods

class Collection(object):
    def __init__(self, collection):
        self.collection = collection

    def count(self):
        return sum(self.collection.values())

    def printfull(self):
        pprint.pprint(vars(self), indent=5)

    def setValue(self, good, value):
        self.collection[good]=value;

    def getValue(self, good):
        value = 0
        if (self.collection[good]>0):
            value = self.collection[good]
        return value

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

class GoodsUtility(Collection):
    HUNGRY_UTIL = {"apple":10, "orange":12, "water":2, "land":3, "clothes":1, "pear":9}
    THIRSTY_UTIL = {"apple":1, "orange":2, "water":8, "land":2, "clothes":1, "pear":2}

    def remove_collection(self, collection):
        super(GoodsUtility, self).remove_collection(self, collection, canBeNegative=True)

    def __init__(self,util):
        super(GoodsUtility,self).__init__(util)

class Possessions(Collection):
    """The set of possessions and actions on a possession for an agent"""
    def __init__(self,possessions):
        super(Possessions,self).__init__(possessions)

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

    def __init__(self,util):
        self.utility = GoodsUtility(util)
        self.possessions = Possessions(dict())

    def getWealth(self):
        """This doesn't work given the new possessions class"""
        return self.appraise(self.possessions)

    def appraise(self, goods):
        """Appraises this collection of goods using agent's utility"""
        value = 0
        for good in goods.collection:
            value += goods.getValue(good) * self.utility.getValue(good)
        return value

    def printFull (self):
        print "     Utility"
        self.utility.printfull()
        print "     Possessions"
        self.possessions.printfull()
        print "\n\n"

    def proposeTrade (self, giving_goods, receiving_goods):
        giving_value = self.appraise(giving_goods)
        receiving_value = self.appraise(receiving_goods)
        if (receiving_value>=giving_value):
            return True
        else:
            return False

    def tradeWith(self, partner):
        self_items=0
        while(self_items==0):
            self_package = self.possessions.random_sample(1);
            self_items = self_package.count();

        partner_items=0
        while(partner_items==0):
            partner_package = partner.possessions.random_sample(1);
            partner_items = partner_package.count()

        print "###self_items"
        self_package.printfull();
        print "###package_items"
        partner_package.printfull();

        if (self.proposeTrade(self_package, partner_package) and partner.proposeTrade(partner_package, self_package)):
            #trade
            print "Trading now..."
            print "self value ", self.getWealth(), " self possessions before"
            self.possessions.printfull()
            print "partner wealth ", partner.getWealth(), " partner possessions before"
            partner.possessions.printfull()

            self.possessions.add_collection(partner_package);
            self.possessions.remove_collection(self_package)

            partner.possessions.add_collection(self_package);
            partner.possessions.remove_collection(partner_package)
            print "###TRADE###"
            print "self value ", self.getWealth(), " self possessions after"
            self.possessions.printfull()
            print "partner wealth ", partner.getWealth(), " partner possessions after"
            partner.possessions.printfull()
            print "Trade completed"

            return True

        else:
            """Don't Trade"""
            return False
        #idea here is to get a random set of possesssions from each party and compare if it would make sense for them to trade.

