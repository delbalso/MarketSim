from agentManager import *
import unittest

class TestAgentManager(unittest.TestCase):
    def setUp(self):
        pass

    def test_createRightNumberOfAgents(self):
        agents = createAndPopulateRandomAgents(5)
        self.assertTrue(len(agents) == 5)

    def test_assignRandomStats(self):
        desiredWealth = 10
        agents = createAndPopulateRandomAgents(5, wealth = desiredWealth)
        for agent in agents:
            self.assertTrue (abs(agent.getWealth() - desiredWealth) < 1)
        self.assertTrue (abs(Agent.getTotalWealth(agents) - 50) < 1)
