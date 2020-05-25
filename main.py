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


def main():
    threads = []
    population = generate_population_manualy()
    display_population(population)

    for firefly in population:
        t = threading.Thread(target=firefly.run2)
        t.setDaemon(True)
        threads.append(t)

    for worker in threads:
        worker.start()
        time.sleep(2) #TODO remove magic number later

    for _ in range(params["SIMULATION_TIME"]):
        plt.pause(0.5)
        update_plot(population)
    plt.show()
    t.join()

def iteratingMain():
    screen = turtle.Screen()
    screen.setup(700,700,startx=0, starty=0)
    screen.setworldcoordinates(0,0,params["Y_MAX"] + 2,params["X_MAX"] + 2)
    screen.title("Synchronized Fireflies")
    population = generate_population_randomly()
    time_step = 0.1
    max_time = 5000
    iterate(population, time_step, max_time)

if __name__ == "__main__":
    for _ in range(experimentation['NR_EXP']):
        #main()
        #iteratingMain()
        test()