from agent import *
import unittest

HUNGRY_UTIL = {"apple": 10, "orange": 9,
               "water": 2, "land": 3, "clothes": 1, "money": 1}
THIRSTY_UTIL = {"apple": 1, "orange": 2,
                "water": 8, "land": 2, "clothes": 1, "money": 1}


class FakeAgent:

    def __init__(self):
        self.id = 0
        self.exchange = None

    def tradeCompleted(self, order1, order2, good):
        pass

    def addInv(self, good, quantity):
        pass

    def removeInv(self, good, quantity):
        pass


class TestMarket(unittest.TestCase):

    def setUp(self):
        self.market = Market("apple")
        self.sampleOrders = {}
        self.fakeAgents = {}
        self.exchange = Exchange()

        self.realAgent1 = Agent(
            self.exchange, utility=HUNGRY_UTIL, inventory=Inventory({"money": 100}))
        self.realAgent2 = Agent(
            self.exchange, utility=THIRSTY_UTIL, inventory=Inventory({"apple": 1}))
        self.fakeAgents[0] = FakeAgent()
        self.fakeAgents[1] = FakeAgent()
        self.fakeAgents[2] = FakeAgent()
        self.fakeAgents[3] = FakeAgent()
        self.fakeAgents[4] = FakeAgent()
        self.sampleOrders[0] = Order(
            self.fakeAgents[0], "apple", 100, 1, time=1)
        self.sampleOrders[1] = Order(
            self.fakeAgents[1], "apple", 150, 3, time=4)
        self.sampleOrders[2] = Order(
            self.fakeAgents[2], "apple", 300, 6, time=1)
        self.sampleOrders[3] = Order(
            self.fakeAgents[3], "apple", 150, 5, time=1)

    def test_agentsInventoryAffectedByTrade(self):
        bidOrder = Order(self.realAgent1, "apple", self.realAgent1.getUtility(
            "apple"), 10, orderType="bid")

        self.assertTrue(self.realAgent2.getInv("apple") == 1)
        self.assertTrue(self.realAgent2.getInv("money") == 0)
        self.assertTrue(self.realAgent1.getInv("apple") == 0)
        self.assertTrue(self.realAgent1.getInv("money") == 100)

        appleMarket = self.exchange.getMarket("apple")
        appleMarket.addOrder(bidOrder)

        self.assertTrue(self.realAgent2.getInv("apple") == 0)
        self.assertTrue(self.realAgent2.getInv("money") == 6)
        self.assertTrue(self.realAgent1.getInv("apple") == 1)
        self.assertTrue(self.realAgent1.getInv("money") == 94)

    def test_add(self):
        self.market.addOrders(list(self.sampleOrders.values()))
        for sampleOrder in self.sampleOrders.values():
            # check that all added orders are present
            self.assertTrue(sampleOrder in self.market.bids.book)
            self.assertFalse(sampleOrder in self.market.asks.book)

    def test_simpleAddMatchedBidOffer(self):
        for index in self.sampleOrders.keys():
            self.sampleOrders[index].orderType = "ask"
        self.market.addOrders(list(self.sampleOrders.values()))
        order = Order(self.fakeAgents[3], "apple",  100, 1, orderType="bid")
        self.market.addOrder(order)
        self.assertFalse(self.sampleOrders[0] in self.market.asks.book)
        self.assertTrue(self.sampleOrders[1] in self.market.asks.book)
        self.assertTrue(self.sampleOrders[2] in self.market.asks.book)
        self.assertTrue(self.sampleOrders[3] in self.market.asks.book)
        self.assertTrue(self.market.bids.book.is_empty())

    def test_simpleAddMatchedAskOffer(self):
        self.market.addOrders(list(self.sampleOrders.values()))
        order = Order(self.fakeAgents[3], "apple", 300, 6, orderType="ask")
        self.market.addOrder(order)
        self.assertTrue(self.sampleOrders[0] in self.market.bids.book)
        self.assertTrue(self.sampleOrders[1] in self.market.bids.book)
        self.assertFalse(self.sampleOrders[2] in self.market.bids.book)
        self.assertTrue(self.sampleOrders[3] in self.market.bids.book)
        self.assertTrue(self.market.asks.book.is_empty())

    def test_NoFill(self):
        self.sampleOrders[2].orderType = "ask"
        self.market.addOrders(list(self.sampleOrders.values()))
        self.assertTrue(self.sampleOrders[1] in self.market.bids.book)
        self.assertTrue(self.sampleOrders[3] in self.market.bids.book)
        self.assertTrue(self.sampleOrders[0] in self.market.bids.book)
        self.assertTrue(self.sampleOrders[2] in self.market.asks.book)

    def test_FullOrder(self):
        self.market.addOrder(
            Order(self.fakeAgents[3], "apple",  100, 1, orderType="ask"))
        self.market.addOrder(
            Order(self.fakeAgents[4], "apple",  100, 1, orderType="ask"))
        self.market.addOrder(
            Order(self.fakeAgents[3], "apple",  100, 2, orderType="bid"))
        self.assertTrue(self.market.asks.book.is_empty())
        self.assertTrue(self.market.bids.book.is_empty())

    def test_PartialOrder(self):
        self.market.addOrder(
            Order(self.fakeAgents[3], "apple",  100, 10, orderType="ask"))
        self.market.addOrder(
            Order(self.fakeAgents[3], "apple",  100, 15, orderType="bid"))
        self.assertTrue(self.market.bids.book.__len__() == 1)
        self.assertTrue(self.market.bids.getBest().quantity == 5)
        self.assertTrue(self.market.bids.getBest().price == 100)
        self.assertTrue(self.market.asks.book.is_empty())

    def test_removeAllAgentOrders(self):
        self.market.addOrder(
            Order(self.fakeAgents[4], "apple", 101, 100, orderType="ask"))
        self.market.addOrder(
            Order(self.fakeAgents[3], "apple", 100, 15, orderType="bid"))
        self.assertTrue(self.market.asks.size() == 1)
        self.assertTrue(self.market.bids.size() == 1)
        self.market.removeAllAgentOrders(self.fakeAgents[4])
        self.assertTrue(self.market.asks.size() == 0)
        self.assertTrue(self.market.bids.size() == 1)
        self.market.removeAllAgentOrders(self.fakeAgents[3])
        self.assertTrue(self.market.asks.size() == 0)
        self.assertTrue(self.market.bids.size() == 0)

    def test_FullSplitOrder(self):
        self.market.addOrder(
            Order(self.fakeAgents[3], "apple", 100, 10, orderType="ask"))
        self.market.addOrder(
            Order(self.fakeAgents[4], "apple", 100, 10, orderType="ask"))
        self.market.addOrder(
            Order(self.fakeAgents[3], "apple", 100, 15, orderType="bid"))
        self.assertTrue(self.market.asks.book.__len__() == 1)
        self.assertTrue(self.market.asks.getBest().quantity == 5)
        self.assertTrue(self.market.asks.getBest().price == 100)
        self.assertTrue(self.market.bids.book.is_empty())

if __name__ == '__main__':
    unittest.main()
