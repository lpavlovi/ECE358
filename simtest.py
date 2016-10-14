from sim import Simulation
import time
sim_results = []
runs = 5

# RUN TESTS
for i in xrange(runs):
    simulation = Simulation(TICKS=100000, Lambda=471.85, L=2000, C=1024*1024, K=None, tick_length=0.00001)
    sim_results.append(simulation.run())

# CALCULATE AVERAGES
avg_queue_load = 0.0
avg_sojourn_time = 0.0
p_idle = 0.0

for i in xrange(runs):
    avg_sojourn_time += sim_results[i]['avg_sojourn_time']
    avg_queue_load += sim_results[i]['avg_queue_load']
    p_idle += sim_results[i]['p_idle']
    time.sleep(1)

p_idle = p_idle / runs
avg_queue_load = avg_queue_load / runs
avg_sojourn_time = avg_sojourn_time / runs

print "P IDLE: %s" % p_idle
print "Average Sojourn Time: %s" % avg_sojourn_time
print "Average Queue Load: %s" % avg_queue_load

