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
    for pos in POSITION:
        for mat in MATERIAL:
            for arrow in ARROW:
                for state in STATE:
                    for health in HEALTH:
                        if health == 0:
                            continue
                        ij = IndianaJones(
                            pos, mat, arrow, state, 25 * health, 0)
                        enum_here = ''.join(
                            [pos, str(mat), str(arrow), state, str(health)])
                        index_here = ENUM[enum_here]
                        actions = ij.getNextStates()
                        for action in actions:
                            vec_here = np.zeros(total_states)
                            avg_reward = 0
                            for ns in action["states"]:
                                vec_here[index_here] += ns["probability"]
                                enum = ''.join(
                                    [ns["next_pos"], str(ns["next_mat"]), str(ns["next_arrow"]), ns["next_mmstate"], str(ns["next_mmhealth"]//25)])
                                index = ENUM[enum]
                                vec_here[index] = -ns["probability"]
                                avg_reward += ns["reward"]
                            possible_states[index_here] += 1
                            if len(action["states"]) > 0:
                                avg_reward /= len(action["states"])
                            R.append(avg_reward)
                            A.append(vec_here.tolist())
                            possible_actions.append(action["action"])
    return A, R, possible_states, possible_actions


def getpolicy(X, possible_states, possible_actions):
    idx = 0
    j = 0
    policy = []

    for i in ENUM:
        print(i)
        print("\t", possible_states[ENUM[i]])
        if possible_states[ENUM[i]] > 0:
            index = np.argmax(X[int(idx): idx + int(possible_states[ENUM[i]])])
            policy.append(
                [[i[0], (ord(i[1]) - ord('0')), ord(i[2]) - ord('0'), i[3], 25 * (ord(i[4]) - ord('0'))], possible_actions[idx + index]])
            idx += int(possible_states[ENUM[i]])
    # for pos in POSITION:
    #     for mat in MATERIAL:
    #         for arrow in ARROW:
    #             for state in STATE:
    #                 for health in HEALTH:
    #                     if health == 0:
    #                         continue
    #                     if possible_states[j] == 0:
    #                         j += 1
    #                         # policy.append("LMAO")
    #                         continue
    #                     index = np.argmax(
    #                         X[int(i):i + int(possible_states[j])])
    #                     policy.append(
    #                         [[pos, mat, arrow, state, 25 * health], possible_actions[i + index]])
    #                     i += int(possible_states[j])
    #                     j += 1

    return policy


if __name__ == "__main__":
    total_states = enumerate_states()
    A, R, possible_states, possible_actions = genAandR(total_states)

    idx = 0
    for i in ENUM:
        print(i, ":")
        for j in range(int(possible_states[ENUM[i]])):
            print("\t", possible_actions[int(idx + j)])
        idx += possible_states[ENUM[i]]

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

    X = cp.Variable(shape=(size, 1), name="X")
    constraints = [cp.matmul(A, X) == alpha, X >= 0]
    objective = cp.Maximize(cp.matmul(R, X))
    problem = cp.Problem(objective, constraints)
    objective = problem.solve()

    X = X.value
    X = list(chain.from_iterable(X))

    print(len(X))

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
