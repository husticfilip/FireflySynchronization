from fireFly import *
from display import *
import numpy as np
import matplotlib.cm as cm
import itertools
def iterate(fireflyes, time_step = 0.1, max_time = 10):
    display_population(fireflyes)
    timer = 0
    while timer <= max_time:
        for f in fireflyes:
            f.applyMove(time_step)

        timer += time_step
        changeStates(fireflyes)

        if timer >= 1000:
            printFireflyesStates(fireflyes, timer)
    plt.show()


def saveIterator(fireflyes, time_step = 0.1, max_time = 10):
    plot_blinking_after = max_time - params['PLOT_BLINKING_OF_LAST_PERIODS']
    #display_population(fireflyes)
    ff_periods = [[] for i in range(len(fireflyes))]
    ff_blinked = [[] for i in range(len(fireflyes))]

    timer = 0
    while abs(max_time - timer ) >= 0.0001:
        for f in fireflyes:
            f.applyMove(time_step)

        for i,ff in enumerate(fireflyes):
            ff_periods[i].append(ff.period)
            if timer >=plot_blinking_after:
                if ff.current_state.STAGE == Stage.BLINKED:
                    ff_blinked[i].append((timer,1))
                else:
                    ff_blinked[i].append((timer,0))
            
        timer += time_step
        changeStates(fireflyes)
        #if timer >= 9970:
        #     printFireflyesStates(fireflyes, timer)
    plotStuff(ff_periods, ff_blinked, time_step, timer)


def plotStuff(ff_periods, ff_blinked, time_step, max):
    plt.figure(1)
    plt.xlabel('Time step')
    plt.ylabel('Fireflyes periods')
    colors = iter(cm.rainbow(np.linspace(0, 1, len(ff_blinked))))
    x = [i for i in np.arange(time_step,max,time_step)]
    for i in range(len(ff_periods)):
        plt.scatter(x,ff_periods[i],s=1, color=next(colors))



    plt.figure(2)
    plt.xlabel('Time step')
    plt.ylabel('Fireflyes')
    plt.yticks(np.arange(1, len(ff_blinked) + 1, 1))
    plt.grid(axis='y', linestyle='-')
    plt.ylim(0, len(ff_periods) + 1)
    y = 0
    # rainbow
    colors = iter(cm.rainbow(np.linspace(0, 1, len(ff_blinked))))
    # iterate through red, green or blue
    # colors = itertools.cycle(["r", "b", "g"])

    for i in range(len(ff_blinked)):
        y += 1
        color = next(colors)
        for timer, b in ff_blinked[i]:
            if b:
                plt.scatter(timer,y, color = color)

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
            print("%.3f" % firefly.current_state.current_counter, end='     ')
        elif firefly.current_state.STAGE == Stage.BLINKED:
            print(" B ", end='       ')
            x_blink.append(firefly.x_coord)
            y_blink.append(firefly.y_coord)
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
    plt.pause(0.01)

    print("Periods:", end='   ')
    for firefly in fireflies:
        print("%.3f" % firefly.period, end='   ')

    print()