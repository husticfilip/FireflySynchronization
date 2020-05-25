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

def update_plot(population):
    x_on = [i.x_coord for i in population if i.isBlinking]
    x_off = [i.x_coord for i in population if not i.isBlinking]
    y_on = [i.y_coord for i in population if i.isBlinking]
    y_off = [i.y_coord for i in population if not i.isBlinking]

    plt.scatter(x_off ,y_off, c="black")
    plt.scatter(x_on, y_on, c="red")

