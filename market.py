from itertools import *
from world import *
from agent import *
from agentManager import *
from orderBook import *
from location import *
from loggingSetup import *

def cycle(world):
    world.logWorldWealth(includeAgents=True)
    world.time = world.time + 1

def worldSetup():
    USA = Location()
    USA.exchange = Exchange()
    China = Location()
    China.exchange = Exchange()
    world = World()
    world.countries.append(USA)
    world.countries.append(China)
    return world

def __main__():
    world = worldSetup()
    # Make a few agents
    agents=createAndPopulateRandomAgents(15, world)

    while world.time<100:
        cycle(world)

__main__()

