import logging

simLog = logging.getLogger('Sim')

handler = logging.StreamHandler()

simLog.addHandler(handler)
simLog.setLevel(logging.WARN)

