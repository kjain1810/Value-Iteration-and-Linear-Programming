import cvxpy as cp
import json
import numpy as np
from itertools import chain

from indianajones import IndianaJones

POSITION = ['W', 'N', 'E', 'S', 'C']
MATERIAL = [0, 1, 2]
ARROW = [0, 1, 2, 3]
STATE = ['D', 'R']
HEALTH = [0, 1, 2, 3, 4]

ENUM = {}

STEP_COST = -20
FIN_REWARD = 0
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
        mm_actions = []
        if self.state_mmstate == "D":
            mm_actions.append("STAY")
            mm_actions.append("ready")
        elif self.state_mmstate == "R":
            mm_actions.append("HIT")
            mm_actions.append("STAY")
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



def enumerate_states():
    total_states = 0
    for pos in POSITION:
        for mat in MATERIAL:
            for arrow in ARROW:
                for state in STATE:
                    for health in HEALTH:
                        here = [pos, str(mat), str(arrow), state, str(health)]
                        ENUM[''.join(here)] = total_states
                        total_states += 1
    return total_states


def genAandR(total_states):
    possible_states = np.zeros(600)
    A = []
    R = []
    possible_states = np.zeros(total_states)
    possible_actions = []
    for i in ENUM:
        pos = i[0]
        mat = ord(i[1]) - ord('0')
        arrow = ord(i[2]) - ord('0')
        state = i[3]
        health = ord(i[4]) - ord('0')
        health_25 = health * 25
        ij = IndianaJones(pos, mat, arrow, state, health_25, 0)
        index_here = ENUM[i]
        actions = ij.getNextStates()

        is_exit_state = 0
        for action in actions:
            vec_here = np.zeros(total_states)
            if len(action["states"]) == 0:
                is_exit_state = 1
            else:
                av_reward = 0
                tpt = 0
                for ns in action["states"]:
                    enum = ''.join(
                        [ns["next_pos"], str(ns["next_mat"]), str(ns["next_arrow"]), ns["next_mmstate"], str(ns["next_mmhealth"]//25)])
                    tpt += ns["probability"]
                    av_reward += ns["reward"] * ns["probability"]
                    if enum == i:
                        continue
                    index = ENUM[enum]
                    vec_here[index] -= ns["probability"]
                    vec_here[index_here] += ns["probability"]
                possible_states[index_here] += 1
                av_reward /= tpt
                A.append(vec_here.tolist())
                R.append(av_reward)
                possible_actions.append(action["action"])
        if is_exit_state == 1:
            vec_here = np.zeros(total_states)
            vec_here[index_here] = 1
            A.append(vec_here.tolist())
            R.append(0)
            possible_states[index_here] += 1
            possible_actions.append("EXIT")
    return A, R, possible_states, possible_actions


def getpolicy(X, possible_states, possible_actions):
    idx = 0
    j = 0
    policy = []

    for i in ENUM:
        if possible_states[ENUM[i]] > 0:
            index = np.argmax(X[int(idx): idx + int(possible_states[ENUM[i]])])
            policy.append(
                [[i[0], (ord(i[1]) - ord('0')), ord(i[2]) - ord('0'), i[3], 25 * (ord(i[4]) - ord('0'))], possible_actions[idx + index]])
            idx += int(possible_states[ENUM[i]])

    return policy


if __name__ == "__main__":
    total_states = enumerate_states()
    A, R, possible_states, possible_actions = genAandR(total_states)

    

    idx = 0

    size = len(A)

    A = np.array(A)
    A = A.transpose()
    R = np.array(R)
    R = R[:, np.newaxis]
    R = R.transpose()
    alpha = np.zeros(total_states)
    alpha[ENUM["C23R4"]] = 1

    alpha = alpha.transpose()
    alpha = np.array(alpha)
    alpha = alpha[:, np.newaxis]

    X = cp.Variable(shape=(size, 1), name="X")
    constraints = [cp.matmul(A, X) == alpha, X >= 0]
    objective = cp.Maximize(cp.matmul(R, X))
    problem = cp.Problem(objective, constraints)
    objective = problem.solve()

    X = X.value
    X = list(chain.from_iterable(X))


    policy = getpolicy(X, possible_states, possible_actions)

    to_write = {
        "a": A.tolist(),
        "r": R.tolist()[0],
        "alpha": [a for x in alpha for a in x],
        "x": X,
        "policy": policy,
        "objective": objective
    }

    with open("./output/part_3_output.json", "w") as f:
        json.dump(to_write, f)
