import logging
from loggingSetup import *
import uuid

""" World is a class that holds the complete state of the world being simulated. """


class World(object):

    def __init__(self):
        self.id = uuid.uuid4()
        self.logger = newLogger("world", self.id)
        self.logger.info("World created")
        self.countries = []
        self.time = 0

    def getWorldWealthState(self, includeAgents=False):
        wealthString = ""
        wealthString = wealthString + \
            ("World Time is " + str(self.time) + "\n")
        for country in self.countries:
            wealthString = wealthString + ("Country " + str(country.id) + " has wealth " + str(
                country.getTotalWealth()) + " and population " + str(len(country.population)) + "\n")
            for agent in country.population:
                wealthString = wealthString + \
                    ("   Agent " + str(agent.id) +
                     " has wealth " + str(agent.getWealth()) + "\n")

        return wealthString
