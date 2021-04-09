import collections
import numpy as np
import json
import cvxpy as cp
import os
import sys
team_number = 18
cost_arr = [1/2, 1, 2]
step_cost = -20

max_pos = 5  # [N,S,E,W,C]
max_mat = 3
max_arrows = 4
monster_state = 2
monster_health = [0, 25, 50, 75, 100]
num_actions = 10

arrow_damage = 25
blade_damage = 50

pos_ind = 0
mat_ind = 1
arrow_ind = 2
mon_state_ind = 3
mon_health_ind = 4

action_map = ["STAY", "RIGHT", "LEFT", "DOWN", "UP", "SHOOT", "HIT", "CRAFT", "GATHER", "NONE"]
# action_map = ["UP", "LEFT", "DOWN", "RIGHT", "STAY",
#               "SHOOT", "HIT", "CRAFT", "GATHER", "NONE"]
pos_map = ['W', 'N', 'E', 'S', 'C']
monster_state_map = ['D', 'R']

start_state = ['C', 2, 3, 'R', 100]

num_states = max_pos * max_mat * max_arrows * \
    monster_state * len(monster_health)

all_states = []

trace = []

alpha = []

x_arr_length = 0

reward_arr = []

d_to_r = 0.2
r_to_d = 0.5

a_matrix_values = []


def get_num(state_arr):
    return all_states.index(state_arr)


def get_state_fancy(state_arr):
    fancy_state = []
    for i in range(len(state_arr)):
        val = state_arr[i]
        if(i == pos_ind):
            fancy_state.append(pos_map[val])
        elif(i == mon_state_ind):
            fancy_state.append(monster_state_map[val])
        else:
            fancy_state.append(val)
    return fancy_state


def get_state(state_arr):
    state = []
    for val in state_arr:
        if val in pos_map:
            state.append(pos_map.index(val))
        elif val in monster_state_map:
            state.append(monster_state_map.index(val))
        else:
            state.append(val)
    return state


count = 0


def take_action(org_state, new_states, action_num, state_num):
    global count
    a_matrix_values.append([state_num, action_num, 1])
    for new_state, prob in new_states:
        new_state_num = get_num(get_state(new_state))
        if(org_state[mon_state_ind] == 'D'):
            a_matrix_values.append(
                [new_state_num, action_num, -1 * prob * (1 - d_to_r)])

            new_state[mon_state_ind] = 'R'
            if(new_state == ['E', 0, 0, 'R', 0]):
                count += 1
            new_state_mm_num = get_num(get_state(new_state))
            a_matrix_values.append(
                [new_state_mm_num, action_num, -1 * prob * d_to_r])

        else:
            if(new_state == ['E', 0, 0, 'R', 0]):
                count += 1
            a_matrix_values.append(
                [new_state_num, action_num, -1 * prob * (1 - r_to_d)])
            if(org_state[pos_ind] in ['C', 'E']):
                new_state = org_state.copy()
                new_state[mon_health_ind] = min(
                    100, new_state[mon_health_ind] + 25)
                new_state[arrow_ind] = 0
            new_state[mon_state_ind] = 'D'
            new_state_mm_num = get_num(get_state(new_state))
            a_matrix_values.append(
                [new_state_mm_num, action_num, -1 * prob * r_to_d])


def up(state_arr, state_num):
    global x_arr_length
    state_arr = get_state_fancy(state_arr)
    if(state_arr[pos_ind] == 'C' or state_arr[pos_ind] == 'S'):
        x_arr_length += 1

        success_prob = 0.85

        reward = step_cost
        if(state_arr[mon_state_ind] == 'R' and state_arr[pos_ind] == 'C'):
            reward = step_cost * (1 - r_to_d) + (step_cost + -40) * r_to_d
        reward_arr.append(reward)

        action_num = x_arr_length - 1
        new_state = state_arr.copy()
        fail_state = state_arr.copy()
        fail_state[pos_ind] = 'E'

        new_state[pos_ind] = 'C' if state_arr[pos_ind] == 'S' else 'N'

        take_action(state_arr, [[new_state, success_prob], [fail_state, 1 - success_prob]],
                    action_num, state_num)

    else:
        return


def left(state_arr, state_num):
    global x_arr_length
    state_arr = get_state_fancy(state_arr)
    if(state_arr[pos_ind] == 'C' or state_arr[pos_ind] == 'E'):
        x_arr_length += 1
        reward = step_cost
        if(state_arr[mon_state_ind] == 'R'):
            reward = step_cost * (1 - r_to_d) + (step_cost + -40) * r_to_d
        reward_arr.append(reward)

        success_prob = 0.85 if state_arr[pos_ind] == 'C' else 1

        action_num = x_arr_length - 1
        new_state = state_arr.copy()
        fail_state = state_arr.copy()
        fail_state[pos_ind] = 'E'

        new_state[pos_ind] = 'C' if state_arr[pos_ind] == 'E' else 'W'

        take_action(state_arr, [[new_state, success_prob], [fail_state, 1 - success_prob]],
                    action_num, state_num)
    else:
        return


def down(state_arr, state_num):
    global x_arr_length
    state_arr = get_state_fancy(state_arr)
    if(state_arr[pos_ind] == 'C' or state_arr[pos_ind] == 'N'):
        x_arr_length += 1
        reward = step_cost
        if(state_arr[mon_state_ind] == 'R' and state_arr[pos_ind] == 'C'):
            reward = step_cost * (1 - r_to_d) + (step_cost + -40) * r_to_d
        reward_arr.append(reward)

        success_prob = 0.85

        action_num = x_arr_length - 1
        new_state = state_arr.copy()
        fail_state = state_arr.copy()
        fail_state[pos_ind] = 'E'

        new_state[pos_ind] = 'C' if state_arr[pos_ind] == 'N' else 'S'
        take_action(state_arr, [[new_state, success_prob], [fail_state, 1 - success_prob]],
                    action_num, state_num)

    else:
        return


def right(state_arr, state_num):
    global x_arr_length
    state_arr = get_state_fancy(state_arr)
    if(state_arr[pos_ind] == 'C' or state_arr[pos_ind] == 'W'):
        x_arr_length += 1
        reward = step_cost
        if(state_arr[mon_state_ind] == 'R' and state_arr[pos_ind] == 'C'):
            reward = step_cost * (1 - r_to_d) + (step_cost + -40) * r_to_d
        reward_arr.append(reward)

        success_prob = 0.85 if state_arr[pos_ind] == 'C' else 1

        action_num = x_arr_length - 1
        new_state = state_arr.copy()
        fail_state = state_arr.copy()
        fail_state[pos_ind] = 'E'

        new_state[pos_ind] = 'C' if state_arr[pos_ind] == 'W' else 'E'
        take_action(state_arr, [[new_state, success_prob], [fail_state, 1 - success_prob]],
                    action_num, state_num)
    else:
        return


def stay(state_arr, state_num):
    global x_arr_length
    state_arr = get_state_fancy(state_arr)
    x_arr_length += 1
    reward = step_cost
    if(state_arr[mon_state_ind] == 'R' and (state_arr[pos_ind] == 'C' or state_arr[pos_ind] == 'E')):
        reward = step_cost * (1 - r_to_d) + (step_cost + -40) * r_to_d
    reward_arr.append(reward)

    success_prob = 1 if state_arr[pos_ind] in ['W', 'E'] else 0.85

    action_num = x_arr_length - 1
    new_state = state_arr.copy()
    fail_state = state_arr.copy()
    fail_state[pos_ind] = 'E'
    take_action(state_arr, [[new_state, success_prob], [fail_state, 1 - success_prob]],
                action_num, state_num)
    return


def shoot(state_arr, state_num):
    global x_arr_length
    state_arr = get_state_fancy(state_arr)
    if((state_arr[pos_ind] == 'C' or state_arr[pos_ind] == 'E' or state_arr[pos_ind] == 'W') and state_arr[arrow_ind] > 0):
        x_arr_length += 1
        reward = step_cost
        if(state_arr[mon_state_ind] == 'R' and (state_arr[pos_ind] == 'C' or state_arr[pos_ind] == 'E')):
            reward = step_cost * (1 - r_to_d) + (step_cost + -40) * r_to_d
        reward_arr.append(reward)

        success_prob = 0.25
        if(state_arr[pos_ind] == 'C'):
            success_prob = 0.5
        if(state_arr[pos_ind] == 'E'):
            success_prob = 0.9
        action_num = x_arr_length - 1
        new_state = state_arr.copy()
        new_state[arrow_ind] -= 1
        fail_state = new_state.copy()
        new_state[mon_health_ind] -= 25

        take_action(state_arr, [[new_state, success_prob], [fail_state, 1 - success_prob]],
                    action_num, state_num)

    else:
        return


def hit(state_arr, state_num):
    global x_arr_length
    state_arr = get_state_fancy(state_arr)
    if(state_arr[pos_ind] == 'C' or state_arr[pos_ind] == 'E'):
        x_arr_length += 1
        reward = step_cost
        if(state_arr[mon_state_ind] == 'R' and (state_arr[pos_ind] == 'C' or state_arr[pos_ind] == 'E')):
            reward = step_cost * (1 - r_to_d) + (step_cost + -40) * r_to_d
        reward_arr.append(reward)

        success_prob = 0.1
        if(state_arr[pos_ind] == 'E'):
            success_prob = 0.2
        action_num = x_arr_length - 1
        new_state = state_arr.copy()
        fail_state = new_state.copy()
        new_state[mon_health_ind] -= 50
        new_state[mon_health_ind] = max(0, new_state[mon_health_ind])

        take_action(state_arr, [[new_state, success_prob], [fail_state, 1 - success_prob]],
                    action_num, state_num)

    else:
        return


def craft(state_arr, state_num):
    global x_arr_length
    state_arr = get_state_fancy(state_arr)
    if(state_arr[pos_ind] == 'N' and state_arr[mat_ind] > 0):
        x_arr_length += 1
        reward = step_cost
        if(state_arr[mon_state_ind] == 'R' and (state_arr[pos_ind] == 'C' or state_arr[pos_ind] == 'E')):
            reward = step_cost * (1 - r_to_d) + (step_cost + -40) * r_to_d
        reward_arr.append(reward)

        action_num = x_arr_length - 1
        poss_states = []
        probs = [[0.5, 1], [0.35, 2], [0.15, 3]]
        for prob, arrow in probs:
            new_state = state_arr.copy()
            new_state[mat_ind] -= 1
            new_state[arrow_ind] = min(3, state_arr[arrow_ind] + arrow)
            poss_states.append([new_state, prob])
        take_action(state_arr, poss_states, action_num, state_num)

    else:
        return


def gather(state_arr, state_num):
    global x_arr_length
    state_arr = get_state_fancy(state_arr)
    if(state_arr[pos_ind] == 'S'):
        x_arr_length += 1
        reward = step_cost
        if(state_arr[mon_state_ind] == 'R' and (state_arr[pos_ind] == 'C' or state_arr[pos_ind] == 'E')):
            reward = step_cost * (1 - r_to_d) + (step_cost + -40) * r_to_d
        reward_arr.append(reward)

        action_num = x_arr_length - 1
        success_prob = 0.75
        new_state = state_arr.copy()
        new_state[mat_ind] = min(2, state_arr[mat_ind] + 1)
        fail_state = state_arr.copy()

        take_action(state_arr, [[new_state, success_prob], [fail_state, 1 - success_prob]],
                    action_num, state_num)
    else:
        return


action_functions = [up, left, down, right, stay, shoot, hit, craft, gather]


def set_all_states():
    for pos in range(max_pos):
        for mat in range(max_mat):
            for arrows in range(max_arrows):
                for mon_state in range(monster_state):
                    for mon_health in monster_health:
                        state_arr = [pos, mat, arrows, mon_state, mon_health]
                        all_states.append(state_arr.copy())


def set_vectors():
    global x_arr_length
    it = 0
    for pos in range(max_pos):
        for mat in range(max_mat):
            for arrows in range(max_arrows):
                for mon_state in range(monster_state):
                    for mon_health in monster_health:
                        state_arr = [pos, mat, arrows, mon_state, mon_health]
                        if(get_state_fancy(state_arr) == start_state):
                            alpha.append(1)
                        else:
                            alpha.append(0)
                        if(mon_health == 0):  # For End State noop action
                            x_arr_length += 1
                            reward_arr.append(0)
                            a_matrix_values.append([it, x_arr_length - 1, 1])
                        else:
                            for func in action_functions:
                                func(state_arr, it)
                        it += 1


def set_A_matrix():
    global A_matrix
    global a_matrix_values
    for x, y, contri in a_matrix_values:
        A_matrix[x][y] += contri
    pass


set_all_states()
set_vectors()


x_arr = cp.Variable(shape=(x_arr_length, 1), name="x_arr")

A_matrix = np.zeros((num_states, x_arr_length), dtype=float)
set_A_matrix()

alpha_arr = np.array(alpha)
alpha_arr = alpha_arr[:, np.newaxis]
constraints = [cp.matmul(A_matrix, x_arr) == alpha_arr, x_arr >= 0]
objective = cp.Maximize(cp.matmul(reward_arr, x_arr))
problem = cp.Problem(objective, constraints)

solution = problem.solve()
print(solution)

# print(A_matrix.shape)
# print(x_arr.shape)
# print(len(reward_arr))

# print(reward_arr)
for x in A_matrix:
    for y in x:
        print("%.1f" % y, end=" ")
    print("")
