from enum import Enum
import math


class Stage(Enum):
    WAITING_TO_START = 0
    SWITCH_TO_COUNTING = 1
    COUNTING = 2
    BLINKED = 3
    WAITING = 4


class Firefly_State():
    def __init__(self, start_counter):
        self.STAGE = Stage.WAITING_TO_START
        self.start_counter = start_counter
        self.current_counter = 0
        self.waiting_counter = 0
        self.num_received_signals = 0

    def resetSignals(self):
        self.num_received_signals = 0


class FireFly():
    def __init__(self, id, x_coord, y_coord, period, period_threshold, waiting_time, sub_time_fun, add_time_fun,
                 start_delay=0, group_id = 0):
        self.id = id
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.period = period
        self.start_delay = start_delay
        self.waiting_time = waiting_time
        self.add_time_fun = add_time_fun    # function which will be adding to the current period, function depends on current period
        self.sub_time_fun = sub_time_fun    # function which will be subtracting from the current period, function depends on current period
        self.got_signal_count = 0
        self.neigbours = []
        self.half_of_neighbours = 0
        self.period_threshold = period_threshold
        self.group_id = group_id

        self.previous_state = Firefly_State(start_delay)
        self.current_state = Firefly_State(start_delay)
        self.next_state = Firefly_State(start_delay)

    def applyMove(self, time_step):
        current_state, next_state, previous_state = self.current_state, self.next_state, self.previous_state
        if current_state.STAGE == Stage.WAITING_TO_START:
            self.waitToStart(current_state, next_state, time_step)
        elif current_state.STAGE == Stage.SWITCH_TO_COUNTING:
            previous_state.resetSignals()
            self.countingDown(current_state, previous_state, next_state, time_step)
        elif current_state.STAGE == Stage.COUNTING:
            self.countingDown(current_state, previous_state, next_state, time_step)
        else:
            self.waiting(current_state, next_state, time_step)

        next_state.resetSignals()

    def waitToStart(self, current_state, next_state, time_step):
        current_state.start_counter -= time_step
        if (current_state.start_counter <= 0):
            next_state.STAGE = Stage.SWITCH_TO_COUNTING
            next_state.current_counter = self.period + current_state.start_counter
        else:
            next_state.start_counter = current_state.start_counter
            next_state.STAGE = Stage.WAITING_TO_START

    def countingDown(self, current_state, previous_state, next_state, time_step):
        current_state.current_counter -= time_step
        self.got_signal_count += previous_state.num_received_signals
        self.countingDownHelp(current_state, next_state)
        if current_state.current_counter <= 0:
            return

        if self.period < self.period_threshold:
            self.period = self.period_threshold
        elif previous_state.num_received_signals > 0:
            sub_value = self.sub_time_fun(self.period)
            current_state.current_counter -= sub_value
            self.period -= sub_value
            self.countingDownHelp(current_state, next_state)


    def countingDownHelp(self, current_state, next_state):
        if current_state.current_counter <= 0:
            next_state.STAGE = Stage.BLINKED
            next_state.waiting_counter = self.waiting_time + current_state.current_counter
            if self.got_signal_count < self.half_of_neighbours:
                self.period += self.add_time_fun(self.period)
            self.got_signal_count = 0
            for n in self.neigbours:
                n.current_state.num_received_signals += 1
        else:
            next_state.current_counter = current_state.current_counter
            next_state.STAGE = Stage.COUNTING

    def waiting(self, current_state, next_state, time_step):
        current_state.waiting_counter -= time_step
        if current_state.waiting_counter <= 0:
            next_state.current_counter = self.period + current_state.waiting_counter
            next_state.STAGE = Stage.COUNTING
        else:
            next_state.waiting_counter = current_state.waiting_counter
            next_state.STAGE = Stage.WAITING

    def setNeighbours(self, neighbours):
        if not isinstance(neighbours, list):
            self.neigbours = [neighbours]
        else:
            self.neigbours = neighbours
        self.half_of_neighbours = math.ceil(len(self.neigbours))