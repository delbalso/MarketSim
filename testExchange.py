from exchange import *
import unittest

class TestExchange(unittest.TestCase):

    def setUp(self):
        self.exchange = Exchange()
        self.sampleOrders = {}
        self.sampleOrders[0] = Order("Agent A", 100, 1, time=1)
        self.sampleOrders[1] = Order("Agent B", 150, 3, time=4)
        self.sampleOrders[2]= Order("Agent C", 300, 6, time=1)
        self.sampleOrders[3]= Order("Agent D", 150, 5, time=1)

    def test_add(self):
        self.exchange.addOrders(list(self.sampleOrders.values()))
        for sampleOrder in self.sampleOrders.values():
            # check that all added orders are present
            self.assertTrue(sampleOrder in self.exchange.bids.book)
            self.assertFalse(sampleOrder in self.exchange.asks.book)

    def test_askorder1(self):
        self.exchange.addOrders(list(self.sampleOrders.values()))
        order = Order("Agent D", 300, 6, orderType="ask")
        self.exchange.addOrder(order)
        # check that all added orders a present
        self.assertTrue(self.sampleOrders[0] in self.exchange.bids.book)
        self.assertTrue(self.sampleOrders[1] in self.exchange.bids.book)
        self.assertFalse(self.sampleOrders[2] in self.exchange.bids.book)
        self.assertTrue(self.sampleOrders[3] in self.exchange.bids.book)
        # self.book.printBook()
"""
    def test_bidOrder(self):
        self.book.addOrders(list(self.sampleOrders.values()))
        orders = list(self.book.book.keys())
        self.assertTrue(orders[0] is self.sampleOrders[0])
        self.assertTrue(orders[1] is self.sampleOrders[1])
        self.assertTrue(orders[2] is self.sampleOrders[3])
        self.assertTrue(orders[3] is self.sampleOrders[2])


    def test_askOrder(self):
        self.book.orderType="ask"
        for index in self.sampleOrders.keys():
            self.sampleOrders[index].orderType = "ask"
        self.book.addOrders(list(self.sampleOrders.values()))
        orders = list(self.book.book.keys())
        self.assertTrue(orders[0] is self.sampleOrders[0])
        self.assertTrue(orders[1] is self.sampleOrders[3])
        self.assertTrue(orders[2] is self.sampleOrders[1])
        self.assertTrue(orders[3] is self.sampleOrders[2])


    def test_insertType(self):
        self.book.orderType="ask"
        self.assertRaises(AssertionError, self.book.addOrder, self.sampleOrders[0])
"""

if __name__ == '__main__':
    unittest.main()
