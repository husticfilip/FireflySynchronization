from fireFly import *
from display import *
import numpy as np
import matplotlib.cm as cm
import itertools

def saveIterator(fireflyes, time_step = 0.1, max_time = 10):
    plot_blinking_after = max_time - params['PLOT_BLINKING_OF_LAST_PERIODS']
    # display_population(fireflyes)
    ff_periods = [[] for i in range(len(fireflyes))]
    ff_blinked = [[] for i in range(len(fireflyes))]

    ff_last_blink = []
    num_of_different_groups = 0 # be carefull, group ids should start from 0,1,2..
    for ff in fireflyes:
        if ff.group_id + 1 > num_of_different_groups:
            num_of_different_groups = ff.group_id + 1
        ff_last_blink.append([ff.group_id, 0, False])
    groups_blinked_syncs = [[] for i in range(num_of_different_groups)]

    timer = 0
    iteration = 0
    while abs(max_time - timer ) >= 0.01:
        for f in fireflyes:
            f.applyMove(time_step)

        changeStates(fireflyes)
        # if timer >= (params['SIMULATION_TIME'] - 10 ):
        #     printFireflyesStates(fireflyes, timer)

        for i,ff in enumerate(fireflyes):
            ff_periods[i].append(ff.period)

            if ff.current_state.STAGE == Stage.BLINKED and ff_last_blink[i][2] == False:
                ff_last_blink[i][1] = iteration
                ff_last_blink[i][2] = True

            if timer >= plot_blinking_after:
                if ff.current_state.STAGE == Stage.BLINKED:
                    ff_blinked[i].append((timer, 1))
                else:
                    ff_blinked[i].append((timer, 0))

        check_sync_groups(ff_last_blink, num_of_different_groups, timer, iteration, groups_blinked_syncs, fireflyes)
        timer += time_step
        iteration += 1
    plotStuff(ff_periods, ff_blinked, time_step, timer)
    print_sync_periods(groups_blinked_syncs, num_of_different_groups)


def check_if_every_in_group_blinked(ff_last_blink, group_id):
    for info in ff_last_blink:
        if info[0] == group_id and info[2] == False:
            return False
    return True

def check_if_group_is_sync(ff_last_blink, group_id, iteration):
    flag = True
    for info in ff_last_blink:
        if info[0] == group_id:
            info[2] = False
            if iteration - info[1] >= 3:
                flag = False
    return flag

def check_sync_groups(ff_last_blink, num_of_different_groups, timer, iteration, groups_blinked_syncs, fireflyes):
    for group_id in range(num_of_different_groups):
        if check_if_every_in_group_blinked(ff_last_blink, group_id):
            if check_if_group_is_sync(ff_last_blink, group_id, iteration):
                groups_blinked_syncs[group_id].append((timer, True))
            else:
                groups_blinked_syncs[group_id].append((timer, False))


def print_sync_periods(groups_blinked_syncs, num_of_different_groups):
    for i, flash_times in enumerate(groups_blinked_syncs):
        print("Synchronizing streaks for group  ", i)
        max_flashing = 0
        longest = [0,0]
        j = 0
        
        while j < len(flash_times):
            #find beginning of sequence
            counter = 1
            while j < len(flash_times):
                if flash_times[j][1] == True:
                    beggining = flash_times[j][0]
                    break
                j += 1
            #find end of sequence
            while j < len(flash_times):
                counter += 1
                if flash_times[j][1] == False:
                    ending = flash_times[j - 1][0]
                    break
                else:
                    ending = params['SIMULATION_TIME']
                j += 1
            print("Flashing sequence  ", beggining,"-",ending, "    nr flashs: ", counter, "       diff: ", (ending-beggining))
            if (longest[1] - longest[0] ) < (ending - beggining):
                longest[1] = ending
                longest[0] = beggining
            max_flashing = max(max_flashing, counter)
        print()
        print("Longest sequence:  ", longest[0],"-", longest[1], "       diff: ", (longest[1]-longest[0]))
        print("nr of flashes: ", max_flashing)
        print()



def are_ff_sync(ff_stable):
    last_blinks = []
    for ff in ff_stable:
        last_blinks.append(ff[0])

    if (np.std(last_blinks)) >= 3.0:
        print((np.std(last_blinks)))
        input()


def is_sistem_stable(ffs_stable):
    for ff in ffs_stable:
        if ff[2] == False:
            return False
    return True


def is_ff_Stable(ff_stability, iteration):
    iterations_taken_to_blink = iteration - ff_stability[0]
    if iterations_taken_to_blink == ff_stability[1] or iterations_taken_to_blink == (ff_stability[1]-1) or iterations_taken_to_blink == (ff_stability[1]+1):
        ff_stability[2] = True
    else:
        ff_stability[2] = False

    ff_stability[0] = iteration #  iteration on which ff blinked
    ff_stability[1] = iterations_taken_to_blink # how many iterations it took ff to blink this time


def plotStuff(ff_periods, ff_blinked, time_step, max):
    plt.figure(1)
    plt.xlabel('Time step')
    plt.ylabel('Fireflies periods')
    colors = iter(cm.rainbow(np.linspace(0, 1, len(ff_blinked))))
    x = [i for i in np.arange(0,max,time_step)]
    for i in range(len(ff_periods)):
        plt.scatter(x,ff_periods[i],s=1, color=next(colors))

    plt.figure(2)
    plt.xlabel('Time step')
    plt.ylabel('Fireflies')
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
    plt.ylim(-0.5, params['Y_MAX'])
    plt.scatter(x_,y_,c="black")
    plt.scatter(x_blink,y_blink,c="red")
    plt.pause(0.01)

    # print("Periods:", end='   ')
    # for firefly in fireflies:
    #     print("%.3f" % firefly.period, end='   ')

    print()