from itertools import *
from agent import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-v', default=0, type=int)
args = parser.parse_args()
__VERBOSE__=args.v

""" Have each possible pair of the given agents attempts to trade in a fixed order """
def tradeRound(agents):
    trading_order = list(combinations(range(len(agents)),2))
    for agent_index, partner_index in trading_order:
        agent = agents[agent_index]
        partner = agents[partner_index]

        old_wealth = agent.getWealth() + partner.getWealth()

        trade_successful = agent.seriesTrade(partner)
        if (__VERBOSE__>1 and trade_successful):
            print "Trade successful between agents, ", agent_index, " and ", partner_index, ". Wealth +", (agent.getWealth() + partner.getWealth() - old_wealth)

""" Run numRounds rounds of trades. If tradeUntilComplete is true, then keep running trade rounds until total wealth convergence (i.e. incremental wealth increase <1) """
def runSetOfTradeRounds(agents, numRounds=1, tradeUntilComplete=False):
    complete = False
    roundsTraded = 0

    while ((roundsTraded<numRounds and tradeUntilComplete==False) or
        (complete == False and tradeUntilComplete==True)):
        if tradeUntilComplete:
            oldTotalWealth = sum(agent.getWealth() for agent in agents)
        tradeRound(agents)
        if (__VERBOSE__>1):
            print "Round ", roundsTraded, " of trading complete. New wealth is: ", sum(agent.getWealth() for agent in agents)
        if tradeUntilComplete:
            newTotalWealth = sum(agent.getWealth() for agent in agents)
            complete = (newTotalWealth - oldTotalWealth < 1)
        roundsTraded += 1

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
    runSetOfTradeRounds(agents, tradeUntilComplete=True)
    end_wealth = Agent.getTotalWealth(agents)
    print "Total wealth: ", end_wealth
    print "up ", 100*(float(end_wealth)/beginning_wealth-1), "%"




__main__()

