import matplotlib.pyplot as plt
from parameters import params


def display_population(population):
    x = [i.x_coord for i in population]
    y = [i.y_coord for i in population]

    plt.figure(0)
    plt.xlim(-0.5, params['X_MAX'])
    plt.ylim(-0.5, params['Y_MAX'])
    plt.scatter(x ,y, c="black")
    plt.pause(0.01)
