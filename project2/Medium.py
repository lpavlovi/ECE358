class Medium():
    def __init__(self, N, propagation_speed, distance_between_nodes, tick_length):
        self.N = N
        self.propagation_delay = int((distance_between_nodes/propagation_speed) / tick_length)
        self.node_transfer_times = [[0,0] for x in xrange(N)]

    def startTransmission(self, n, current_tick):
        [self.setTransmissionStart(self.node_transfer_times[x], current_tick) for x in xrange(self.N) if x != n ]

    def sendJammingSignal(self, jamming_duration, current_tick):
        [self.setTransmissionEnd(self.node_transfer_times[x], current_tick + jamming_duration) for x in xrange(self.N)]

    def setTransmissionStart(self, tx_time, starting_tick):
        tx_time[0] = starting_tick + self.propagation_delay
        tx_time[1] = 0

    def setTransmissionEnd(self, tx_time, ending_tick):
        tx_time[0] = 0
        tx_time[1] = ending_tick + self.propagation_delay

    def isCarrierBusy(self, n, current_tick):
        node_times = self.node_transfer_times[n]

        if node_times[0] == 0 and node_times[1] == 0:
            return False

        if node_times[0] > 0  and node_times[0] <= current_tick:
            return True

        if node_times[1] > 0  and node_times[1] > current_tick:
            return True

        return False


"""
[ 0000 , 1305]
[ 0000 , 1305]
[ 0000 , 1305]
"""
