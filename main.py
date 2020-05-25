import threading
import time
from utils import  *
from display import *
from iterator import *
import turtle
import numpy

"""
NOTES
- list to keep the fireflies that blinked each second

- Firefly reacts only to first neighbour?

THINK ABOUT THIS:
- what is the best way to work with individuals in threads ?
- how to update the blinking plot?

"""

#TODO: function to save population
# Function to load population, from json


def iteratingMain():
    population = generate_population_two_grops_different_periods()
    time_step = 0.1
    max_time = 5000
    iterate(population, time_step, max_time)

if __name__ == "__main__":
    for _ in range(experimentation['NR_EXP']):
        #main()
        iteratingMain()