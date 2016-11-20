from Node import Node
import random
from NodeStates import NodeState
import math

sim_L = 1500
sim_W = 1000000
sim_A = 10

n = Node(sim_L, sim_W, sim_A, 0.000001)

print n
print n.bit_time
print n.bit_ticks
print n.transmission_duration

for ct in xrange(0, 8518727):
    n.run(ct)

