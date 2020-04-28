import random

class Firefly:
    def __init__(self, id):
        self.id = id
        self.position = []
        self.frequency = 0
        self.latency = 0 # not used yet
        self.blinking = False

    def generate_position(self, mode, x_max, y_max):
        # 0 - automatic, 1 - manual
        if mode == 0:
            x = random.uniform(0, x_max)
            y = random.uniform(0, y_max)
            self.position = [x,y]
        else:
            # TODO: choose positions manually
            pass
    
    def generate_latency(self, l_max):
        self.latency = random.randint(0,l_max)

    def generate_frequency(self, f_max):
        self.frequency = random.randint(0, f_max)

    def get_position(self):
        return self.position

    def get_x(self):
        return self.position[0]

    def get_y(self):
        return self.position[1]

    def isBlinking(self):
        return self.blinking

    # TODO: get nearest firefly