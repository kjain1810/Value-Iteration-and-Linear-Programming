import numpy as np
from functools import reduce
from copy import deepcopy
from operator import add

# HYPER PARAMETERS

TASK = 0
GAMMA = 0.999
if TASK == 3:
    GAMMA = 0.25
DELTA = 1e-3

POSITION = ['W', 'N', 'E', 'S', 'C']
MATERIAL = [0, 1, 2]
ARROW = [0, 1, 2, 3]
STATE = ['D', 'R']
HEALTH = [0, 1, 2, 3, 4]

MAIN_PATH = "./output/part_2_trace.txt"
if TASK == 1:
    MAIN_PATH = "./output/part_2_task_2.1_trace.txt"
if TASK == 2:
    MAIN_PATH = "./output/part_2_task_2.2_trace.txt"
if TASK == 3:
    MAIN_PATH = "./output/part_2_task_2.3_trace.txt"

LAST_ITER_PATH = "lastiteration.txt"

printer = open(MAIN_PATH, "w+")

STEP_COST = -20
FIN_REWARD = 50
HIT_COST = -40


class IndianaJones:
    def __init__(self):
        self.state_pos = "C"  # possible: N, E, S, W, C
        self.state_mat = 2  # possible: 0, 1, 2
        self.state_arrow = 0  # possible: 0, 1, 2, 3
        self.state_mmstate = "R"  # possible: D, R
        self.state_mmhealth = 100  # possible: 0, 25, 50, 75, 100

    def __init__(self, pos, mat, arrow, mmstate, mmhealth, task):
        if mmhealth != 0 and mmhealth != 25 and mmhealth != 50 and mmhealth != 75 and mmhealth != 100:
            print("WRONG MMHEALTH")
        self.state_pos = pos  # possible: N, E, S, W, C
        self.state_mat = mat  # possible: 0, 1, 2
        self.state_arrow = arrow  # possible: 0, 1, 2, 3
        self.state_mmstate = mmstate  # possible: D, R
        self.state_mmhealth = mmhealth  # possible: 0, 25, 50, 75, 100
        self.task = task

    def actions(self):
        ij_actions = []
        ij_actions.append("STAY")
        if self.state_pos == "W":
            ij_actions.append("RIGHT")
            if self.state_arrow > 0:
                ij_actions.append("SHOOT")
        elif self.state_pos == "E":
            ij_actions.append("LEFT")
            if self.state_arrow > 0:
                ij_actions.append("SHOOT")
            ij_actions.append("HIT")
        elif self.state_pos == "N":
            ij_actions.append("DOWN")
            if self.state_mat > 0:
                ij_actions.append("CRAFT")
        elif self.state_pos == "S":
            ij_actions.append("UP")
            ij_actions.append("GATHER")
        elif self.state_pos == "C":
            ij_actions.append("RIGHT")
            ij_actions.append("LEFT")
            ij_actions.append("DOWN")
            ij_actions.append("UP")
            if self.state_arrow > 0:
                ij_actions.append("SHOOT")
            ij_actions.append("HIT")
        # else:
        #     print("Invalid state: " + self.state_pos)
        #     exit(0)
        mm_actions = []
        if self.state_mmstate == "D":
            mm_actions.append("STAY")
            mm_actions.append("ready")
        elif self.state_mmstate == "R":
            mm_actions.append("HIT")
            mm_actions.append("STAY")
        # else:
        #     print("Invalid state: " + self.state_pos)
        #     exit(0)
        return ij_actions, mm_actions

    def moveState(self, x):
        if x == "STAY":
            return self.state_pos
        pos = self.state_pos
        if (x == "LEFT" and pos == "E") and self.task == 1:
            return "W"
        if (x == "LEFT" and pos == "E") or (x == "RIGHT" and pos == "W") or (x == "UP" and pos == "S") or (x == "DOWN" and pos == "N"):
            return "C"
        if x == "LEFT":
            return "W"
        if x == "RIGHT":
            return "E"
        if x == "UP":
            return "N"
        if x == "DOWN":
            return "S"
        print("INVALID MOVE: " + x + " from state " + pos)
        exit(0)

    def getState(self):
        return {"next_pos": None,
                "next_mat": None,
                "next_arrow": None,
                "next_mmstate": None,
                "next_mmhealth": None,
                "reward": None,
                "probability": None
                }

    def getObj(self):
        return {
            "action": None,
            "states": []
        }

    def getNextStates(self):
        if self.state_mmhealth == 0:
            return [{"action": "NONE", "states": []}]

        ij, mm = self.actions()

        states = []
        for i in ij:
            ns = self.getObj()
            ns["action"] = i
            if i == "LEFT" or i == "RIGHT" or i == "UP" or i == "DOWN" or i == "STAY":
                succ = self.getState()
                succ["next_pos"] = self.moveState(i)
                succ["next_mat"] = self.state_mat
                succ["next_arrow"] = self.state_arrow
                succ["next_mmhealth"] = self.state_mmhealth
                if self.task == 2 and i == "STAY":
                    succ["reward"] = 0
                else:
                    succ["reward"] = STEP_COST
                if self.state_pos == "E" or self.state_pos == "W":
                    succ["probability"] = 1.0
                else:
                    succ["probability"] = 0.85
                    fail = self.getState()
                    fail["next_pos"] = "E"
                    fail["next_mat"] = self.state_mat
                    fail["next_arrow"] = self.state_arrow
                    fail["next_mmhealth"] = self.state_mmhealth
                    fail["probability"] = 0.15
                    if self.task == 2 and i == "STAY":
                        fail["reward"] = 0
                    else:
                        fail["reward"] = STEP_COST
                    ns["states"].append(fail)
                ns["states"].append(succ)
            elif i == "SHOOT":
                succ = self.getState()
                succ["next_pos"] = self.state_pos
                succ["next_mat"] = self.state_mat
                succ["next_arrow"] = self.state_arrow - 1
                succ["next_mmhealth"] = max(0, self.state_mmhealth - 25)
                if succ["next_mmhealth"] == 0:
                    succ["reward"] = STEP_COST + FIN_REWARD
                else:
                    succ["reward"] = STEP_COST
                fail = self.getState()
                fail["next_pos"] = self.state_pos
                fail["next_mat"] = self.state_mat
                fail["next_arrow"] = self.state_arrow - 1
                fail["next_mmhealth"] = self.state_mmhealth
                fail["reward"] = STEP_COST
                if self.state_pos == "C":
                    succ["probability"] = 0.5
                    fail["probability"] = 0.5
                elif self.state_pos == "E":
                    succ["probability"] = 0.9
                    fail["probability"] = 0.1
                else:
                    succ["probability"] = 0.25
                    fail["probability"] = 0.75
                ns["states"].append(succ)
                ns["states"].append(fail)
            elif i == "HIT":
                succ = self.getState()
                succ["next_pos"] = self.state_pos
                succ["next_mat"] = self.state_mat
                succ["next_arrow"] = self.state_arrow
                succ["next_mmhealth"] = max(0, self.state_mmhealth - 50)
                if succ["next_mmhealth"] == 0:
                    succ["reward"] = STEP_COST + FIN_REWARD
                else:
                    succ["reward"] = STEP_COST
                fail = self.getState()
                fail["next_pos"] = self.state_pos
                fail["next_mat"] = self.state_mat
                fail["next_arrow"] = self.state_arrow
                fail["next_mmhealth"] = self.state_mmhealth
                fail["reward"] = STEP_COST
                if self.state_pos == "E":
                    succ["probability"] = 0.2
                    fail["probability"] = 0.8
                else:
                    succ["probability"] = 0.1
                    fail["probability"] = 0.9
                ns["states"].append(succ)
                ns["states"].append(fail)
            elif i == "GATHER":
                succ = self.getState()
                succ["next_pos"] = self.state_pos
                succ["next_mat"] = min(2, self.state_mat + 1)
                succ["next_arrow"] = self.state_arrow
                succ["next_mmhealth"] = self.state_mmhealth
                succ["probability"] = 0.75
                succ["reward"] = STEP_COST
                fail = self.getState()
                fail["next_pos"] = self.state_pos
                fail["next_mat"] = self.state_mat
                fail["next_arrow"] = self.state_arrow
                fail["next_mmhealth"] = self.state_mmhealth
                fail["probability"] = 0.25
                fail["reward"] = STEP_COST
                ns["states"].append(succ)
                ns["states"].append(fail)
            elif i == "CRAFT":
                succ1 = self.getState()
                succ2 = self.getState()
                succ3 = self.getState()
                succ1["next_pos"] = self.state_pos
                succ2["next_pos"] = self.state_pos
                succ3["next_pos"] = self.state_pos
                succ1["next_mat"] = self.state_mat - 1
                succ2["next_mat"] = self.state_mat - 1
                succ3["next_mat"] = self.state_mat - 1
                succ1["next_mmhealth"] = self.state_mmhealth
                succ2["next_mmhealth"] = self.state_mmhealth
                succ3["next_mmhealth"] = self.state_mmhealth
                succ1["next_arrow"] = min(3, self.state_arrow + 1)
                succ2["next_arrow"] = min(3, self.state_arrow + 2)
                succ3["next_arrow"] = min(3, self.state_arrow + 3)
                succ1["probability"] = 0.5
                succ2["probability"] = 0.35
                succ3["probability"] = 0.15
                succ1["reward"] = STEP_COST
                succ2["reward"] = STEP_COST
                succ3["reward"] = STEP_COST
                ns["states"].append(succ1)
                ns["states"].append(succ2)
                ns["states"].append(succ3)
            states.append(ns)
        for m in mm:
            if m == "STAY":
                if self.state_mmstate == "D":
                    for state in states:
                        for ns in state["states"]:
                            ns["next_mmstate"] = "D"
                            ns["probability"] *= 0.8
                else:
                    for state in states:
                        for ns in state["states"]:
                            ns["next_mmstate"] = "R"
                            ns["probability"] *= 0.5
        for m in mm:
            if m == "STAY":
                continue
            elif m == "ready":
                for action in states:
                    new_states = []
                    for ns in action["states"]:
                        x = ns.copy()
                        x["next_mmstate"] = "R"
                        x["probability"] *= 0.2 / 0.8
                        new_states.append(x)
                    for x in new_states:
                        action["states"].append(x)
            else:
                if self.state_pos != "E" and self.state_pos != "C":
                    for action in states:
                        new_states = []
                        for ns in action["states"]:
                            x = ns.copy()
                            x["next_mmstate"] = "D"
                            x["probability"] *= 0.5 / 0.5
                            new_states.append(x)
                        for x in new_states:
                            action["states"].append(x)
                else:
                    new_states = []
                    for action in states:
                        new_states = []
                        for ns in action["states"]:
                            x = ns.copy()
                            x["next_pos"] = self.state_pos
                            x["next_mat"] = self.state_mat
                            x["next_arrow"] = 0
                            x["next_mmstate"] = "D"
                            x["next_mmhealth"] = min(
                                100, self.state_mmhealth + 25)
                            x["probability"] *= 0.5 / 0.5
                            x["reward"] = STEP_COST + HIT_COST
                            new_states.append(x)
                        for x in new_states:
                            action["states"].append(x)
        return states


def value_iteration():
    utilities = np.full((len(POSITION), len(MATERIAL),
                         len(ARROW), len(STATE), len(HEALTH)), 0.0)
    policies = np.full((len(POSITION), len(MATERIAL), len(
        ARROW), len(STATE), len(HEALTH)), "exit    ")

    index = 0
    done = False
    while not done:  # one iteration of value iteration
        printer.write("iteration=%d\n" % (index))
        index += 1
        temp = np.zeros(utilities.shape)
        delta = np.NINF

        for state, util in np.ndenumerate(utilities):
            properState = IndianaJones(
                POSITION[state[0]], state[1], state[2], STATE[state[3]], state[4]*25, TASK)
            if(properState.state_mmhealth == 0):
                printer.write("(%c,%d,%d,%c,%d):%s=[0.000]\n" % (POSITION[state[0]], state[1],
                                                              state[2], STATE[state[3]], state[4] * 25, "NONE"))
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
            printer.write("(%c,%d,%d,%c,%d):%s=[%.3f]\n" % (POSITION[state[0]], state[1],
                                                          state[2], STATE[state[3]], state[4] * 25, policies[state], round(new_util, 3)))
            delta = max(delta, np.abs(util - new_util))
        utilities = temp
        if delta < DELTA:
            done = True
        # if index == 10:
        #     break
    return policies, utilities


if __name__ == "__main__":
    policies, utilities = value_iteration()
    # f = open(LAST_ITER_PATH, "w+")
    # for pos in range(5):
    #     for mat in range(3):
    #         for arrow in range(4):
    #             for mmstate in range(2):
    #                 for mmhealth in range(5):
    #                     f.write("%c %d %d %c %d\n" % (POSITION[pos], mat, arrow,
    #                                                   STATE[mmstate], mmhealth))
    #                     f.write(policies[pos, mat, arrow, mmstate, mmhealth])
    #                     f.write("\n")
