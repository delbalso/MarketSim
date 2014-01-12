from agent import *

""" Generate n random market agents """
def createAndPopulateRandomAgents(numAgents):
    agents=list()
    for i in xrange(numAgents):
        agents.append(Agent())
        agents[i].assignRandomStats()

    return agents
