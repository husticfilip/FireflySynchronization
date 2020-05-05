import threading
import time
from utils import  *
from display import *
from iterator import *

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
    population = generate_population_manualy()
    time_step = 0.5
    max_time = 10
    iterate(population, time_step, max_time)


if __name__ == "__main__":
    for _ in range(experimentation['NR_EXP']):
        #main()
        iteratingMain()
