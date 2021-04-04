import numpy as np
from functools import reduce
from copy import deepcopy
from operator import add
from indianajones import IndianaJones

# HYPER PARAMETERS

GAMMA = 0.999
DELTA = 1e-3

POSITION = ['W', 'N', 'E', 'S', 'C']
MATERIAL = [0, 1, 2]
ARROW = [0, 1, 2, 3]
STATE = ['D', 'R']
HEALTH = [0, 1, 2, 3, 4]

PATH = "lastiteration.txt"


def value_iteration():
    utilities = np.full((len(POSITION), len(MATERIAL),
                         len(ARROW), len(STATE), len(HEALTH)), 0.0)
    policies = np.full((len(POSITION), len(MATERIAL), len(
        ARROW), len(STATE), len(HEALTH)), "exit    ")

    index = 0
    done = False
    while not done:  # one iteration of value iteration
        print("iteration=%d" % (index))
        index += 1
        temp = np.zeros(utilities.shape)
        delta = np.NINF

        for state, util in np.ndenumerate(utilities):
            properState = IndianaJones(
                POSITION[state[0]], state[1], state[2], STATE[state[3]], state[4]*25)
            if(properState.state_mmhealth == 0):
                print("(%c,%d,%d,%c,%d):%s=[%f]" % (POSITION[state[0]], state[1],
                                                    state[2], STATE[state[3]], state[4] * 25, "NONE", 0.0))
                continue
            actions = properState.getNextStates()
            new_util = np.NINF
            for action in actions:
                finalUtility = 0.0
                for state_inner in action["states"]:
                    utilityIndex = (POSITION.index(state_inner["next_pos"]), state_inner["next_mat"], state_inner["next_arrow"], STATE.index(
                        state_inner["next_mmstate"]), state_inner["next_mmhealth"]//25)
                    finalUtility += state_inner["probability"]*(
                        state_inner["reward"] + (GAMMA * utilities[utilityIndex]))
                new_util = max(float(finalUtility), float(new_util))
                if(new_util == finalUtility):
                    policies[state[0], state[1], state[2],
                             state[3], state[4]] = action["action"]
            temp[state] = new_util
            print("(%c,%d,%d,%c,%d):%s=[%f]" % (POSITION[state[0]], state[1],
                                                state[2], STATE[state[3]], state[4] * 25, policies[state], new_util))
            delta = max(delta, np.abs(util - new_util))
        utilities = temp
        if delta < DELTA:
            done = True
        # if index == 10:
        #     break
    return policies, utilities


if __name__ == "__main__":
    policies, utilities = value_iteration()
    f = open(PATH, "w+")
    for pos in range(5):
        for mat in range(3):
            for arrow in range(4):
                for mmstate in range(2):
                    for mmhealth in range(5):
                        f.write("%c %d %d %c %d\n" % (POSITION[pos], mat, arrow,
                                                      STATE[mmstate], mmhealth))
                        f.write(policies[pos, mat, arrow, mmstate, mmhealth])
                        f.write("\n")
                        # print(POSITION[pos], mat, arrow,
                        #       STATE[mmstate], mmhealth)
                        # print(policies[pos, mat, arrow, mmstate, mmhealth])
