from agent import *

a=Agent(GoodsUtility.HUNGRY_UTIL)
b = Agent (GoodsUtility.THIRSTY_UTIL)

#Add some items
a.possessions.add_item("pear")
a.possessions.add_item("apple")
a.possessions.add_item("apple")
b.possessions.add_item("apple")

assert(b.possessions.collection == {"apple":1})
assert(a.possessions.collection == {"apple":2, "pear":1})
assert(a.possessions.count() == 3)
assert(a.possessions.getValue("apple")==2)

#do a trade
a_package = Collection({"pear":1})
b_package = Collection({"apple":1})
a.tradeWith(b,a_package, b_package)

assert(a.possessions.getValue("apple")==3, "Simple trade was wrong")
assert(b.possessions.getValue("apple")==0, "Simple trade was wrong")
assert(a.possessions.getValue("pear")==0, "Simple trade was wrong")
assert(b.possessions.getValue("pear")==1, "Simple trade was wrong")

#try a trade that should fail because of insufficient inventory
a.tradeWith(b,a_package, b_package)

assert(a.possessions.getValue("apple")==3, "Trade w/ insufficient inventory was wrong")
assert(b.possessions.getValue("apple")==0, "Trade w/ insufficient inventory was wrong")
assert(a.possessions.getValue("pear")==0, "Trade w/ insufficient inventory was wrong")
assert(b.possessions.getValue("pear")==1, "Trade w/ insufficient inventory was wrong")

#try a trade that should fail because of negative profit
a_package = Collection({"pear":1})
b_package = Collection({"apple":1})

a.tradeWith(b,a_package, b_package)

assert(a.possessions.getValue("apple")==3, "Trade w/ negative profit illegally occured")
assert(b.possessions.getValue("apple")==0, "Trade w/ negative profit illegally occured")
assert(a.possessions.getValue("pear")==0, "Trade w/ negative profit illegally occured")
assert(b.possessions.getValue("pear")==1, "Trade w/ negative profit illegally occured")

print "random sample"
sample = a.possessions.random_sample(1)
sample.printfull()

print "a"
a.printFull()

print "printing b"
b.printFull()

