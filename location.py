import uuid

""" Location is a class that represents a location in the virtual world. Each location has one exchange and a population. """


class Location(object):

    def __init__(self, exchange=None, population=None):
        self.id = uuid.uuid4()
        self.exchange = exchange
        if population==None:
            population = []
        self.population = population
    """ addAgent is called when an agent transports to a new location. The Agent class should handle adding the agent to this location when in its methods """

    def addAgent(self, agent):
        assert agent not in self.population
        self.population.append(agent)

    """ removeAgent removes an agent from this location. Its invocation details are similar to addAgent """

    def removeAgent(self, agent):
        assert agent in self.population
        self.population.remove(agent)

    """ getTotalWealth is the total wealth of all memebers of the population of this Location """
    def getTotalWealth(self):
        totalWealth = 0
        for agent in self.population:
            totalWealth = totalWealth + agent.getWealth()
        return totalWealth
