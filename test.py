from market import *
from agentManage import *
from agent import *

a = Agent(Utility.HUNGRY_UTIL)
b = Agent (Utility.THIRSTY_UTIL)

### Add some items
a.possessions.add_item("orange")
a.possessions.add_item("apple")
a.possessions.add_item("apple")
b.possessions.add_item("apple")

assert b.possessions.collection == {"apple":1}, "Items not added to Agent properly"
assert a.possessions.collection == {"apple":2, "orange":1}, "Items not added to Agent properly"
assert a.possessions.count() == 3, "Items not added to Agent properly"
assert a.possessions.getValue("apple")==2, "Items not added to Agent properly"

#### Do a trade
a_package = Collection({"orange":1})
b_package = Collection({"apple":1})
a.trade(b,a_package, b_package)

assert a.possessions.getValue("apple")==3, "Simple trade was wrong"
assert b.possessions.getValue("apple")==0, "Simple trade was wrong"
assert a.possessions.getValue("orange")==0, "Simple trade was wrong"
assert b.possessions.getValue("orange")==1, "Simple trade was wrong"

### Try a trade that should fail because of insufficient inventory
a.trade(b,a_package, b_package)
assert a.possessions.getValue("apple")==3, "Trade w/ insufficient inventory was wrong"
assert b.possessions.getValue("apple")==0, "Trade w/ insufficient inventory was wrong"
assert a.possessions.getValue("orange")==0, "Trade w/ insufficient inventory was wrong"
assert b.possessions.getValue("orange")==1, "Trade w/ insufficient inventory was wrong"

### Try a trade that should fail because of negative profit
a_package = Collection({"apple":1})   # value of 10 to A
b_package = Collection({"orange":1})  # value of 9 to A

a.trade(b,a_package, b_package)

assert a.possessions.getValue("apple")==3, "Trade w/ negative profit illegally occured"
assert b.possessions.getValue("apple")==0, "Trade w/ negative profit illegally occured"
assert a.possessions.getValue("orange")==0, "Trade w/ negative profit illegally occured"
assert b.possessions.getValue("orange")==1, "Trade w/ negative profit illegally occured"

### Assign random utility and possession
a=Agent()
b=Agent()
a.assignRandomStats(possessions=0)
b.assignRandomStats(utility=0)

for good in ALL_GOODS:
    assert a.utility.collection.has_key(good), "Good not assigned by random stats"
    assert not a.possessions.collection.has_key(good), "Good incorrectly assigned by random stats"
    assert a.utility.getValue(good) > 0 and a.utility.getValue(good) < 100, "Invalid quantity in utility"
    assert b.possessions.collection.has_key(good), "Good not assigned by random stats"
    assert not b.utility.collection.has_key(good), "Good incorrectly  assigned by random stats"
    assert b.possessions.getValue(good) > 0 and b.possessions.getValue(good) < 100, "Invalid quantity in  utility"


""" Ensure right number of rounds in seriesTrade """
random.seed(1337)
agents = createAndPopulateRandomAgents(5)
roundsTraded = runSetOfTradeRounds(agents,tradeUntilComplete=True)
assert roundsTraded==32, "Incorrect number of trade rounds in seriesTrade"
assert agents[0].possessions.collection["apple"]==129, "Incorrect inventory after seriesTrades"

