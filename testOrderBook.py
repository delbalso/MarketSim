from orderBook import *
import unittest

class TestOrderBook(unittest.TestCase):

    def setUp(self):
        self.book = OrderBook()
#TODO turn this into a list of orders
        self.sampleOrders = {}
        self.sampleOrders[0] = Order("Agent A", 100, 1)
        self.sampleOrders[1] = Order("Agent B", 124, 3)
        self.sampleOrders[2]= Order("Agent C", 342, 6)
        self.sampleOrders[3]= Order("Agent D", 124, 5)
        self.sampleOrders[0].orderTime = 1
        self.sampleOrders[1].orderTime = 4
        self.sampleOrders[2].orderTime = 1
        self.sampleOrders[3].orderTime = 1

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

    def test_insertType(self):
        self.book.orderType="ask"
        self.assertRaises(AssertionError, self.book.addOrder, self.sampleOrders[0])

if __name__ == '__main__':
    unittest.main()
