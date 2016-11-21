import random
import math
import loggingModule
from NodeStates import NodeState
from collections import deque

class Node():
    def __init__(self, L, W, A, _id, tick_length, Medium):
        """
        Inputs:
          L: Lenght of Packet in bytes
          W: Speed of LAN (bits / second)
          A: Packet Arrival (packets/second)
          tick_length: length of tick in seconds - defaults to 10 ns
        """
        self.id = _id

        self.tick_length = tick_length
        # Lenght of Packet in bits
        self.L = L * 8
        self.W = W
        self.A = A
        self.q = deque()
        self.Medium = Medium
        self.bit_time = 1.00 / float(W)
        # Number of ticks it takes to advance a single bit time
        self.bit_ticks = self.bit_time / tick_length

        # Tp represented with number of ticks
        self.Tp = 512 * self.bit_ticks

        # Number of ticks it required to transmit an entire packet
        self.transmission_duration = self.L * self.bit_ticks

        # Number of ticks needed for carrier sensing
        self.sensing_duration = 96 * self.bit_ticks

        # Number of ticks that the jamming signal will last
        self.jamming_duration = 48 * self.bit_ticks

        # The waiting duration is initialized to 0
        self.waiting_duration = self.Tp

        self.servicing_milestone = 0
        self.intermediate_milestone = 0

        # Represents when the next packet will arrive
        self.arrival_tick = 0

        self.server = None

        self.current_state = NodeState.IDLE
        self.i = 0
        self.updateArrivalTick(0)

        # Stat Tracking
        self.successful_transfers = 0
        self.packets_dropped = 0
        self.delay_sum = 0

        loggingModule.nodeInit(self.id)

    def getClosestEvent(self, current_tick):
        if self.intermediate_milestone != 0 and self.intermediate_milestone > current_tick:
            ret_val = self.intermediate_milestone
            self.intermediate_milestone = 0
            return ret_val

        if self.servicing_milestone != 0 and self.arrival_tick != 0:
            return min(self.servicing_milestone, self.arrival_tick)
        if self.arrival_tick == 0:
            return self.servicing_milestone
        else:
            return self.arrival_tick

    def calcArrivalTime(self):
        u = random.uniform(0,1)
        arrival_time_sec = (-1.0 / self.A) * math.log(1.0 - u)
        arrival_time = arrival_time_sec / self.tick_length
        discrete_arrival_time = int(round(arrival_time, 0))

        return discrete_arrival_time if discrete_arrival_time > 0 else 1

    def updateArrivalTick(self, current_tick):
        self.arrival_tick = current_tick + self.calcArrivalTime()
        loggingModule.nextPacket(self.id, self.arrival_tick)

    def serviceNextPacket(self, current_tick):
        # If the queue is empty go to IDLE state
        # Else go to SENSING state and get the next packet from the queue
        if not self.q:
            self.setIdleState(current_tick)
        else:
            self.setSensingState(current_tick)
            loggingModule.nodeLog.debug("Node %03d Queue Length: %s" % (self.id, len(self.q)))
            assert len(self.q) > 0, "Cannot service next packet when the queue is empty"
            p = self.q.popleft()
            self.server = p

    def setIdleState(self, current_tick):
        self.current_state = NodeState.IDLE
        self.servicing_milestone = 0
        self.server = None
        loggingModule.stateChanged(self.id, NodeState.IDLE, current_tick)

    def setSensingState(self, current_tick):
        self.current_state = NodeState.SENSING
        self.servicing_milestone = int(current_tick + self.sensing_duration)
        loggingModule.stateChanged(self.id, NodeState.SENSING, int(current_tick))

    def setTransmititngState(self, current_tick):
        self.current_state = NodeState.TRANSMITTING
        self.servicing_milestone = int(current_tick + self.transmission_duration)
        self.intermediate_milestone = int(current_tick + 10)
        self.Medium.startTransmission(self.id, current_tick)
        loggingModule.stateChanged(self.id, NodeState.TRANSMITTING, current_tick)

    def calculateBEB(self, i):
        upperbound = int(math.pow(2,i)) - 1
        R = random.randrange(0,upperbound)
        R = R if R > 0 else 1
        return self.Tp * R

    def setBackoffState(self, current_tick):
        self.current_state = NodeState.BACKOFF

        self.i += 1
        if self.i > 10:
            loggingModule.bebError(self.id, current_state, self.server)
            self.packets_dropped += 1
            self.serviceNextPacket(current_state)
            return

        self.waiting_duration = self.calculateBEB(self.i)

        self.servicing_milestone = self.waiting_duration + current_tick 
        loggingModule.stateChanged(self.id, NodeState.BACKOFF, current_tick)
        loggingModule.bebStatus(self.id, self.i, current_tick, self.servicing_milestone)

    def setWaitingState(self, current_tick):
        self.current_state = NodeState.WAITING

        new_wait_duration = self.waiting_duration if self.waiting_duration > 0 else 1

        self.servicing_milestone = current_tick + new_wait_duration 
        loggingModule.stateChanged(self.id, NodeState.WAITING, current_tick)

    def setJammingState(self, current_tick):
        self.current_state = NodeState.JAMMING
        self.servicing_milestone = int(current_tick + self.jamming_duration)
        self.intermediate_milestone = int(current_tick + 10)
        self.Medium.sendJammingSignal(self.jamming_duration, current_tick)
        loggingModule.stateChanged(self.id, NodeState.JAMMING, current_tick)

    def isMediumBusy(self, current_tick):
        return self.Medium.isCarrierBusy(self.id, current_tick)

    def arrival(self, current_tick):
        if current_tick == self.arrival_tick:
            loggingModule.packetArrived(self.id, current_tick)
            # If the server is IDLE
            if self.current_state == NodeState.IDLE:
                assert self.server is None, "Server is not None while Node is in IDLE state"
                self.server = current_tick
                self.setSensingState(current_tick)

            # Add packet to queue
            else:
                self.q.append(current_tick)

            # Update next packet arrival time
            self.updateArrivalTick(current_tick)


    def servicing(self, current_tick):
        # SENSING
        if self.current_state == NodeState.SENSING:
            if self.isMediumBusy(current_tick):
                self.setWaitingState(current_tick)

            elif self.servicing_milestone == current_tick:
                self.setTransmititngState(current_tick)

        # TRANSMITTING
        elif self.current_state == NodeState.TRANSMITTING:
            if self.isMediumBusy(current_tick):
                self.setJammingState(current_tick)
            # If transmission successfully complete:
            # begin servicing next packet from queue
            # if queue is empty - go to idle state
            elif self.servicing_milestone == current_tick:

                # Track the successful transfers and total delay
                packet_delay = current_tick - self.server
                self.successful_transfers += 1
                self.delay_sum += packet_delay

                loggingModule.txSuccess(self.id, current_tick, self.server, packet_delay, packet_delay * self.tick_length)

                self.i = 0
                self.Medium.finishTransmission(self.id, current_tick)
                self.serviceNextPacket(current_tick)

        # JAMMING
        elif self.current_state == NodeState.JAMMING:
            if self.servicing_milestone == current_tick:
                self.setBackoffState(current_tick)
                self.intermediate_milestone = int(current_tick + 1)

        # BACKOFF
        elif self.current_state == NodeState.BACKOFF:
            if self.servicing_milestone == current_tick:
                self.setSensingState(current_tick)
                self.intermediate_milestone = int(current_tick + 1)

        # WAITING
        elif self.current_state == NodeState.WAITING:
            if self.servicing_milestone == current_tick:
                self.setSensingState(current_tick)
                self.intermediate_milestone = int(current_tick + 1)


    def run(self, current_tick):
        self.arrival(current_tick)
        self.servicing(current_tick)

    def getStatistics(self):
        return [self.delay_sum, self.successful_transfers, self.packets_dropped]
