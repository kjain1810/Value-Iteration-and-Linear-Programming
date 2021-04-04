import math

state_space = ["A", "B", "C", "D", "E"]# TODO: CHANGE
exit_state = "E" # TODO: CHANGE

action_space = {
    "A": {"right": [("A", 0.2, -1), ("C", 0.8, -1)]},
    "B": {"down": [("C", 0.8, -1), ("B", 0.2, -1)]},
    "C": {"right": [("E", 0.25, -3), ("C", 0.75, -1)], "down": [("D", 0.8, -1), ("C", 0.2, -1)], "up": [("B", 0.8, -1), ("C", 0.2, -1)], "left": [("A", 0.8, -1), ("C", 0.2, -1)]},
    "D": {"up": [("C", 0.8, -1), ("D", 0.2, -1)]},
    "E": {}
}# TODO: CHANGE
REWARDS = 16# TODO: CHANGE
U = {"A": 0, "B": 0, "C": 0, "D": 0, "E": REWARDS}# TODO: CHANGE
U_starting = {"A": -100, "B": -100, "C": -100, "D": -100, "E": REWARDS}# TODO: CHANGE
gamma = 0.2# TODO: CHANGE
delta = 0.003# TODO: CHANGE

it_no = 1

while True:
    print("-----------------------------------------------------------------------------------------------\n")
    print("Iteration number:", it_no)
    it_no += 1
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
            print("\t\tU_"+action+"= ", end="")
            here = 0
            for res in possible_results:
                print("%r(%r + %r*(%r)) + "%(res[1], res[2], gamma, U[res[0]]), end="")
                here += res[1] * (res[2] + gamma * U[res[0]])
            print("\n\t\tU_"+action+"= %r"%(round(here, 7)))
            print()
            U_new[state] = round(max(U_new[state], here), 7)

    ch = 0
    for state in state_space:
        ch = max(ch, abs(U_new[state] - U[state]))
    U = U_new
    print("States after iteration number:", it_no-1)
    for state in state_space:
        print(state, ": %r"%(U[state]))
    print()
    print("Bellman error:", ch)
    print()
    print()
    if ch < delta:
        break
