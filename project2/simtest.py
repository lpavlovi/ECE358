from Node import Node
import random
from NodeStates import NodeState
import math

sim_L = 1500
sim_W = 1000000
sim_A = 10

n = Node(sim_L, sim_W, sim_W)

print n
print n.L
print n.W
print n.bit_time
print n.bit_ticks
print n.current_state
