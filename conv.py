#!/bin/python

import sys

NANO_SECOND = 1e-9
TICK_LENGTH = 10.0 * NANO_SECOND

if len(sys.argv) == 2:
    ticks = float(sys.argv[1])
    to_seconds = ticks * TICK_LENGTH
    print "%f" % to_seconds

if len(sys.argv) == 3:
    ticks_one = float(sys.argv[1])
    ticks_two = float(sys.argv[2])
    to_seconds_one = ticks_one * TICK_LENGTH
    to_seconds_two = ticks_two * TICK_LENGTH
    delta_ticks   =  ticks_two - ticks_one
    delta_seconds =  to_seconds_two - to_seconds_one
    print "%f" % to_seconds_one
    print "%f" % to_seconds_two
    print "Delta:    %f" % delta_ticks
    print "Delta(s): %f" % delta_seconds

