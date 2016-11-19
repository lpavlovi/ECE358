import logging
import logging.handlers
import sys

fname = sys.argv[2] if len(sys.argv) == 3 else 'net'
simLog = logging.getLogger('Sim')
stream_handler = logging.StreamHandler()
file_handler = logging.FileHandler('/tmp/%s.log' % fname)


simLog.addHandler(stream_handler)
simLog.addHandler(file_handler)
simLog.setLevel(logging.WARN)

