from enum import Enum

class NodeState(Enum):
    IDLE         = 1
    SENSING      = 2
    TRANSMITTING = 3
    JAMMING      = 4
    BACKOFF      = 5
    WAITING      = 6
    PROBABILITY  = 7
