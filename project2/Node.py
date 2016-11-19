import random
import math
from NodeStates import NodeState
from logmodule import simLog as log
from collections import deque

class Node():
    def __init__(self, L, W, A, tick_length=0.00000001):
        """
        Inputs:
          L: Lenght of Packet in bytes
          W: Speed of LAN (bits / second)
          A: Packet Arrival (packets/second)
          tick_length: length of tick in seconds - defaults to 10 ns
        """

        self.tick_length = tick_length
        # Lenght of Packet in bits
        self.L = L * 8
        self.W = W
        self.q = deque()
        self.bit_time = 1.00 / float(W)
        # Number of ticks it takes to advance a single bit time
        self.bit_ticks = self.bit_time / tick_length

        # Number of ticks it required to transmit an entire packet
        self.transmission_duration = self.L * self.bit_ticks

        # Number of ticks needed for carrier sensing
        self.sensing_duration = 96 * self.bit_ticks

        # Number of ticks that the jamming signal will last
        self.jamming_duration = 48 * self.bit_ticks

        # Tp represented with number of ticks
        self.jamming_duration = 512 * self.bit_ticks

        # Represents when the next packet will arrive
        self.arrival_tick = 0

        self.server = None

        self.current_state = NodeState.IDLE

    def calcArrivalTime(self):
        u = random.uniform(0,1)
        arrival_time_sec = (-1.0 / self.A) * math.log(1.0 - u)
        arrival_time = arrival_time_sec / self.tick_length
        discrete_arrival_time = int(round(arrival_time, 0))

        return discrete_arrival_time if discrete_arrival_time > 0 else 1

    def arrival(self, current_tick):
        if current_tick == self.arrival_tick:
            # If the server is IDLE
            if self.current_state == NodeState.IDLE:
                assert(self.server is None, "Server is not None while Node is in IDLE state")
                self.server = current_tick
                self.setSensingState(current_tick)

            # Add packet to queue
            else:
                self.q.append(current_tick)

            # Update next packet arrival time
            self.updateArrivalTick(current_tick)

    def updateArrivalTick(self, current_tick):
        self.arrival_tick = current_tick + self.calcArrivalTime()

    """
    def updateDepartureTick(self, current_tick):
        self.departure_tick = current_tick + self.server_proc_duration
    """

    def setIdleState(current_tick):
        # TODO: Revisit method later
        self.current_state = NodeState.IDLE
        self.servicing_milestone = 0

    def setSensingState(current_tick):
        self.current_state = NodeState.SENSING
        self.servicing_milestone = current_tick + self.sensing_duration

    def setTransmititngState(current_tick):
        self.current_state = NodeState.TRANSMITTING
        self.servicing_milestone = current_tick + self.transmission_duration

    def setBackoffState(current_tick):
        self.current_state = NodeState.TRANSMITTING
        self.servicing_milestone = current_tick + self.transmission_duration

    def setWaitingState(current_tick):
        self.current_state = NodeState.WAITING
        # TODO: Calculate waiting duration
        # This implementation is wrong - just a placeholder
        self.servicing_milestone = current_tick + 24 * self.bit_ticks

    def sendJammingSignal(self):
        print "sendJammingSignal not yet implemented"
        return

    def isMediumBusy(self):
        return False

    def servicing(self, current_tick):
        if self.current_state == NodeState.SENSING:
            # TODO: Check medium for any signal
            if self.isMediumBusy(current_tick):
                self.setWaitingState(current_tick)

            if self.servicing_milestone == current_tick:
                self.setTransmititngState(current_tick)

        if self.current_state == NodeState.TRANSMITTING:
            # TODO: Check medium for any signal
            if self.isMediumBusy(current_tick):
                self.setJammingState()

            # If transmission successfully complete:
            # begin servicing next packet from queue
            # if queue is empty - go to idle state
            if self.servicing_milestone == current_tick:
                # TODO: Implement start servicing next packet in queue
                self.setSensingState(current_tick)

        if self.current_state == NodeState.JAMMING:
            self.sendJammingSignal()

            if self.servicing_milestone == current_tick:
                self.setBackoffState(current_tick)


        if self.current_state == NodeState.BACKOFF:
            if self.servicing_milestone == current_tick:
                self.setSensingState(current_tick)

        if self.current_state == NodeState.WAITING:
            if self.servicing_milestone == current_tick:
                self.setSensingState(current_tick)

