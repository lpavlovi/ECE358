import random
import math
from logmodule import simLog as log
from collections import deque

class Simulation():
    def __init__(self, TICKS, Lambda, L, C, K=None, tick_length=0.000001):
        # Input Parameters

        self.TICKS = TICKS
        # Tick length - SECONDS / TICK
        self.tick_length = tick_length

        # Packets per second - used for calculating the next arrival time
        self.Lambda = float(Lambda)

        # Buffer size
        self.K = K

        self.q = deque()

        # The number of ticks required to process a single packet
        self.server_proc_duration = int(
                round(
                    (( float(L) / float(C) ) / self.tick_length),
                    0))

        self.arrival_tick = 0
        self.departure_tick = 0

        # Stats
        self.packets_in_queue = [0]*self.TICKS
        self.sojourn_time = []

        log.info('Simulation lasts %s ticks' % self.TICKS)
        log.info('Simulation covers %s seconds' % (self.TICKS * self.tick_length))
        log.info('Server Proc Duration (ticks): %s' % self.server_proc_duration)

    def calcArrivalTime(self):
        u = random.uniform(0,1)
        arrival_time_sec = (-1.0 / self.Lambda) * math.log(1 - u)
        arrival_time = arrival_time_sec / self.tick_length
        discrete_arrival_time = int(round(arrival_time, 0))
        return discrete_arrival_time

    def arrival(self, current_tick):
        if current_tick == self.arrival_tick:
            log.debug('PACKET ARRIVED: %s' % current_tick)

            # if the queue is empty - need to set new departure time
            if not self.q:
                self.updateDepartureTick(current_tick)
                log.debug('New Departure: %s' % self.departure_tick)

            self.q.append(current_tick)
            log.debug('Enque Packet: {:8d} Q: {:4d}'.format(current_tick, len(self.q)))
            self.arrival_tick = current_tick + self.calcArrivalTime()

    def updateDepartureTick(self, current_tick):
        self.departure_tick = current_tick + self.server_proc_duration

    def departure(self, current_tick):
        if current_tick == self.departure_tick and self.q:
            p = self.q.popleft()
            log.debug('Deque Packet: {:12d} @ {:12d} Q: {:5d}'.format(p, current_tick, len(self.q)))
            st = current_tick - p
            self.sojourn_time.append(st)

            if self.q:
                self.updateDepartureTick(current_tick)
                log.debug('New Departure: %s' % self.departure_tick)

        # current_tick is past the previous departure time and queue is empty: IDLE
        # elif current_tick > self.departure_tick and not self.q:
        # log.debug('SERVRE IDLE: %s' % current_tick)

    def run(self):
        self.arrival_tick = self.calcArrivalTime()
        log.debug('Next Arrival: %s' % self.arrival_tick)

        for i in xrange(self.TICKS):
            self.arrival(i)
            self.departure(i)

            self.packets_in_queue[i] = len(self.q)

        log.debug('QUEUE:\n%s' % self.q)

        avg_sojourn_time = float(sum(self.sojourn_time)) / float(len(self.sojourn_time))
        avg_queue_load = float(sum(self.packets_in_queue)) / float(len(self.packets_in_queue))

        p_idle = (float(self.packets_in_queue.count(0)) / float(len(self.packets_in_queue))) * 100

        # TODO Calculate p_loss
        p_loss = None

        log.info('Average Sojourn Time: %s' % avg_sojourn_time )
        log.info('Average Queue Load:   %s' %   avg_queue_load )
        log.info('Server Idle Percent:  %s' %   p_idle )

        return {'avg_queue_load': avg_queue_load,
                'avg_sojourn_time': avg_sojourn_time,
                'p_idle': p_idle, 
                'p_loss': p_loss}
