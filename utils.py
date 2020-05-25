import random
import math
from parameters import params, experimentation
from sklearn.neighbors import KDTree
from fireFly import FireFly
import numpy as np
import turtle


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
    subtraction_time = params['SUBTRACTION_TIME'] # time we substract from counter if we get signal from other firefly
    period_threshold = 0.0
    coords = []
    for id in range(params['POP_SIZE']):
        # t = turtle.Turtle(shape="circle")
        # t.shapesize(0.5,0.5)
        t = None
        x_coord, y_coord = empty_cells.pop(random.randint(0,len(empty_cells)-1))

        # t.hideturtle()
        # t.up()
        # t.goto((x_coord, y_coord))
        # t.showturtle()
        coords.append([x_coord, y_coord])
        latency = 0 #random.randint(0,10)
        period = random.uniform(period_domain[0], period_domain[1])
        waiting_time = 1
        population.append(FireFly(id,x_coord, y_coord, period, period_threshold,waiting_time, linearFunct(0.01), expFunct(0.01,-1), latency, turtle=t))

    for ff in population:
        ff.setNeighbours(get_neighbours(ff, population))
        #find_n_nearest_neighbours(population, coords)

    return population


def generate_population_two_grops_different_periods():
    population = []
    id = 0

    for x in range(2, 5):
        for y in range(4, 7):
            population.append(gen_firefly(id, x, y, [5, 10]))
            id += 1

    for x in range(8,11):
        for y in range(4, 7):
            population.append(gen_firefly(id, x, y, [100, 200]))
            id += 1

    for ff in population:
        ff.setNeighbours(get_neighbours(ff, population))

    return population

def gen_firefly(id, x_coord, y_coord, period_domain):
    return FireFly(id, x_coord, y_coord, random.uniform(period_domain[0], period_domain[1]), period_threshold=0,
                   waiting_time=1, sub_time_fun=linearFunct(0.01), add_time_fun=expFunct(0.01, -1), start_delay=0)


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