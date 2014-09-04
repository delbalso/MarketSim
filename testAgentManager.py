from agentManager import *
from location import *
from world import *
import unittest


class TestAgentManager(unittest.TestCase):

    def setUp(self):
        USA = Location()
        USA.exchange = Exchange()
        China = Location()
        China.exchange = Exchange()
        self.world = World()
        self.world.countries.append(USA)
        self.world.countries.append(China)

    def test_createRightNumberOfAgents(self):
        agents = createAndPopulateRandomAgents(5, self.world)
        self.assertTrue(len(agents) == 5)

    def test_assignRandomStats(self):
        desiredWealth = 10
        agents = createAndPopulateRandomAgents(
            5, self.world, wealth=desiredWealth)
        for agent in agents:
            self.assertTrue(abs(agent.getWealth() - desiredWealth) < 1)
            self.assertTrue(agent.getLocation() in self.world.countries)
        self.assertTrue(abs(Agent.getTotalWealth(agents) - 50) < 1)
