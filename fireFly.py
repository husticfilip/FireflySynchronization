import time
from display import update_plot
debug = 1

class FireFly:

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
           # if debug: print(time.strftime("%H:%M:%S:%MS", time.localtime()), "Firefly: ", self.id, " countownd:",self.period)
            current_period = self.period #5
            while current_period > 0:
                #if debug: print(time.strftime("%H:%M:%S:%MS", time.localtime()), "Firefly: ", self.id,"   ", current_period ,"T",self.id)
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
        if debug: print(time.strftime("%H:%M:%S:%MS", time.localtime()), "Firefly: ", self.id, " blinked")
        update_plot(self)
        for neighbour in self.neighbours:
            neighbour.setSignal()

    def setSignal(self):
        #if debug: print(time.strftime("%H:%M:%S:%MS", time.localtime()), "Firefly: ", self.id, " got signal")
        self.number_of_signals += 1

    def resetSignal(self):
        #if debug: print(time.strftime("%H:%M:%S:%MS", time.localtime()), "Firefly: ", self.id, " reseting signal ")
        self.number_of_signals = 0

    def setNeighbours(self, neigbours):
        if not isinstance(neigbours,list):
            raise ValueError("Set neighbours method takes in list of neighbours.")
        self.neighbours = neigbours
        self.half_of_neighbours = len(neigbours) / 2



