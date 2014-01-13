import uuid
import time
import functools
from bintrees import RBTree
# https://pypi.python.org/pypi/bintrees

@functools.total_ordering
class Order:
    def __init__(self, agent, price, quantity, orderType="bid"):
        assert price>=0, "Order can't have a negative price"
        self.agent = agent
        self.price = price
        self.quantity = quantity
        self.orderTime = time.time()
        self.orderType = orderType
        self.ID = uuid.uuid4()

    def __eq__(self, other):
        if (self.orderTime == other.orderTime and
                self.price == other.price):
            return True
        return False

    def __le__(self, other):
        if self.price < other.price:
            return True
        if self.price == other.price:
            if (self.orderType =="bid" and self.orderTime > other.orderTime):
                return True
            if (self.orderType =="ask" and self.orderTime < other.orderTime):
                return True
        return False

    def printOrder(self):
        print "agent: " + str(self.agent)
        print "price: "+ str(self.price)
        print "quantity: "+ str(self.quantity)
        print "orderType: "+ str(self.orderType)
        print "orderTime: "+ str(self.orderTime)

class OrderBook:
    def __init__(self,orderType="bid"):
        self.book = RBTree()
        self.orderType = "bid"

    def addOrder(self, order):
        assert order.orderType==self.orderType, "Tried to add incorrect type of order to book"
        self.book[order] = True

    def addOrders(self, orders):
        for order in orders:
            self.addOrder(order)

    def printBook(self):
        for item in self.book.keys():
            item.printOrder()
            print "-------"

    """ Can this order book provide the other side of order's trade, return orders that will meet it
        return tuple (quantity, list of orders) """
    def canMeet(self, order):
        pass

class Exchange:
    def __init__(self):
        self.bids = OrderBook(orderType="bid")
        self.asks = OrderBook(orderType="ask")

    def addOrder(self, order):
        """
        4 cases
         1) order is not met, just add it
         2) order is partiall met, some of the is fulfilled
         3) order is fully met, partially fultills order on the other side
         4) order is fully met on both sides (maybe including multiple orders)
         """
        pass



