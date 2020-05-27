import threading
import time
from utils import  *
from display import *
from iterator import *
import turtle
import numpy
from parameters import params

"""
NOTES
- list to keep the fireflies that blinked each second

- Firefly reacts only to first neighbour?

THINK ABOUT THIS:
- what is the best way to work with individuals in threads ?
- how to update the blinking plot?

"""

def iteratingMain():
    population = generate_population()
    # save_scenario(population)
    # population = load_scenario()
    
    time_step = 0.1
    max_time = params['SIMULATION_TIME']
    saveIterator(population, time_step, max_time)

if __name__ == "__main__":
    for _ in range(experimentation['NR_EXP']):
        iteratingMain()