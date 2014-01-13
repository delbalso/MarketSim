import uuid
import time
import functools
from bintrees import RBTree
# https://pypi.python.org/pypi/bintrees

@functools.total_ordering
class Order:
    def __init__(self, agent, price, quantity, orderType="bid", time=time.time()):
        assert price>=0, "Order can't have a negative price"
        self.agent = agent
        self.price = price
        self.quantity = quantity
        self.orderTime = time
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

    def getBest(self):
        if len(self)==0:
            return None
        if self.orderType=="bid":
            return self.book.max_key()
        else:
            return self.book.min_key()

    def getNext(self, order):
        if self.orderType=="bid":
            return self.book.prev_key(order)
        else:
            return self.book.next_key(order)

    def addOrder(self, order):
        assert order.orderType==self.orderType, "Tried to add incorrect type of order to book"
        self.book[order] = True

    def addOrders(self, orders):
        for order in orders:
            self.addOrder(order)

    def printBook(self):
        for item in self.book.keys():
            item.printOrder()
            print "-----------------------------"

    """ Can this order book provide the other side of order's trade, return orders that will meet it
        return tuple (quantity, list of orders) """
    def canMeet(self, orderToMatch):
        assert orderToMatch.orderType!=self.orderType, "Tried to meet incorrect order type"
        quantity=0
        for order in self.book.keys(reverse=(self.orderType=="bid")):
            if quantity >= orderToMatch.quantity:
                break
            if ((order.price < orderToMatch.price and self.orderType=="bid") or
                    (order.price > orderToMatch.price and self.orderType=="ask")):
                break
            quantity += order.quantity
        return (quantity >= orderToMatch.quantity)

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

    def trade(self, order):
        books = self.bids if order.orderType()=="ask" else self.asks
        #Collect matching orders
        quantity=0
        pass

