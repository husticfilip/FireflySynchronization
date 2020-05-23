import random
import math
from parameters import params, experimentation
from sklearn.neighbors import KDTree
from fireFly import FireFly
import numpy as np


#############################################
#
#   DIFFERENT WAYS TO GENERATE POPULATION
#
#############################################
def generate_population_randomly():
    population = []
    x_max = params['X_MAX']
    y_max = params['Y_MAX']
    period_domain = [params['PERIOD_MIN'], params['PERIOD_MAX']]
    latency = params['LATENCY'] # we can change so latency will also between some min and max value
    subtraction_time = params['SUBTRACTION_TIME'] # time we substract from counter if we get signal from other firefly
    period_threshold = 0.0
    coords = []
    for id in range(params['POP_SIZE']):
        x_coord = random.randint(0, x_max)
        y_coord = random.randint(0,y_max)
        coords.append([x_coord, y_coord])
        latency = random.randint(0,latency)
        period = random.uniform(period_domain[0], period_domain[1])
        waiting_time = 1
        population.append(FireFly(id,x_coord, y_coord, period, period_threshold,waiting_time, linearFunct(0.1), expFunct(0.1,-1), latency))

    find_n_nearest_neighbours(population, coords)

    return population


def generate_population_manualy():
    fireflyes = []

    fireflyes.append(FireFly(1, 0, 0, 4, 1.5, 0.5, linearFunct(0.05), expFunct(0.1,-1), start_delay = 5))
    fireflyes.append(FireFly(2, 1, 2, 3, 1.5, 0.5, linearFunct(0.05), expFunct(0.1,-1), start_delay = 1))
    fireflyes.append(FireFly(3, 4, 5, 2.5, 1.5, 0.5, linearFunct(0.05), expFunct(0.1,-1), start_delay = 3))
    fireflyes.append(FireFly(4, 9, 9, 7, 1.5, 0.5, linearFunct(0.05), expFunct(5,-1), start_delay = 7))

    fireflyes[0].setNeighbours([fireflyes[1], fireflyes[2], fireflyes[3]])
    fireflyes[1].setNeighbours([fireflyes[0], fireflyes[2], fireflyes[3]])
    fireflyes[2].setNeighbours([fireflyes[3], fireflyes[0], fireflyes[1]])
    fireflyes[3].setNeighbours([fireflyes[0], fireflyes[1], fireflyes[2]])

    return fireflyes


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


