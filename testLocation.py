from location import *
from exchange import Exchange
from agent import Agent
import unittest


class TestLocation(unittest.TestCase):

    def setUp(self):
        exchange1 = Exchange()
        exchange2 = Exchange()
        self.location1 = Location(exchange1)
        self.location2 = Location(exchange2)
        self.agent1 = Agent(location=self.location1)
        self.agent2 = Agent(location=self.location2)

    def test_setUp(self):
        self.assertTrue(self.agent1.exchange == self.location1.exchange)
        self.assertTrue(self.agent2.exchange == self.location2.exchange)
        self.assertTrue(self.agent1 in self.location1.population)
        self.assertTrue(self.agent2 in self.location2.population)
        self.assertTrue(self.agent1.getLocation() == self.location1)
        self.assertTrue(self.agent2.getLocation() == self.location2)
