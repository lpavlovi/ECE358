import logging
import logging.handlers
import sys

nodeLog = logging.getLogger('Node')
simLog = logging.getLogger('Sim')

fname = 'Project2Simulation'
file_handler = logging.FileHandler('%s.log' % fname)

stream_handler = logging.StreamHandler()

simLog.addHandler(file_handler)
simLog.addHandler(stream_handler)
simLog.setLevel(logging.INFO)

nodeLog.addHandler(stream_handler)
nodeLog.setLevel(logging.INFO)

def logSimulationStats(average_delay, successful_transfers, packets_dropped):
    simLog.info("Simulation - Average Delay: %f - Successful Transfers: %d - Packets Dropped: %d" % (average_delay, successful_transfers, packets_dropped));

def logNodeStats(node_id, average_delay, successful_transfers, packets_dropped):
    simLog.info("Node %02d - Average Delay: %f - Successful Transfers: %d - Packets Dropped: %d" % (node_id, average_delay, successful_transfers, packets_dropped));

def nodeInit(node_id):
    nodeLog.info("Node %03d Initialized" % (node_id));

def nextPacket(node_id, next_packet):
    nodeLog.info("Node %03d Next Packet: %s" % (node_id, next_packet));

def packetArrived(node_id, current_tick):
    nodeLog.debug("Node %03d Packet Arrived - %s" % (node_id, current_tick));

def stateChanged(node_id, state, current_tick):
    nodeLog.debug("Node %03d %s - %s" % (node_id, state, current_tick));

def txSuccess(node_id, current_tick, packet):
    nodeLog.info("Node %03d Transmission Successful: %s - at %s" % (node_id, packet, current_tick));

def bebError(node_id, current_tick, packet):
    nodeLog.error("Node %03d Transmission Error %s - at %s" % (node_id, packet, current_tick));
