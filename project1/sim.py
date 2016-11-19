import random
import math
from logmodule import simLog as log
from collections import deque

class Simulation():
    def __init__(self, TICKS, Lambda, L, C, K=None, tick_length=0.00001):
        # Input Parameters

        self.TICKS = TICKS
        # Tick length - SECONDS / TICK
        self.tick_length = tick_length

        # Packets per second - used for calculating the next arrival time
        self.Lambda = float(Lambda)

        # Buffer size
        self.K = K + 1 if not K is None else None

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
        self.packets_dropped = 0

        log.info('Simulation lasts %s ticks' % self.TICKS)
        log.info('Simulation covers %s seconds' % (self.TICKS * self.tick_length))
        log.info('Server Proc Duration (ticks): %s' % self.server_proc_duration)
        log.info('Lambda: %s' % self.Lambda)

    def calcArrivalTime(self):
        u = random.uniform(0,1)
        aa = (-1.0 / self.Lambda)
        bb = math.log(1.0 - u)
        arrival_time_sec = aa * bb
        arrival_time = arrival_time_sec / self.tick_length
        discrete_arrival_time = int(round(arrival_time, 0))

        log.debug('u: %s' % u)
        log.debug('-1 / Lambda = %s' % aa)
        log.debug('log (1 - u) = %s' % bb)
        log.debug('arrival_time_sec: %s' % arrival_time_sec)
        log.debug('arrival_time: %s' % arrival_time)
        log.debug('discrete_arrival_time: %s' % discrete_arrival_time)

        return discrete_arrival_time if discrete_arrival_time > 0 else 1

    def arrival(self, current_tick):
        if current_tick == self.arrival_tick:
            log.debug('PACKET ARRIVED: %s' % current_tick)

            # if the queue is empty - need to set new departure time
            if not self.q:
                self.updateDepartureTick(current_tick)
                log.debug('New Departure: %s' % self.departure_tick)

            if not self.K is None and len(self.q) == self.K:
                self.packets_dropped += 1
                log.debug('PACKET DROPPED: %s' % current_tick)
            else:
                self.q.append(current_tick)

            log.debug('Enque Packet: {:8d} Q: {:4d}'.format(current_tick, len(self.q)))
            self.arrival_tick = current_tick + self.calcArrivalTime()
            log.debug('NEW ARRIVAL TIME: %s' % self.arrival_tick)

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

    def run(self):
        self.arrival_tick = self.calcArrivalTime()
        log.debug('Next Arrival: %s' % self.arrival_tick)

        for i in xrange(self.TICKS):
            self.arrival(i)
            self.departure(i)
            self.packets_in_queue[i] = len(self.q)

        # log.debug('QUEUE:\n%s' % self.q)

        avg_sojourn_time = float(sum(self.sojourn_time)) / float(len(self.sojourn_time))
        packets_in_queue = 0
        for i in self.packets_in_queue:
            packets_in_queue += (i - 1) if i > 0 else 0
        avg_queue_load = float(packets_in_queue) / float(self.TICKS)

        p_idle = float(self.packets_in_queue.count(0)) / float(self.TICKS)
        p_loss = ( float(self.packets_dropped) / float(len(self.sojourn_time) + self.packets_dropped) ) if not self.K is None else None

        """
        log.info('---:: RUN STATISTICS ::---')
        log.info('Average Sojourn Time: %s' % avg_sojourn_time )
        log.info('Average Queue Load:   %s' % avg_queue_load )
        log.info('Server Idle Ratio:    %s' % p_idle )
        log.info('Packet Drop Ratio:    %s' % p_loss )
        log.info('Total Packets Arrived: %s' % len(self.sojourn_time) )
        log.info('Number of packets dropped: %s' % self.packets_dropped )
        """

        #log.debug('%s' % self.packets_in_queue )

        return {'avg_queue_load': avg_queue_load,
                'avg_sojourn_time': avg_sojourn_time,
                'p_idle': p_idle, 
                'p_loss': p_loss}

