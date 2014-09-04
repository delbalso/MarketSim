import logging
LOG_FILENAME = '/tmp/world_timeline.out'
logger = logging.getLogger("world")
f = logging.FileHandler('/tmp/world_timeline.out',mode="w",)
logger.addHandler(f)

""" World is a class that holds the complete state of the world being simulated. """
class World(object):

    def __init__(self):
        self.countries = []
        self.time = 0
        logger.info("Initializing")

    def logWorldWealth(self, includeAgents=False):
        wealthString = ""
        wealthString = wealthString + ("World Time is " + str(self.time) +"\n")
        for country in self.countries:
            wealthString = wealthString + ("Country " + str(country.id) + " has wealth " + str(country.getTotalWealth()) + " and population " + str(len(country.population)) + "\n")
            for agent in country.population:
                wealthString = wealthString + ("   Agent " + str(agent.id) + " has wealth " + str(agent.getWealth()) + "\n")

        logger.info(wealthString)

