import logging
import logging.handlers
import sys

nodeLog = logging.getLogger('Node')
simLog = logging.getLogger('Sim')
mediumLog = logging.getLogger('Medium')

#persistence = sys.argv[3] if  len(sys.argv) == 4 else 'N'
#fname = 'sim_N%d_A%d_P%s' % (int(sys.argv[1]), int(sys.argv[2]), persistence)
#file_handler = logging.FileHandler('./simulation_logs/%s.log' % fname)
file_handler = logging.FileHandler('./simulation_logs/sim_log.csv')

stream_handler = logging.StreamHandler()

simLog.addHandler(file_handler)
simLog.addHandler(stream_handler)
simLog.setLevel(logging.INFO)

mediumLog.addHandler(stream_handler)
mediumLog.setLevel(logging.WARN)

nodeLog.addHandler(stream_handler)
nodeLog.setLevel(logging.CRITICAL)


def logSimulationStatsV3(N, A, W, P, L, simulation_duration_seconds, average_delay, average_delay_seconds, successful_transfers, packets_dropped, tput):
    simLog.info("%s,%s,%s,%s,%s,%f,%f,%f,%d,%d,%d" % (N, A, W, P, L, simulation_duration_seconds, average_delay, average_delay_seconds, successful_transfers, packets_dropped, tput));

def logSimulationStatsV2(simulation_duration_seconds, average_delay, average_delay_seconds, successful_transfers, packets_dropped, tput):
    simLog.info("Simulation - Duration: %f - Average Delay: %f - Average Delay Seconds: %f - Successful Transfers: %d - Packets Dropped: %d - TPUT: %d" % (simulation_duration_seconds, average_delay, average_delay_seconds, successful_transfers, packets_dropped, tput));

def logSimulationStats(simulation_duration_seconds, average_delay, average_delay_seconds, successful_transfers, packets_dropped):
    simLog.info("Simulation - Simulation Duration: %f - Average Delay: %f - Average Delay Seconds: %f - Successful Transfers: %d - Packets Dropped: %d" % (simulation_duration_seconds ,average_delay, average_delay_seconds, successful_transfers, packets_dropped));

def logNodeStats(node_id, average_delay, successful_transfers, packets_dropped):
    simLog.debug("Node %02d - Average Delay: %f - Successful Transfers: %d - Packets Dropped: %d" % (node_id, average_delay, successful_transfers, packets_dropped));

def nodeInit(node_id):
    nodeLog.info("Node %03d Initialized" % (node_id));

def nextPacket(node_id, next_packet):
    nodeLog.info("Node %03d Next Packet: %s" % (node_id, next_packet));

def packetArrived(node_id, current_tick):
    nodeLog.debug("Node %03d Packet Arrived - %s" % (node_id, current_tick));

def stateChanged(node_id, state, current_tick):
    nodeLog.debug("Node %03d %s - %s" % (node_id, state, current_tick));

def txSuccess(node_id, current_tick, packet, packet_delay, packet_delay_seconds):
    nodeLog.info("Node %03d Transmission Successful: %s - at %s - Delay: %f - Delay(s): %f" % (node_id, packet, current_tick, packet_delay, packet_delay_seconds));

def bebError(node_id, current_tick, packet):
    nodeLog.error("Node %03d Transmission Error %s - at %s" % (node_id, packet, current_tick));

def bebStatus(node_id, i, current_tick, backoff_duration):
    nodeLog.error("Node %03d BEB - i: %d Start: %d - End: %d" % (node_id, i, current_tick, backoff_duration));
