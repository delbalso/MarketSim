from agent import *
from loggingSetup import *
ALL_GOODS = ["apple", "banana", "orange", "water", "land", "clothes", "money"]
""" Generate n random market agents """


def createAndPopulateRandomAgents(numAgents, world, wealth=None):
    agents = list()
    for i in xrange(numAgents):
        agents.append(Agent(None))
        assignRandomStats(agents[i], world, wealth=wealth)

    return agents

""" assignRandomStats gives an agent random stats with a wealth (according to the appraisal of the utility assigned by this function) of wealth """


def assignRandomStats(agent, world, inventory=None, utility=None, wealth=None):
    agent.utility.empty()
    agent.inventory.empty()
    if (utility == None):
        agent.utility.addCollection(generateRandomSet())
        agent.utility.setValue("money", 1)
    if (inventory == None):
        agent.inventory.addCollection(generateRandomSet())
        if (wealth != None):
            assert wealth > 0, "Desired wealth not > 0"
            adjustmentFactor = float(wealth) / agent.getWealth()
            for good in agent.inventory.collection.keys():
                count = agent.getInv(good)
                if adjustmentFactor > 1:
                    agent.addInv(good, count * adjustmentFactor - count)
                else:
                    agent.removeInv(good,  - count * adjustmentFactor + count)
    logging.debug("Assigned agent " + str(agent.id) +
                  " random stats with a wealth of " + str(agent.getWealth()))
    agent.setLocation(random.choice(world.countries))

""" generateRandomSet generates a set of random goods in random quantities """


def generateRandomSet():
    randomSet = dict()
    for good in ALL_GOODS:
        randomSet[good] = int(random.random() * 100)
    return randomSet
