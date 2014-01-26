import uuid
import copy
import time
import functools
from bintrees import RBTree
# https://pypi.python.org/pypi/bintrees

@functools.total_ordering
class Order:
    @classmethod
    def fromOrder(self,order, quantity=None):
        newOrder = copy.copy(order)
        if quantity!=None:
            newOrder.quantity = quantity
        return newOrder

    def __init__(self, agent, good, price, quantity, orderType="bid", time=time.time()):
        assert price>=0, "Order can't have a negative price"
        self.agent = agent
        self.price = price
        self.good = good
        self.quantity = quantity
        self.orderTime = time
        self.orderType = orderType
        self.ID = uuid.uuid4()

    def __eq__(self, other):
        if (self.orderTime == other.orderTime and
                self.price == other.price and
                self.ID == other.ID):
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
    def __init__(self, good, orderType="bid"):
        self.book = RBTree()
        self.orderType = orderType
        self.good = good

    def getBest(self):
        if len(self.book)==0:
            return None
        if self.orderType=="bid":
            return self.book.max_key()
        else:
            return self.book.min_key()

    def removeOrder(self, order):
        return self.book.discard(order)

    def getNext(self, order):
        if self.orderType=="bid":
            return self.book.prev_key(order)
        else:
            return self.book.succ_key(order)

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
        assert orderToMatch.orderType!=self.orderType, "Tried to meet incorrect order type "+orderToMatch.orderType
        quantity=0
        orders=[]
        canMeet = None # represents whether this orderbook can meet the order
        for order in self.book.keys(reverse=(self.orderType=="bid")):
            if quantity >= orderToMatch.quantity:
                break
            if ((order.price < orderToMatch.price and self.orderType=="bid") or
                    (order.price > orderToMatch.price and self.orderType=="ask")):
                break
            quantity += order.quantity
            if quantity > orderToMatch.quantity:
                quantityToKeep = quantity - orderToMatch.quantity
            else:
                quantityToKeep = order.quantity
            orders.append(order)
        if (quantity == orderToMatch.quantity):
            canMeet = "full" # Orders fit perfectly into this orderToMatch's quantity
        elif (quantity >= orderToMatch.quantity):
            canMeet = "full-split" # Order fit orderToMatch, but last order needs to be split
        elif quantity >0:
            canMeet = "partial" # Only part of OrderToMatch could be filled
        else:
            canMeet = "nofill" # No order matched orderToMatch
        return canMeet, orders

