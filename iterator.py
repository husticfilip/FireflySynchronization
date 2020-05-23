from fireFly import *
from display import *

def iterate(fireflyes, time_step = 0.1, max_time = 10):
    timer = 0
    while timer <= max_time:
        if( abs(timer - 94.2) <= 0.01):
            a = 1

        for f in fireflyes:
            f.applyMove(time_step)

        timer += time_step
        changeStates(fireflyes)
        printFireflyesStates(fireflyes, timer)

def changeStates(fireflyes):
    for f in fireflyes:
        f.previous_state, f.current_state, f.next_state = f.current_state, f.next_state, f.previous_state


def printFireflyesStates(fireflies, timer):
    print("%.3f" % timer, end='      ')

    for firefly in fireflies:
        if firefly.current_state.STAGE == Stage.WAITING_TO_START:
            print(" X ",end='   ')
        elif firefly.current_state.STAGE == Stage.COUNTING or firefly.current_state.STAGE == Stage.SWITCH_TO_COUNTING:
            firefly.turtle.fillcolor("black")
            print("%.3f" % firefly.current_state.current_counter, end='     ')
        elif firefly.current_state.STAGE == Stage.BLINKED:
            print(" B ", end='       ')
            firefly.turtle.fillcolor("yellow")
            # FIXME if I remove the color on the waiting time, it blinks too fast
        else:
            print("%.2fT" % firefly.current_state.waiting_counter, end='     ')

    print(      "Periods:", end= '   ')
    for firefly in fireflies:
        print("%.3f" % firefly.period, end='   ')

    print()