from orderBook import *
import unittest


class TestOrderBook(unittest.TestCase):

    def setUp(self):
        self.book = OrderBook("apple")
        self.sampleOrders = {}
        self.sampleOrders[0] = Order("Agent A", "apple", 100, 1, time=1)
        self.sampleOrders[1] = Order("Agent B", "apple", 150, 3, time=4)
        self.sampleOrders[2] = Order("Agent C", "apple", 300, 6, time=1)
        self.sampleOrders[3] = Order("Agent D", "apple", 150, 5, time=1)

    def test_addOrders(self):
        self.book.addOrders(list(self.sampleOrders.values()))
        for sampleOrder in self.sampleOrders.values():
            # check that all added orders a present
            self.assertTrue(sampleOrder in self.book.book)
        # self.book.printBook()

    def test_complexAddOffer(self):
        self.book.addOrder(Order("Agent D", "apple", 100, 1))
        self.book.addOrder(Order("Agent E", "apple", 100, 1))
        self.assertTrue(len(self.book.book) == 2)

    def test_getBestAndOrderSequenceForBids(self):
        self.book.addOrders(list(self.sampleOrders.values()))
        self.assertTrue(self.book.getBest() == self.sampleOrders[2])
        self.assertTrue(
            self.book.getNext(self.sampleOrders[2]) == self.sampleOrders[3])
        self.assertTrue(
            self.book.getNext(self.sampleOrders[3]) == self.sampleOrders[1])
        self.assertTrue(
            self.book.getNext(self.sampleOrders[1]) == self.sampleOrders[0])

    def test_removeAllAgentOrders(self):
        self.book.addOrder(Order("Agent D", "apple", 100, 1))
        self.assertTrue(self.book.size() == 1)
        self.book.removeAllAgentOrders("Agent D")
        self.assertTrue(self.book.size() == 0)

    def test_getBestAndOrderSequenceForAsks(self):
        self.book.orderType = "ask"
        for index in self.sampleOrders.keys():
            self.sampleOrders[index].orderType = "ask"
        self.book.addOrders(list(self.sampleOrders.values()))
        self.assertTrue(self.book.getBest() == self.sampleOrders[0])
        self.assertTrue(
            self.book.getNext(self.sampleOrders[0]) == self.sampleOrders[3])
        self.assertTrue(
            self.book.getNext(self.sampleOrders[3]) == self.sampleOrders[1])
        self.assertTrue(
            self.book.getNext(self.sampleOrders[1]) == self.sampleOrders[2])

    def test_canMeet(self):
        self.book.addOrders(list(self.sampleOrders.values()))

        """ Good Trade """
        newOrder = Order("Agent A", "apple", 100, 3, orderType="ask")
        self.assertTrue(self.book.canMeet(newOrder)[0] == "full-split")
        newOrder = Order("Agent A", "apple", 300, 6, orderType="ask")
        self.assertTrue(self.book.canMeet(newOrder)[0] == "full")

        """ Enough inventory but not at that price """
        newOrder = Order("Agent A", "apple", 300, 7, orderType="ask")
        self.assertTrue(self.book.canMeet(newOrder)[0] == "partial")

        """ No bids at that price """
        newOrder = Order("Agent A", "apple", 1000, 3, orderType="ask")
        self.assertTrue(self.book.canMeet(newOrder)[0] == "nofill")

        """ Not enough inventory to meet order """
        newOrder = Order("Agent A", "apple", 1, 3000, orderType="ask")
        self.assertTrue(self.book.canMeet(newOrder)[0] == "partial")

    def test_insertType(self):
        self.book.orderType = "ask"
        self.assertRaises(
            AssertionError, self.book.addOrder, self.sampleOrders[0])

if __name__ == '__main__':
    unittest.main()
