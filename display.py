import matplotlib.pyplot as plt
from parameters import params


def display_population(population):
    x = [i.x_coord for i in population]
    y = [i.y_coord for i in population]

    plt.figure(0)
    plt.xlim(-0.5, params['X_MAX'] + 1)
    plt.ylim(-0.5, params['Y_MAX'] + 1)
    plt.scatter(x ,y, c="black")

def update_plot(firefly):
    plt.scatter(firefly.x_coord ,firefly.y_coord, c="red")
    plt.pause(params['BLINKING_TIME'])
    plt.scatter(firefly.x_coord ,firefly.y_coord, c="black")
    plt.pause(0.1)