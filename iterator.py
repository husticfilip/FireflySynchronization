from fireFly import *
from display import *

def iterate(fireflyes, time_step = 0.1, max_time = 10):
    display_population(fireflyes)
    timer = 0
    while timer <= max_time:
        for f in fireflyes:
            f.applyMove(time_step)

        timer += time_step
        changeStates(fireflyes)

        if timer >= 500:
            printFireflyesStates(fireflyes, timer)
    plt.show()

def changeStates(fireflyes):
    for f in fireflyes:
        f.previous_state, f.current_state, f.next_state = f.current_state, f.next_state, f.previous_state


def printFireflyesStates(fireflies, timer):
    print("%.3f" % timer, end='      ')
    x_blink = []
    y_blink = []
    x_ = []
    y_ = []
    for firefly in fireflies:
        if firefly.current_state.STAGE == Stage.WAITING_TO_START:
            x_.append(firefly.x_coord)
            y_.append(firefly.y_coord)
            print(" X ",end='   ')
        elif firefly.current_state.STAGE == Stage.COUNTING or firefly.current_state.STAGE == Stage.SWITCH_TO_COUNTING:
            x_.append(firefly.x_coord)
            y_.append(firefly.y_coord)
            # firefly.turtle.fillcolor("black")
            print("%.3f" % firefly.current_state.current_counter, end='     ')
        elif firefly.current_state.STAGE == Stage.BLINKED:
            print(" B ", end='       ')
            x_blink.append(firefly.x_coord)
            y_blink.append(firefly.y_coord)
            # firefly.turtle.fillcolor("yellow")
            # FIXME if I remove the color on the waiting time, it blinks too fast
        else:
            x_blink.append(firefly.x_coord)
            y_blink.append(firefly.y_coord)
            print("%.2fT" % firefly.current_state.waiting_counter, end='     ')
    plt.cla()
    plt.xlim(-0.5, params['X_MAX'])
    plt.ylim(0.5, params['Y_MAX'])
    plt.scatter(x_,y_,c="black")
    plt.scatter(x_blink,y_blink,c="red")
    plt.pause(0.1)

    print("Periods:", end='   ')
    for firefly in fireflies:
        print("%.3f" % firefly.period, end='   ')

    print()