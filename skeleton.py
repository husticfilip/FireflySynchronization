import threading
import numpy
import random
import pandas
import matplotlib.pyplot as plt
from parameters import params, experimentation
from Firefly import Firefly
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

def generate_population():
    population = []
    for id in range(params['POP_SIZE']):
        firefly = Firefly(id)
        firefly.generate_position(params['POSITION_MODE'], params['X_MAX'], params['Y_MAX'])
        firefly.generate_latency(params['LATENCY_MAX'])
        firefly.generate_frequency(params['FREQUENCY_MAX'])
        population.append(firefly)
    return population

def display_population(population):
    x = [i.get_x() for i in population]
    y = [i.get_y() for i in population]
    
    plt.figure(0)
    plt.xlim(0, params['X_MAX'])
    plt.ylim(0, params['Y_MAX'])
    plt.scatter(x,y, c="black")
    return plt

def update_plot(population):
    x_on = [i.get_x() for i in population if i.isBlinking()]
    x_off = [i.get_x() for i in population if not i.isBlinking()]
    y_on = [i.get_y() for i in population if i.isBlinking()]
    y_off = [i.get_y() for i in population if not i.isBlinking()]
    
    plt.scatter(x_off,y_off, c="black")
    plt.scatter(x_on, y_on, c="red")

def main():
    population = generate_population()
    display_population(population)
    
    for _ in range(params["SIMULATION_TIME"]):
        # TODO: thread to update each firefly
        # input()
        # TODO: add decay on blinking
        # random "blinking" just for test
        population[random.randint(0,params["POP_SIZE"] - 1)].blinking = not population[random.randint(0,params["POP_SIZE"] - 1)].blinking

        plt.pause(0.5)
        update_plot(population)
    plt.show()


if __name__ == "__main__":
    for _ in range(experimentation['NR_EXP']):
        main()
