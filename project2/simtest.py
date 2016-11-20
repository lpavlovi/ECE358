import random
import math
from Node import Node
from Medium import Medium
from NodeStates import NodeState
import loggingModule

PROP_SPEED = 2e8
NODE_DIST = 20
TICK_LENGTH = 0.00000001
SIM_DURATION = 100000000

sim_L = 1500
sim_W = 1000000
sim_A = 10

class NetWork():
    def __init__(self, N, L, W, A, tick_length, sim_duration):

        # Number of ticks it takes to advance a single bit time
        self.bit_ticks = int(( 1.00 / float(W) ) / tick_length)

        self.sim_duration = sim_duration
        self.medium = Medium(N, PROP_SPEED, NODE_DIST, tick_length)
        self.nodes  = [Node(L,W,A,x,tick_length,self.medium) for x in xrange(N)]
        self.N = N

        print self.nodes

    def simulate(self):
        for tick in xrange(self.sim_duration):
            for n in self.nodes:
                n.run(tick)

    def logStatistics(self):
        total_delay = 0
        total_successful_transfers = 0
        total_packets_dropped = 0
        for i in xrange(self.N):
            # Get node statistics
            delay_sum, successful_transfers, packets_dropped = self.nodes[i].getStatistics()
            average_delay = float(delay_sum) / float(successful_transfers) if successful_transfers!= 0 else 0

            # Log node statistics
            loggingModule.logNodeStats(i, average_delay, successful_transfers, packets_dropped)

            # Track totals
            total_delay += delay_sum
            total_successful_transfers += successful_transfers
            total_packets_dropped += packets_dropped

        total_average_delay = float(total_delay) / float(total_successful_transfers) if total_successful_transfers!= 0 else 0
        loggingModule.logSimulationStats(total_average_delay, total_successful_transfers, total_packets_dropped)

nw = NetWork(20, sim_L, sim_W, sim_A, TICK_LENGTH, SIM_DURATION)
nw.simulate()
nw.logStatistics()
