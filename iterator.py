from fireFlyStagesEnum import Stage
import fireFly

def iterate(fireflyes, time_step = 0.1, max_time = 10):
    timer = 0
    fireFly.EVEN_ITERATION = False # 1st iteration is odd
    while(timer <= max_time):
        for firefly in fireflyes:
            firefly.applyMove(time_step)

        timer += time_step
        fireFly.EVEN_ITERATION = False if fireFly.EVEN_ITERATION else True
        printFireflyesStates(fireflyes, timer)


def printFireflyesStates(fireflies, timer):
    print("%.3f" % timer, end='      ')

    for firefly in fireflies:
        if firefly.STAGE == Stage.WAITING_TO_START:
            print(" X ",end='   ')
        elif firefly.STAGE == Stage.COUNTING_DOWN:
            print("%.3f" % firefly.current_time_counting, end='     ')
        elif firefly.STAGE == Stage.BLINKED:
            print(" B ", end='       ')
        else:
            print("%.2fT" % firefly.current_time_waiting, end='     ')

    print()