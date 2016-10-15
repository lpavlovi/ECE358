from sim import Simulation
import time, sys

# Simulation Variables
sim_L = float(2000)
sim_C = float(1024*1024)
sim_p = float(sys.argv[1]) if len(sys.argv) >= 2 else float(0.2)
sim_K = 50

sim_TICKS = 100000
sim_Lambda = (sim_p * sim_C) / sim_L

sim_results = []
runs = 1

# RUN TESTS
for i in xrange(runs):
    simulation = Simulation(TICKS=sim_TICKS, Lambda=sim_Lambda, L=sim_L, C=sim_C, K=sim_K)
    sim_results.append(simulation.run())

# CALCULATE AVERAGES
avg_queue_load = 0.0
avg_sojourn_time = 0.0
p_idle = 0.0
p_loss = 0.0 if not sim_K is None else None

for i in xrange(runs):
    avg_sojourn_time += sim_results[i]['avg_sojourn_time']
    avg_queue_load += sim_results[i]['avg_queue_load']
    p_idle += sim_results[i]['p_idle']
    if not sim_K is None:
        p_loss = float(sim_results[i]['p_loss'])

p_idle = p_idle / runs
avg_queue_load = avg_queue_load / runs
avg_sojourn_time = avg_sojourn_time / runs

if not sim_K is None:
    p_loss = float(p_loss) / float(runs)

print "p: %s" % sim_p
print "P_idle: %s" % p_idle

if not sim_K is None:
    print "P_loss: %s" % p_loss

print "E[T]: %s" % avg_sojourn_time
print "E[N]: %s" % avg_queue_load

