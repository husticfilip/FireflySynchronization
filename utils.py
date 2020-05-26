import random
import math
from parameters import params, experimentation
from sklearn.neighbors import KDTree
from fireFly import FireFly
import numpy as np
import turtle
import json


#############################################
#
#   DIFFERENT WAYS TO GENERATE POPULATION
#
#############################################



def generate_population_randomly_grid():
    x_max = params['X_MAX']
    y_max = params['Y_MAX']
    empty_cells = [(x, y) for y in range(y_max) for x in range(x_max)]

    if x_max * y_max <= params["POP_SIZE"]:
        print("Not enough size on the grid for the chosen number of fireflies")

    population = []
    period_domain = [params['PERIOD_MIN'], params['PERIOD_MAX']]
    latency = params['LATENCY'] # we can change so latency will also between some min and max value
    period_threshold = 0.0
    coords = []
    for id in range(params['POP_SIZE']):

        x_coord, y_coord = empty_cells.pop(random.randint(0,len(empty_cells)-1))
        coords.append([x_coord, y_coord])
        lat = random.randint(0,latency)
        period = random.uniform(period_domain[0], period_domain[1])
        waiting_time = 1
        population.append(FireFly(id,x_coord, y_coord, period, period_threshold,waiting_time, linearFunct(0.01), expFunct(0.01,-1), lat))

    for ff in population:
        ff.setNeighbours(get_neighbours(ff, population))

    return population


def generate_population_two_groups_different_periods():
    population = []
    id = 0
    flag = False
    for x in range(3, 6):
        for y in range(5, 11):
            if flag:
                population.append(gen_firefly(id, x, y, [5, 10]))
                id += 1
            flag = not flag
        flag = not flag

    flag = False
    for x in range(10,13):
        for y in range(5, 11):
            if flag:
                population.append(gen_firefly(id, x, y, [20, 30]))
                id += 1
            flag = not flag
        flag = not flag

    for ff in population:
        ff.setNeighbours(get_neighbours(ff, population))

    return population


def generate_population_two_groups_with_bridge():
    population = []
    id = 0
    flag = False
    for x in range(2, 5):
        for y in range(5, 11):
            if flag:
                population.append(gen_firefly(id, x, y, [5, 10]))
                id += 1
            flag = not flag
        flag = not flag

    flag = False
    for x in range(10,13):
        for y in range(5, 11):
            if flag:
                population.append(gen_firefly(id, x, y, [20, 30]))
                id += 1
            flag = not flag
        flag = not flag

    population.append(gen_firefly(id, 5, 7, [5, 30]))
    id += 1
    population.append(gen_firefly(id, 7, 7, [5, 30]))
    id += 1
    population.append(gen_firefly(id, 9, 7, [5, 30]))
    # id += 1
    # population.append(gen_firefly(id, 6, 8, [5, 30]))
    # id += 1
    # population.append(gen_firefly(id, 8, 8, [5, 30]))
    for ff in population:
        ff.setNeighbours(get_neighbours(ff, population))

    return population


def generate_population_with_probability():
    population = []
    id = 0
    for x in range(0, params["X_MAX"]):
        for y in range(0, params["Y_MAX"]):
            if random.random() < 0.1:
                population.append(gen_firefly(id, x, y, [5, 30]))
                id += 1
    return population


def gen_firefly(id, x_coord, y_coord, period_domain):
    return FireFly(id, x_coord, y_coord, random.uniform(period_domain[0], period_domain[1]), period_threshold=0,
                   waiting_time=1, sub_time_fun=linearFunct(0.01), add_time_fun=expFunct(0.01, -1), start_delay=0)



def generate_population():
    
    if params['SCENARIO'].upper() == 'TWO_GROUPS_DIFF_PERIODS':
        return generate_population_two_groups_different_periods()
    elif params['SCENARIO'].upper() == 'TWO_GROUPS_WITH_BRIDGE':
        return generate_population_two_groups_with_bridge()
    elif params['SCENARIO'].upper() == 'RANDOM':
        return generate_population_randomly_grid()
    elif params['SCENARIO'].upper() == 'PROBABILITY':
        return generate_population_with_probability()

    else:
        raise Exception("Provided scenario not defined, change param 'SCENARIO'")


################################################
#
#   DIFFERENT FUNCTIONS FOR ADDING TO PERIOD WHEN FIREFLY
#   DIDN'T GET ANY SIGNAL FROM OTHER FIREFLIES
#
################################################

def expFunct(A=0.1, b=1):
    def fun(x):
        return A * math.exp(b*x)
    return fun

def linearFunct(m = 0.1, b = 0):
    def fun(x):
        return m * x + b
    return fun

def contFunction(A=0.05):
    def fun(x):
        return A
    return fun


################################################
#
#   OTHER AUXILIARY FUNCTIONS
#
################################################


def find_n_nearest_neighbours(fireflyes, X):
    neighbours = []
    X = np.array(X)
    tree = KDTree(X, leaf_size=2)
    for i in range(len(fireflyes)):
        _ , ind = tree.query([X[i]], k=params['N_NEIGHBOURS'] + 1)
        for j in ind[0]:
            if j != i:
                neighbours.append(fireflyes[j])
        fireflyes[i].setNeighbours(neighbours)

def get_neighbours(firefly, fireflies):
    neighbors = []
    for f in fireflies:
        if f.id != firefly.id:
            dx = abs(firefly.x_coord - f.x_coord)
            dy = abs(firefly.y_coord - f.y_coord)
            if dx <= params["NEIGHBOURS_DIST"] * math.sqrt(2) and dy <= params["NEIGHBOURS_DIST"] * math.sqrt(2):
                neighbors.append(f)
    return neighbors

def save_scenario(fireflies):
    f = []
    for firefly in fireflies:
        f.append([firefly.id, firefly.x_coord, firefly.y_coord, firefly.period, firefly.period_threshold, firefly.waiting_time, firefly.start_delay])
    open('scenario_prob.json','w').write(json.dumps(f))

def load_scenario():
    with open('scenario_prob.json') as f:
        pop = json.load(f)
    fireflies = []
    for id, x_coord, y_coord, period, period_threshold, waiting_time, start_delay in pop:
        fireflies.append(FireFly(id, x_coord, y_coord, period, period_threshold, waiting_time, sub_time_fun=linearFunct(0.01), add_time_fun=expFunct(0.01, -1), start_delay=start_delay))
    return fireflies