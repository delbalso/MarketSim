import random
import operator
import pprint

ALL_GOODS = ["apple", "banana", "orange", "water", "land", "clothes", "money"]

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
    HUNGRY_UTIL = {"apple":10, "orange":9, "water":2, "land":3, "clothes":1, "money":1}
    THIRSTY_UTIL = {"apple":1, "orange":2, "water":8, "land":2, "clothes":1, "money":1}

    @staticmethod
    def generateRandomSet():
        randomSet = Collection.generateRandomSet()
        randomSet["money"] = 1
        return randomSet

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
            self.utility.setCollection(Utility.generateRandomSet())


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
        """Prints all members of an agent"""
        print "     Utility"
        self.utility.printfull()
        print "     Possessions"
        self.possessions.printfull()
        print "\n\n"

    """ For a list of goods, have self try to buy as many goods from partner as possible that are being sold for an acceptable price. Uses the partner's minimum sale price """
    def seriesTradeHelper(self, partner, goods):
        for good, ratio in goods:
            if (self.utility.getValue(good)>partner.utility.getValue(good)):
                # Try to get the maximum amount
                number_to_buy = min((self.possessions.getValue("money")-1)/max(partner.utility.getValue(good),1), partner.possessions.getValue(good))
                # note: this chooses the lowest price for the buyer, consider changing this to a more realisistic number
                self_package = Collection({"money": number_to_buy*partner.utility.getValue(good)+1})
                partner_package = Collection({ good : number_to_buy})

                self.trade(partner, self_package, partner_package)


    """ Iterate through all goods, compare utilities of each, attempt trade if there is a
    mismatch """
    def seriesTrade(self, partner):
        # Create a list that holds the ratio of utility for each good for both parties (so the largest self_utility/partner_utility is first)
        utilityRatios = dict((good,float(self.utility.getValue(good))/max(partner.utility.getValue(good),1)) for good in ALL_GOODS)

        # Operate on the biggest utility mismatches first
        goodsUtilityRatios = sorted(utilityRatios.iteritems(), key=operator.itemgetter(1), reverse=True)
        self.seriesTradeHelper(partner, goodsUtilityRatios)
        partner.seriesTradeHelper(self, reversed(goodsUtilityRatios))


    def proposeTrade (self, giving_goods, receiving_goods):
        giving_value = self.appraise(giving_goods)
        receiving_value = self.appraise(receiving_goods)
        if (receiving_value>=giving_value and
                self.possessions.verifyInventoryForRemove(giving_goods)):
            return True
        else:
            return False

    def randomTrade(self, partner):
        """Attempt to trade a totally random package between self and the partner"""
        #set self_package to be random if not specified
        self_items=0
        while(self_items==0):
            self_package = self.possessions.random_sample(1);
            self_items = self_package.count();

        #set partner package to be random if not specified
        partner_items=0
        while(partner_items==0):
            partner_package = partner.possessions.random_sample(1);
            partner_items = partner_package.count()

        return self.trade(partner, self_package, partner_package)

    def trade(self, partner, self_package=None, partner_package=None):
        """Performs a trade between two parties if it's beneficial for both"""
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

