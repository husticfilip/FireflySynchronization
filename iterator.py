from fireFly import *
from display import *


def saveIterator(fireflyes, time_step = 0.1, max_time = 10):
    plot_blinking_after = max_time - params['PLOT_BLINKING_OF_LAST_PERIODS']
    display_population(fireflyes)

    timer = 0
    while abs(max_time - timer ) >= 0.01:
        for f in fireflyes:
            f.applyMove(time_step)

        changeStates(fireflyes)
        if timer > plot_blinking_after:
            plotChanges(fireflyes, timer)
            #printFireflyesStates(fireflyes, timer)

        timer += time_step


def changeStates(fireflyes):
    for f in fireflyes:
        f.previous_state, f.current_state, f.next_state = f.current_state, f.next_state, f.previous_state


def plotChanges(fireflies, timer):
    x_blink = []
    y_blink = []
    x_ = []
    y_ = []
    for firefly in fireflies:
        if firefly.current_state.STAGE == Stage.BLINKED or firefly.current_state.STAGE == Stage.WAITING:
            x_blink.append(firefly.x_coord)
            y_blink.append(firefly.y_coord)
        else:
            x_.append(firefly.x_coord)
            y_.append(firefly.y_coord)
    plt.cla()

    plt.xlim(-0.5, params['X_MAX'])
    plt.ylim(-0.5, params['Y_MAX'])
    plt.scatter(x_, y_, c="black")
    plt.scatter(x_blink, y_blink, c="red")
    plt.pause(0.01)

def printFireflyesStates(fireflies, timer):
    print("%.3f" % timer, end='      ')
    for firefly in fireflies:
        if firefly.current_state.STAGE == Stage.WAITING_TO_START:
            print(" X ",end='   ')
        elif firefly.current_state.STAGE == Stage.COUNTING or firefly.current_state.STAGE == Stage.SWITCH_TO_COUNTING:
            print("%.3f" % firefly.current_state.current_counter, end='     ')
        elif firefly.current_state.STAGE == Stage.BLINKED:
            print(" B ", end='       ')
        else:
            print("%.2fT" % firefly.current_state.waiting_counter, end='     ')
    print()