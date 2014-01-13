from orderBook import *
import unittest

class TestOrderBook(unittest.TestCase):

    def setUp(self):
        self.book = OrderBook()
        self.sampleOrders = {}
        self.sampleOrders[0] = Order("Agent A", 100, 1, time=1)
        self.sampleOrders[1] = Order("Agent B", 150, 3, time=4)
        self.sampleOrders[2]= Order("Agent C", 300, 6, time=1)
        self.sampleOrders[3]= Order("Agent D", 150, 5, time=1)

    def test_insert(self):
        self.book.addOrders(list(self.sampleOrders.values()))
        for sampleOrder in self.sampleOrders.values():
            # check that all added orders a present
            self.assertTrue(sampleOrder in self.book.book)
        # self.book.printBook()

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

    def test_canMeet(self):
        self.book.addOrders(list(self.sampleOrders.values()))
        """ Good Trade """
        newOrder = Order("Agent A", 100, 3, orderType="ask")
        self.assertTrue(self.book.canMeet(newOrder))
        newOrder = Order("Agent A", 300, 6, orderType="ask")
        self.assertTrue(self.book.canMeet(newOrder))
        """ Enough inventory but not at that price """
        newOrder = Order("Agent A", 300, 7, orderType="ask")
        self.assertFalse(self.book.canMeet(newOrder))
        """ No bids at that price """
        newOrder = Order("Agent A", 1000, 3, orderType="ask")
        self.assertFalse(self.book.canMeet(newOrder))
        """ Not enough inventory to meet order """
        newOrder = Order("Agent A", 1, 3000, orderType="ask")
        self.assertFalse(self.book.canMeet(newOrder))


    def test_insertType(self):
        self.book.orderType="ask"
        self.assertRaises(AssertionError, self.book.addOrder, self.sampleOrders[0])

if __name__ == '__main__':
    unittest.main()
