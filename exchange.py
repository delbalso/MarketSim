from orderBook import Order, OrderBook
from loggingSetup import *


class Exchange:

    def __init__(self, good):
        self.good = good
        self.bids = OrderBook(good, orderType="bid")
        self.asks = OrderBook(good, orderType="ask")

    """ Given an orderType/bookType string, return this exchange's corresponding book.
    Return the opposing book if reverse set to True """

    def getBook(self, bookType, reverse=False):
        assert bookType in [
            "ask", "bid"], "Tried to add incorrect type of order to book"
        if ((bookType == "ask") != reverse):
            return self.asks
        else:
            return self.bids

    def addOrders(self, orders):
        for order in orders:
            self.addOrder(order)
    """ Place an order on the exchange. If the order can be met, perform whatever trades needed to
        meet the order """

    def addOrder(self, order):
        logging.debug("addOrder. id: " + str(order.agent.id) + ", good: " + order.good + ", orderType: " +
                      order.orderType + ", price: " + str(order.price) + ", quantity: " + str(order.quantity))
        assert order.good == self.good, "Tried to add the incorrect type of good"
        # We don't want an exchange for money
        assert order.good != "money", "Tried to add an order for money"
        # The book to which this order is intended to be added
        destinationBook = self.getBook(order.orderType)
        destinationBook.addOrder(order)

        tradeOccurred = self.settle()
        unsettled = tradeOccurred
        while unsettled == True:
            unsettled = self.settle()

        return tradeOccurred

    """ settle executes any possible trades given the exchange's orderbooks. It recursively calls itself until all possible trades are made """

    def settle(self):
        bestAsk = self.asks.getBest()
        bestBid = self.bids.getBest()

        if bestAsk == None or bestBid == None:
            return False

        quantity = 0  # How much is being traded
        if bestAsk.price <= bestBid.price:  # Should a trade occur?
            if bestAsk.quantity < bestBid.quantity:
                # also covers the case of bid and ask having equal quantities
                quantity = bestAsk.quantity
            else:
                quantity = bestBid.quantity

            # This uses the halfway point between the bid and the ask as the
            # price, this may not be exactly what is needed. We may want to use
            # the best price for the new incoming order. (i.e. if incoming
            # order is a bid, use best ask price, and vice versa)
            price = (bestAsk.price + bestBid.price) / 2

            # TODO: Add tests to ensure that the agent is solvent
            assert (
                quantity <= bestAsk.quantity and quantity <= bestBid.quantity)
            # This is a partial execution of this order
            if quantity < bestAsk.quantity:
                bestAsk.quantity = bestAsk.quantity - quantity
            else:  # The quantity is the exact size of the order
                self.asks.removeOrder(bestAsk)
            # This is a partial execution of this order
            if quantity < bestBid.quantity:
                bestBid.quantity = bestBid.quantity - quantity
            else:  # The quantity is the exact size of the order
                self.bids.removeOrder(bestBid)

            logging.debug("Trade: " + str(bestAsk.agent.id) + " --> " + str(bestBid.agent.id) + ", for good: " + self.good +
                          ", price: " + str(price) + ", quantity: " + str(quantity) + ", money exchanged = " + str(price * quantity))

            # Adjust the participating agent's inventories
            bestAsk.agent.removeInv(self.good, quantity)
            bestBid.agent.removeInv("money", quantity * price)
            bestAsk.agent.addInv("money", quantity * price)
            bestBid.agent.addInv(self.good, quantity)
            return True
        else:
            return False

    """ Print the current state of the exchange """

    def printBooks(self):
        print "*** Asks ***"
        self.asks.printBook()
        print "*** Bids ***"
        self.bids.printBook()

ALL_GOODS = ["apple", "banana", "orange", "water", "land", "clothes", "money"]


class Exchanges:

    def __init__(self):
        self.exchanges = {}
        for good in ALL_GOODS:
            self.exchanges[good] = Exchange(good)

    def getExchange(self, good):
        assert self.exchanges.has_key(
            good), "Tried to retreive exchange \"" + good + "\" that doesn't exist"
        return self.exchanges[good]
