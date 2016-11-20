import logging
import logging.handlers
import sys

nodeLog = logging.getLogger('Node')

fname = sys.argv[2] if len(sys.argv) == 3 else 'net'
stream_handler = logging.StreamHandler()

#file_handler = logging.FileHandler('/tmp/%s.log' % fname)
#nodeLog.addHandler(file_handler)

nodeLog.addHandler(stream_handler)
nodeLog.setLevel(logging.DEBUG)

def nodeInit(node_id):
    nodeLog.info("Node %03d Initialized" % (node_id));

def nextPacket(node_id, current_tick):
    nodeLog.info("Node %03d Next Packet: %s" % (node_id, current_tick));

def packetArrived(node_id, current_tick):
    nodeLog.info("Node %03d Packet Arrived - %s" % (node_id, current_tick));

def stateChanged(node_id, state, current_tick):
    nodeLog.info("Node %03d %s - %s" % (node_id, state, current_tick));

def txSuccess(node_id, current_tick, packet):
    nodeLog.info("Node %03d Transmission Successful: %s - at %s" % (node_id, current_tick, packet));

def bebError(node_id, current_tick, packet):
    nodeLog.info("Node %03d Transmission Successful: %s - at %s" % (node_id, current_tick, packet));
