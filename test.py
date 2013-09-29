from agent import *

a=Agent(Utility.HUNGRY_UTIL)
b = Agent (Utility.THIRSTY_UTIL)

#Add some items
a.possessions.add_item("pear")
a.possessions.add_item("apple")
a.possessions.add_item("apple")
b.possessions.add_item("apple")

assert b.possessions.collection == {"apple":1}, "Items not added to Agent properly"
assert a.possessions.collection == {"apple":2, "pear":1}, "Items not added to Agent properly"
assert a.possessions.count() == 3, "Items not added to Agent properly"
assert a.possessions.getValue("apple")==2, "Items not added to Agent properly"

#do a trade
a_package = Collection({"pear":1})
b_package = Collection({"apple":1})
a.tradeWith(b,a_package, b_package)

assert a.possessions.getValue("apple")==3, "Simple trade was wrong"
assert b.possessions.getValue("apple")==0, "Simple trade was wrong"
assert a.possessions.getValue("pear")==0, "Simple trade was wrong"
assert b.possessions.getValue("pear")==1, "Simple trade was wrong"

#try a trade that should fail because of insufficient inventory
a.tradeWith(b,a_package, b_package)
assert a.possessions.getValue("apple")==3, "Trade w/ insufficient inventory was wrong"
assert b.possessions.getValue("apple")==0, "Trade w/ insufficient inventory was wrong"
assert a.possessions.getValue("pear")==0, "Trade w/ insufficient inventory was wrong"
assert b.possessions.getValue("pear")==1, "Trade w/ insufficient inventory was wrong"

#try a trade that should fail because of negative profit
a_package = Collection({"pear":1})
b_package = Collection({"apple":1})

a.tradeWith(b,a_package, b_package)

assert a.possessions.getValue("apple")==3, "Trade w/ negative profit illegally occured"
assert b.possessions.getValue("apple")==0, "Trade w/ negative profit illegally occured"
assert a.possessions.getValue("pear")==0, "Trade w/ negative profit illegally occured"
assert b.possessions.getValue("pear")==1, "Trade w/ negative profit illegally occured"

#Assign random utility and possession
a=Agent()
b=Agent()
a.assignRandomStats(possessions=0)
b.assignRandomStats(utility=0)

for good in ALL_GOODS:
    assert a.utility.collection.has_key(good), "Good not assigned by random stats"
    assert not a.possessions.collection.has_key(good), "Good incorrectly assigned by random stats"
    assert a.utility.getValue(good) > 0 and a.utility.getValue(good) < 100, "Invalid quantity in  utility"

    assert b.possessions.collection.has_key(good), "Good not assigned by random stats"
    assert not b.utility.collection.has_key(good), "Good incorrectly  assigned by random stats"
    assert b.possessions.getValue(good) > 0 and b.possessions.getValue(good) < 100, "Invalid quantity in  utility"

print "random sample"
sample = a.possessions.random_sample(1)
sample.printfull()

print "a"
a.printAgent()

print "printing b"
b.printAgent()

