from itertools import *
from agent import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-v', default=0, type=int)
args = parser.parse_args()
__VERBOSE__=args.v

def tradeRound(agents):
    trading_order = list(combinations(range(len(agents)),2))
    for agent_index, partner_index in trading_order:
        agent = agents[agent_index]
        partner = agents[partner_index]

        old_wealth = agent.getWealth() + partner.getWealth()

        trade_successful = agent.tradeWith(partner)
        if (__VERBOSE__>1 and trade_successful):
            print "Trade successful between agents, ", agent_index, " and ", partner_index, ". Wealth +", (agent.getWealth() + partner.getWealth() - old_wealth)

def runSetOfTradeRounds(agents, numRounds=1):
    for i in xrange(numRounds):
        tradeRound(agents)
        if (__VERBOSE__>1):
            print "round ", i, " of trading complete. New wealth is: ", sum(agent.getWealth() for agent in agents)

def vprint (verbosity, message):
    if (__VERBOSE__>=verbosity):
        print message

def __main__():
    #make a few agents
    agents=list()
    for i in xrange(15):
        agents.append(Agent())
        agents[i].assignRandomStats()

    #print current stats
    print list(agent.getWealth() for agent in agents)
    print "Total wealth: ", Agent.getTotalWealth(agents)

    #trade a bit
    beginning_wealth = Agent.getTotalWealth(agents)
    runSetOfTradeRounds(agents, numRounds = 100)
    end_wealth = Agent.getTotalWealth(agents)
    print "Total wealth: ", end_wealth
    print "up ", 100*(float(end_wealth)/beginning_wealth-1), "%"




__main__()

