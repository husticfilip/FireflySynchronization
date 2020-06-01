import random
import math
from parameters import params
from fireFly import FireFly



#############################################
#
#   DIFFERENT WAYS TO GENERATE POPULATION
#
#############################################

def generate_population_randomly_grid():
    """
    Function generates random generation with values of parameters
    set in parameter.py/params
    """
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
        population.append(FireFly(id,x_coord, y_coord, period, period_threshold,waiting_time, linearFunct(0.01), expFunct(0.01, -1), lat))

    for ff in population:
        ff.setNeighbours(get_neighbours(ff, population))

    return population

def generate_population_two_groups_different_periods():
    """
    This function generates two groups each one differing in the
    domain of the periods.
    """
    population = []
    id = 0
    flag = False
    for x in range(3, 6):
        for y in range(5, 11):
            if flag:
                population.append(gen_firefly(id, x, y, [5, 10], 0))
                id += 1
            flag = not flag
        flag = not flag

    flag = False
    for x in range(10,13):
        for y in range(5, 11):
            if flag:
                population.append(gen_firefly(id, x, y, [100, 105], 1))
                id += 1
            flag = not flag
        flag = not flag

    for ff in population:
        ff.setNeighbours(get_neighbours(ff, population))

    return population

def generate_population_two_groups_with_bridge():
    """
    Function generates two groups with bridge fireflies between them
    """
    population = []
    id = 0
    flag = False
    for x in range(2, 5):
        for y in range(5, 11):
            if flag:
                population.append(gen_firefly(id, x, y, [5, 10], 0))
                id += 1
            flag = not flag
        flag = not flag

    flag = False
    for x in range(10,13):
        for y in range(5, 11):
            if flag:
                population.append(gen_firefly(id, x, y, [25, 30], 0))
                id += 1
            flag = not flag
        flag = not flag
    population.append(gen_firefly(id, 5, 7, [5, 30], 0))
    id += 1
    population.append(gen_firefly(id, 7, 7, [5, 30], 0))
    id += 1
    population.append(gen_firefly(id, 9, 7, [5, 30], 0))
    id += 1
    population.append(gen_firefly(id, 6, 8, [5, 30], 0))
    id += 1
    population.append(gen_firefly(id, 8, 8, [5, 30], 0))

    for ff in population:
        ff.setNeighbours(get_neighbours(ff, population))

    return population

def generate_population_four_groups_different_periods():
    """
      Function generates four groups of fireflies each
      with different domain of periods
    """
    population = []
    id = 0
    flag = True

    for x in range(3, 6):
        for y in range(3, 6):
            if flag:
                population.append(gen_firefly(id, x, y, [5, 10], 0))
                id += 1
            flag = not flag

    flag = True
    for x in range(3, 6):
        for y in range(9, 12):
            if flag:
                population.append(gen_firefly(id, x, y, [100, 105], 1))
                id += 1
            flag = not flag

    flag = True
    for x in range(9, 12):
        for y in range(9, 12):
            if flag:
                population.append(gen_firefly(id, x, y, [200, 205], 2))
                id += 1
            flag = not flag

    flag = True
    for x in range(9, 12):
        for y in range(3, 6):
            if flag:
                population.append(gen_firefly(id, x, y, [300, 305], 3))
                id += 1
            flag = not flag


    for ff in population:
        ff.setNeighbours(get_neighbours(ff, population))

    return population

def generate_population_four_groups_with_bridge():
    """
      Function generates four groups of fireflies each
      with different domain of periods and one bridge
      group between them.
    """
    population = []
    id = 0
    flag = True

    for x in range(3, 6):
        for y in range(3, 6):
            if flag:
                population.append(gen_firefly(id, x, y, [5, 10], 0))
                id += 1
            flag = not flag

    flag = True
    for x in range(3, 6):
        for y in range(9, 12):
            if flag:
                population.append(gen_firefly(id, x, y, [100, 105], 0))
                id += 1
            flag = not flag

    flag = True
    for x in range(9, 12):
        for y in range(9, 12):
            if flag:
                population.append(gen_firefly(id, x, y, [200, 205], 0))
                id += 1
            flag = not flag

    flag = True
    for x in range(9, 12):
        for y in range(3, 6):
            if flag:
                population.append(gen_firefly(id, x, y, [300, 305], 0))
                id += 1
            flag = not flag

    # Bridge, in the middle of groups
    flag = True
    for x in range(6, 9):
        for y in range(6, 9):
            if flag:
                population.append(gen_firefly(id, x, y, [5, 305], 0))
                id += 1
            flag = not flag

    for ff in population:
        ff.setNeighbours(get_neighbours(ff, population))

    return population

def generate_population_with_probability():
    """
      Function generates firefly on one cell of th grid
      with given probability.
    """
    population = []
    id = 0
    for x in range(0, params["X_MAX"]):
        for y in range(0, params["Y_MAX"]):
            if random.random() < 0.5:
                population.append(gen_firefly(id, x, y, [5, 30], 0))
                id += 1
    return population


def gen_firefly(id, x_coord, y_coord, period_domain, group_id):
    return FireFly(id, x_coord, y_coord, random.uniform(period_domain[0], period_domain[1]), period_threshold=0,
                   waiting_time=0.2, sub_time_fun=linearFunct(0.01), add_time_fun=expFunct(0.01, -1), start_delay=0, group_id = group_id)


def generate_population():
    
    if params['SCENARIO'].upper() == 'TWO_GROUPS_DIFF_PERIODS':
        return generate_population_two_groups_different_periods()
    elif params['SCENARIO'].upper() == 'TWO_GROUPS_WITH_BRIDGE':
        return generate_population_two_groups_with_bridge()
    elif params['SCENARIO'].upper() == 'RANDOM':
        return generate_population_randomly_grid()
    elif params['SCENARIO'].upper() == 'PROBABILITY':
        return generate_population_with_probability()
    elif params['SCENARIO'].upper() == 'FOUR_GROUPS_DIFF_PERIODS':
        return generate_population_four_groups_different_periods()
    elif params['SCENARIO'].upper() == 'FOUR_GROUPS_WITH_BRIDGE':
        return generate_population_four_groups_with_bridge()
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


def get_neighbours(firefly, fireflies):
    """
      Function returns all neighbouring fireflies in the provided
      Moore distance from provided firefly.
    """
    neighbors = []
    for f in fireflies:
        if f.id != firefly.id and f.group_id == firefly.group_id:
            dx = abs(firefly.x_coord - f.x_coord)
            dy = abs(firefly.y_coord - f.y_coord)
            if dx <= params["MOORE_DIST"] and dy <= params["MOORE_DIST"]:
                neighbors.append(f)
    return neighbors