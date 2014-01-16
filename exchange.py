from orderBook import Order, OrderBook

class Exchange:
    def __init__(self):
        self.bids = OrderBook(orderType="bid")
        self.asks = OrderBook(orderType="ask")

    def addOrders(self, orders):
        for order in orders:
            self.addOrder(order)

    """ Given an orderType/bookType string, return this exchange's corresponding book.
    Return the opposing book if reverse set to True """
    def getBook(self, bookType, reverse=False):
        assert bookType in ["ask","bid"], "Tried to add incorrect type of order to book"
        if ((bookType == "ask") != reverse):
            return self.asks
        else:
            return self.bids

    """ Place an order on the exchange. If the order can be met, perform whatever trades needed to
        meet the order """
    def addOrder(self, order):
        """
        4 cases
         1) order is not met at all, just add it
         2) order is partiall met, some of the is fulfilled
         3) order is fully met, partially fultills order on the other side
         4) order is fully met on both sides (maybe including multiple orders)
         """
        destinationBook = self.getBook(order.orderType) # The book to which this order is intended to be added
        matchingBook = self.getBook(order.orderType, reverse=True) # The book that would hold orders that would match order
        canMeetOrder, matchingOrders = matchingBook.canMeet(order)

        if canMeetOrder in ["full", "full-split", "partial"]:
            for matchingOrder in matchingOrders:
                if order.quantity > matchingOrder.quantity:
                    # Split off a child order to match the size of the first matching order
                    order1 = Order.fromOrder(order, quantity=matchingOrder.quantity)
                    order2 = matchingOrder
                    order.quantity -= matchingOrder.quantity
                    order2InBook = True
                elif order.quantity == matchingOrder.quantity:
                    order1 = order
                    order2 = matchingOrder
                    order2InBook = True
                elif order.quantity < matchingOrder.quantity:
                    order1 = order
                    order2 = Order.fromOrder(matchingOrder, quantity=order.quantity)
                    matchingOrder.quantity -= order.quantity
                    order2InBook = False

                self.trade(order1, order2, order2InBook=order2InBook)
        if order.quantity > 0:
            destinationBook.addOrder(order)


    """ Executes a trade. Some trades can be already stored in a book, one will always be new. order1 is always the new order and order2 can be already in a book or not depending on the order2InBook param. order2.quantity should never exceed order1.quantity """
    def trade(self, order1, order2, order2InBook=True):
        if order2InBook:
            order2Book = self.getBook(order2.orderType)
            order2Book.removeOrder(order2)
        order1.quantity -= order2.quantity

    """ Print the current state of the exchange """
    def printBooks(self):
        print "*** Asks ***"
        self.asks.printBook()
        print "*** Bids ***"
        self.bids.printBook()