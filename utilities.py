import math

state_space = ["A", "B", "C", "D"] # TODO: CHANGE
exit_state = "E" # TODO: CHANGE

action_space = {
    "A": {"up": [("A", 0.2, -1), ("C", 0.8, -1)], "right": [("A", 0.2, -1), ("B", 0.8, -1)]},
    "B": {"up": [("B", 0.2, -1), ("D", 0.8, -4)], "left": [("A", 0.8, -1), ("B", 0.2, -1)]},
    "C": {"right": [("D", 0.25, -3), ("C", 0.75, -1)], "down": [("A", 0.8, -1), ("C", 0.2, -1)]},
    "D": {}
} # TODO: CHANGE
REWARDS = 15 # TODO: CHANGE
U = {"A": 0, "B": 0, "C": 0, "D": REWARDS} # TODO: CHANGE
U_starting = {"A": -100, "B": -100, "C": -100, "D": REWARDS} # TODO: CHANGE
gamma = 0.2 # TODO: CHANGE
delta = 0.02 # TODO: CHANGE

it_no = 1

while True:
    print("Iteration number:", it_no)
    U_new = U_starting.copy()
    for state in state_space:
        print("\tState:", state)
        for action in action_space[state]:
            print("\taction =", action)
            possible_results = action_space[state][action]
            print("\t\tU_"+action+" = ", end="")
            for res in possible_results:
                print("P_"+res[0]+" x (" + "R_" + res[0] + " + gamma x E_" + str(int(it_no - 1)) + "(" + res[0] + ")) + ", end="")
            print()
            print("\t\tU_"+action+" = ", end="")
            here = 0
            for res in possible_results:
                print("%f x (%f + %f*(%f)) + "%(res[1], res[2], gamma, U[res[0]]), end="")
                here += res[1] * (res[2] + gamma * U[res[0]])
            print("\n\t\tU_"+action+" =", here)
            print()
            U_new[state] = max(U_new[state], here)

    ch = 0
    for state in state_space:
        ch = max(ch, abs(U_new[state] - U[state]))
    U = U_new
    print("States after iteration number:", it_no-1)
    for state in state_space:
        print(state, ":", U[state])
    print()
    print("Bellman error:", ch)
    print()
    print()
    if ch < delta:
        break
    it_no += 1
