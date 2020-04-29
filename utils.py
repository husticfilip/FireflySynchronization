import random
import math
from parameters import params, experimentation
from fireFly import FireFly
from sklearn.neighbors import KDTree
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
    coords = []
    for id in range(params['POP_SIZE']):
        x_coord = random.uniform(0, x_max)
        y_coord = random.uniform(0,y_max)
        coords.append([x_coord, y_coord])
        period = random.uniform(period_domain[0], period_domain[1])
        population.append(FireFly(id,x_coord, y_coord, period, subtraction_time, expFunct(), latency))

    find_n_nearest_neighbours(population, coords)

    return population


def generate_population_manualy():
    fireflyes = []

    fireflyes.append(FireFly(1, 0, 0, 4, 2, expFunct(), 1))
    fireflyes.append(FireFly(2, 1, 2, 3.5, 2,expFunct(), 1))
    fireflyes.append(FireFly(3, 4, 5, 5.5, 2, expFunct(), 1))
    fireflyes.append(FireFly(4, 9, 9, 6.5, 2, expFunct(), 1))

    # fireflyes[0].setNeighbours([fireflyes[1]])
    # fireflyes[1].setNeighbours([fireflyes[2]])
    # fireflyes[2].setNeighbours([fireflyes[3]])
    # fireflyes[3].setNeighbours([fireflyes[0]])
    X = [[0,0],[1,2],[4,5],[9,9]]
    find_n_nearest_neighbours(fireflyes, X)

    return fireflyes


################################################
#
#   DIFFERENT FUNCTIONS FOR ADDING TO PERIOD WHEN FIREFLY
#   DIDN'T GET ANY SIGNAL FROM OTHER FIREFLIES
#
################################################

def expFunct(A=4, b=-0.2):
    def fun(x):
        return A * math.exp(b*x)
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



