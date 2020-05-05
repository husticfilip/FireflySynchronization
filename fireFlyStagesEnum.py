from enum import Enum

class Stage(Enum):
    WAITING_TO_START = 0
    COUNTING_DOWN = 1
    BLINKED = 2
    WAITING_AFTER_BLINKING = 3