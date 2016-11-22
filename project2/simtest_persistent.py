import random
import math
import sys
from NodePersistent import Node as Node
from Medium import Medium
from NodeStates import NodeState
import loggingModule

PROP_SPEED = 2e8
NODE_DIST = 20
TICK_LENGTH = 0.00000001
SIM_DURATION = 100000000
FIVE_MIN = (SIM_DURATION * 60 * 5)

sim_N = int(sys.argv[1])
sim_L = 1500
sim_W = 1000000
sim_A = int(sys.argv[2])
sim_P = float(sys.argv[3])

class NetWork():
    def __init__(self, N, L, W, A, tick_length, P, sim_duration):

        # Number of ticks it takes to advance a single bit time
        self.bit_ticks = int(( 1.00 / float(W) ) / tick_length)
        self.simulation_duration_seconds = float(sim_duration) * float(tick_length)
        self.sim_duration = sim_duration
        self.medium = Medium(N, PROP_SPEED, NODE_DIST, tick_length)
        self.nodes  = [Node(L, W, A, x, tick_length, P, self.medium) for x in xrange(N)]
        self.N = N
        self.tick_length = tick_length


    def simulate(self):
        for tick in xrange(self.sim_duration):
            for n in self.nodes:
                n.run(tick)

    def simulateTickSkip(self):
        tick = 0
        closest_node_event = [0]*self.N

        while tick < self.sim_duration:
            for i in xrange(self.N):
                self.nodes[i].run(tick)
                closest_node_event[i] = self.nodes[i].getClosestEvent(tick)
            tick = min(closest_node_event)

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

        # Calculate total average delay and throughput
        total_average_delay = float(total_delay) / float(total_successful_transfers) if total_successful_transfers!= 0 else 0
        total_average_delay_seconds = float(total_average_delay) * float(self.tick_length)
        total_throughput = (total_successful_transfers * float(sim_L) * 8.00) / (float(self.sim_duration) * float(self.tick_length))

        # Log complete simulation statistics
        loggingModule.logSimulationStatsV2(
                self.simulation_duration_seconds,
                total_average_delay,
                total_average_delay_seconds,
                total_successful_transfers,
                total_packets_dropped,
                total_throughput
                )

simulatedNetwork = NetWork(sim_N, sim_L, sim_W, sim_A, TICK_LENGTH, sim_P, SIM_DURATION * 5)
simulatedNetwork.simulateTickSkip()
simulatedNetwork.logStatistics()
