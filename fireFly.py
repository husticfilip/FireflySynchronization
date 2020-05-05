from fireFlyStagesEnum import Stage
import math
import time
from display import update_plot

global EVEN_ITERATION # flag which tells all fireflies if current iteration is even or odd
                      # used when one firefly looks if it has set signals from other ff in
                      # previous iteration

class FireFly:

    def __init__(self,id ,x_coord, y_coord, period, sub_time ,sub_period_fun, add_period_fun, wait_time, start_delay = 0):
        self.id = id
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.period = period
        self.sub_time = sub_time
        self.sub_period_fun = sub_period_fun
        self.add_period_fun = add_period_fun
        self.wait_time = wait_time
        self.neighbours = None
        self.half_of_neighbours = 0
        self.start_delay = start_delay

        #support for iterator
        self.STAGE = Stage.WAITING_TO_START
        self.current_time_counting = self.period
        self.current_time_waiting = self.wait_time
        self.blinked = False
        self.signal_flag = False

        self.even_iteration_signal_set = False # has signal from some other ff been set on its even iteration
        self.odd_iteration_signal_set = False  # or has it been set on odd iteration

    def applyMove(self, time_step):
        if self.STAGE == Stage.WAITING_TO_START:
            self.waitingToStartFunction(time_step)
        elif self.STAGE == Stage.COUNTING_DOWN:
            self.countingDownFunction(time_step)
        elif self.STAGE == Stage.BLINKED:
            self.STAGE = Stage.WAITING_AFTER_BLINKING
            self.waitingFunction(time_step)
        else:
            self.waitingFunction(time_step)

    def waitingToStartFunction(self, time_step):
        self.start_delay -= time_step
        if self.start_delay <= 0:
            self.STAGE = Stage.COUNTING_DOWN
            self.current_time_counting += self.start_delay  # subtract time to start counting

    def countingDownFunction(self, time_step):
        global EVEN_ITERATION
        if (EVEN_ITERATION and self.odd_iteration_signal_set) or (not EVEN_ITERATION and self.even_iteration_signal_set): # we need to look at signals from previous iteration
            self.signal_flag = True
            self.current_time_counting -= self.sub_time
            self.period -= self.sub_period_fun(self.period)
            if EVEN_ITERATION:
                self.odd_iteration_signal_set = False
            else:
                self.even_iteration_signal_set = False

        self.current_time_counting -= time_step
        if self.current_time_counting<=0:
            self.blink()
            if not self.signal_flag:
                self.period -= self.sub_period_fun(self.period)

            self.signal_flag = False            # so next time we start counting all flags are set on False
            self.odd_iteration_signal_set = False
            self.even_iteration_signal_set = False

            self.STAGE = Stage.BLINKED
            self.current_time_waiting += self.current_time_counting
            self.current_time_counting = self.period


    def waitingFunction(self, time_step):
        self.current_time_waiting -= time_step
        if self.current_time_waiting <= 0:
            self.STAGE = Stage.COUNTING_DOWN
            self.current_time_counting += self.current_time_waiting
            self.current_time_waiting = self.wait_time

    def blink(self):
        global EVEN_ITERATION
        self.blinked = True
        for neighbour in self.neighbours:
            if neighbour.STAGE == Stage.COUNTING_DOWN:
                if EVEN_ITERATION:
                    neighbour.even_iteration_signal_set = True
                else:
                    neighbour.odd_iteration_signal_set = True

    def setNeighbours(self, neigbours):
        if not isinstance(neigbours,list):
            raise ValueError("Set neighbours method takes in list of neighbours.")
        self.neighbours = neigbours
        self.half_of_neighbours = math.ceil (len(neigbours) / 2)



# Class for paralelization run, multithreading
class FireFlyParallel:

    def __init__(self, id ,x_coord, y_coord, period, subtraction_time, add_period_function, latency):
        self.id = id
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.period = period
        self.subtraction_time = subtraction_time
        self.add_period_function = add_period_function
        self.neighbours = None
        self.half_of_neighbours = 0
        self.number_of_signals = 0
        self.latency = latency
        self.isBlinking = False

    def run(self):
        while True:
            current_period = self.period
            while current_period > 0:
                if self.number_of_signals:
                    current_period -= self.subtraction_time
                    self.resetSignal()
                current_period -= 0.5
                time.sleep(0.5)
            self.signal()

            #TODO do something smart with latency
            self.blinking = True
            time.sleep(self.latency)
            self.blinking = False

            if self.half_of_neighbours > self.number_of_signals:
                self.period += self.add_period_function(self.period)
            self.resetSignal()


    def signal(self):
        #update_plot(self)
        for neighbour in self.neighbours:
            neighbour.setSignal()

    def setSignal(self):
        self.number_of_signals += 1

    def resetSignal(self):
        self.number_of_signals = 0

    def setNeighbours(self, neigbours):
        if not isinstance(neigbours,list):
            raise ValueError("Set neighbours method takes in list of neighbours.")
        self.neighbours = neigbours
        self.half_of_neighbours = len(neigbours) / 2


