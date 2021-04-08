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
            vec_here[index_here] = 1
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
                if i == "E02R3":
                    print(action, vec_here, av_reward)
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

    alpha[ENUM["W00D4"]] = 1

    alpha = alpha.transpose()
    alpha = np.array(alpha)
    alpha = alpha[:, np.newaxis]

    print(A)

    X = cp.Variable(shape=(size, 1), name="X")
    constraints = [cp.matmul(A, X) == alpha, X >= 0]
    objective = cp.Maximize(cp.matmul(R, X))
    problem = cp.Problem(objective, constraints)
    objective = problem.solve()

    X = X.value
    print(X)
    X = list(chain.from_iterable(X))

    # print(len(X))

    policy = getpolicy(X, possible_states, possible_actions)

    to_write = {
        "a": A.tolist(),
        "r": R.tolist(),
        "alpha": alpha.tolist(),
        "x": X,
        "policy": policy,
        "objective": objective
    }

    with open("./output/part_3_output.json", "w") as f:
        json.dump(to_write, f)
    print(objective)
