import random
import math
from parameters import params, experimentation
from fireFly import FireFly


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

    for id in range(params['POP_SIZE']):
        x_coord = random.randint(0, x_max)
        y_coord = random.randint(0,y_max)
        period = random.uniform(period_domain[0], period_domain[1])
        population.append(FireFly(id,x_coord, y_coord, period, subtraction_time, expFunct(), latency))

    for firefily in population:
        firefily.setNeighbours(find_n_nearest_neighbours(firefily, population))

    return population


def generate_population_manualy():
    fireflyes = []

    fireflyes.append(FireFly(1, 0, 0, 2.5, 1, contFunction(0.2), contFunction(0.8), 0))
    fireflyes.append(FireFly(2, 1, 2, 4, 1, contFunction(0.2), contFunction(0.8), 1))
    fireflyes.append(FireFly(3, 4, 5, 5.5, 1, contFunction(0.2), contFunction(0.8), 0))
    fireflyes.append(FireFly(4, 9, 9, 7, 1, contFunction(0.2), contFunction(0.8), 3.5))
    #fireflyes.append(FireFly(5, 9, 9, 2.3, 0.5, contFunction(0.01), contFunction(0.1), 6))
    #fireflyes.append(FireFly(6, 9, 9, 14.5, 0.5, contFunction(0.01), contFunction(0.1), 2))
    #fireflyes.append(FireFly(7, 9, 9, 6.5, 0.5, contFunction(0.01), contFunction(0.1), 0))

    for i in range(len(fireflyes)):
        neigh = []
        for j in range(len(fireflyes)):
            if j != i:
                neigh.append(fireflyes[j])
        fireflyes[i].setNeighbours(neigh)



    # fireflyes[0].setNeighbours([fireflyes[1], fireflyes[2], fireflyes[3]])
    # fireflyes[1].setNeighbours([fireflyes[0], fireflyes[2], fireflyes[3]])
    # fireflyes[2].setNeighbours([fireflyes[3], fireflyes[0], fireflyes[1]])
    # fireflyes[3].setNeighbours([fireflyes[0], fireflyes[1], fireflyes[2]])

    return fireflyes


################################################
#
#   DIFFERENT FUNCTIONS FOR ADDING TO PERIOD WHEN FIREFLY
#   DIDN'T GET ANY SIGNAL FROM OTHER FIREFLIES
#
################################################

def expFunct(A=1, b=-0.2):
    def fun(x):
        return A * math.exp(b*x)
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

def find_n_nearest_neighbours(firefly, fireflyes):
    pass



