from utils import  generate_population
from iterator import iterator
from parameters import params, experimentation


def iteratingMain():
    population = generate_population()
    time_step = params['TIME_STEP']
    max_time = params['SIMULATION_TIME']

    iterator(population, time_step, max_time)

if __name__ == "__main__":
    for _ in range(experimentation['NR_EXP']):
        iteratingMain()