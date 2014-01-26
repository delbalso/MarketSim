from exchange import *
import unittest

class FakeAgent:
    def tradeCompleted(self, order1, order2, good):
        pass


class TestExchange(unittest.TestCase):

    def setUp(self):
        self.exchange = Exchange("apple")
        self.sampleOrders = {}
        self.fakeAgents = {}

        self.fakeAgents[0] = FakeAgent()
        self.fakeAgents[1] = FakeAgent()
        self.fakeAgents[2] = FakeAgent()
        self.fakeAgents[3] = FakeAgent()
        self.fakeAgents[4] = FakeAgent()
        self.sampleOrders[0] = Order(self.fakeAgents[0], "apple", 100, 1, time=1)
        self.sampleOrders[1] = Order(self.fakeAgents[1], "apple", 150, 3, time=4)
        self.sampleOrders[2] = Order(self.fakeAgents[2], "apple", 300, 6, time=1)
        self.sampleOrders[3] = Order(self.fakeAgents[3], "apple", 150, 5, time=1)

    def test_add(self):
        self.exchange.addOrders(list(self.sampleOrders.values()))
        for sampleOrder in self.sampleOrders.values():
            # check that all added orders are present
            self.assertTrue(sampleOrder in self.exchange.bids.book)
            self.assertFalse(sampleOrder in self.exchange.asks.book)

    def test_simpleAddBidOffer(self):
        for index in self.sampleOrders.keys():
            self.sampleOrders[index].orderType = "ask"
        self.exchange.addOrders(list(self.sampleOrders.values()))
        order = Order(self.fakeAgents[3], "apple",  100, 1, orderType="bid")
        self.exchange.addOrder(order)
        self.assertFalse(self.sampleOrders[0] in self.exchange.asks.book)
        self.assertTrue(self.sampleOrders[1] in self.exchange.asks.book)
        self.assertTrue(self.sampleOrders[2] in self.exchange.asks.book)
        self.assertTrue(self.sampleOrders[3] in self.exchange.asks.book)
        self.assertTrue(self.exchange.bids.book.is_empty())

    def test_simpleAddAskOffer(self):
        self.exchange.addOrders(list(self.sampleOrders.values()))
        order = Order(self.fakeAgents[3], "apple", 300, 6, orderType="ask")
        self.exchange.addOrder(order)
        self.assertTrue(self.sampleOrders[0] in self.exchange.bids.book)
        self.assertTrue(self.sampleOrders[1] in self.exchange.bids.book)
        self.assertFalse(self.sampleOrders[2] in self.exchange.bids.book)
        self.assertTrue(self.sampleOrders[3] in self.exchange.bids.book)
        self.assertTrue(self.exchange.asks.book.is_empty())
        # self.book.printBook()

    def test_NoFill(self):
        self.sampleOrders[2].orderType = "ask"
        self.exchange.addOrders(list(self.sampleOrders.values()))
        #self.exchange.printBooks()
        self.assertTrue(self.sampleOrders[1] in self.exchange.bids.book)
        self.assertTrue(self.sampleOrders[3] in self.exchange.bids.book)
        self.assertTrue(self.sampleOrders[0] in self.exchange.bids.book)
        self.assertTrue(self.sampleOrders[2] in self.exchange.asks.book)

    def test_FullOrder(self):
        self.exchange.addOrder(Order(self.fakeAgents[3], "apple",  100, 1, orderType="ask"))
        self.exchange.addOrder(Order(self.fakeAgents[4],"apple",  100, 1, orderType="ask"))
        self.exchange.addOrder(Order(self.fakeAgents[3],"apple",  100, 2, orderType="bid"))
        self.assertTrue(self.exchange.asks.book.is_empty())
        self.assertTrue(self.exchange.bids.book.is_empty())

    def test_PartialOrder(self):
        self.exchange.addOrder(Order(self.fakeAgents[3],"apple",  100, 10, orderType="ask"))
        self.exchange.addOrder(Order(self.fakeAgents[3],"apple",  100, 15, orderType="bid"))
        self.assertTrue(self.exchange.bids.book.__len__()==1)
        self.assertTrue(self.exchange.bids.getBest().quantity == 5)
        self.assertTrue(self.exchange.bids.getBest().price == 100)
        self.assertTrue(self.exchange.asks.book.is_empty())

    def test_FullSplitOrder(self):
        self.exchange.addOrder(Order(self.fakeAgents[3], "apple", 100, 10, orderType="ask"))
        self.exchange.addOrder(Order(self.fakeAgents[4], "apple", 100, 10, orderType="ask"))
        self.exchange.addOrder(Order(self.fakeAgents[3], "apple", 100, 15, orderType="bid"))
        self.assertTrue(self.exchange.asks.book.__len__()==1)
        self.assertTrue(self.exchange.asks.getBest().quantity == 5)
        self.assertTrue(self.exchange.asks.getBest().price == 100)
        self.assertTrue(self.exchange.bids.book.is_empty())

if __name__ == '__main__':
    unittest.main()
