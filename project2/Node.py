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
        self.waiting_duration = 0

        # The backoff duration is initialized to 0
        self.backoff_duration = 0

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
        self.i = 0
        loggingModule.stateChanged(self.id, NodeState.SENSING, current_tick)

    def setTransmititngState(self, current_tick):
        self.current_state = NodeState.TRANSMITTING
        self.servicing_milestone = int(current_tick + self.transmission_duration)
        loggingModule.stateChanged(self.id, NodeState.TRANSMITTING, current_tick)

    def setBackoffState(self, current_tick):
        self.current_state = NodeState.BACKOFF

        self.i += 1
        if self.i > 10:
            loggingModule.bebError(self.id, current_state, self.server)
            self.packets_dropped += 1
            self.serviceNextPacket(current_state)
        upperbound = int(math.pow(2,i)) - 1
        R = random.randrange(0,upperbound)
        self.backoff_duration = self.Tp * R
        self.waiting_duration = self.backoff_duration

        new_backoff_duration = int(current_tick + self.backoff_duration)
        self.servicing_milestone = new_backoff_duration if new_backoff_duration > 0 else 1
        loggingModule.stateChanged(self.id, NodeState.BACKOFF, current_tick)

    def setWaitingState(self, current_tick):
        self.current_state = NodeState.WAITING
        new_wait_duration = int(current_tick + self.waiting_duration)
        self.servicing_milestone = new_wait_duration if new_wait_duration > 0 else 1
        loggingModule.stateChanged(self.id, NodeState.WAITING, current_tick)

    def setJammingState(self, current_tick):
        self.current_state = NodeState.JAMMING
        self.servicing_milestone = int(current_tick + self.jamming_duration)
        self.Medium.sendJammingSignal(self.jamming_duration, current_tick)
        loggingModule.stateChanged(self.id, NodeState.JAMMING, current_tick)

    def isMediumBusy(self, current_tick):
        # TODO: Not yet implemented
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
                self.setJammingState()

            # If transmission successfully complete:
            # begin servicing next packet from queue
            # if queue is empty - go to idle state
            elif self.servicing_milestone == current_tick:
                loggingModule.txSuccess(self.id, current_tick, self.server)

                # Track the successful transfers and total delay
                self.successful_transfers += 1
                self.delay_sum += (current_tick - self.server)

                self.serviceNextPacket(current_tick)

        # JAMMING
        elif self.current_state == NodeState.JAMMING:
            if self.servicing_milestone == current_tick:
                self.setBackoffState(current_tick)

        # BACKOFF
        elif self.current_state == NodeState.BACKOFF:
            if self.servicing_milestone == current_tick:
                self.setSensingState(current_tick)

        # WAITING
        elif self.current_state == NodeState.WAITING:
            if self.servicing_milestone == current_tick:
                self.setSensingState(current_tick)


    def run(self, current_tick):
        self.arrival(current_tick)
        self.servicing(current_tick)

    def getStatistics(self):
        return [self.delay_sum, self.successful_transfers, self.packets_dropped]
