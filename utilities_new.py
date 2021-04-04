import math

state_space = ["A", "B", "C"]
exit_state = "D"


action_space = {
    "A": {"up": [("A", 0.2, -1), ("C", 0.8, -1)], "right": [("A", 0.2, -1), ("B", 0.8, -1)]},
    "B": {"up": [("B", 0.2, -1), ("D", 0.8, -4)], "left": [("A", 0.8, -1), ("B", 0.2, -1)]},
    "C": {"right": [("D", 0.25, -3), ("C", 0.75, -1)], "down": [("A", 0.8, -1), ("C", 0.2, -1)]},
    "D": {}
}
REWARDS = 16
U = {"A": 0, "B": 0, "C": 0, "D": REWARDS}
gamma = 0.2
delta = 0.02

it_no = 1

while True:
    print("Iteration number:", it_no)
    it_no += 1
    U_new = {"A": -100, "B": -100, "C": -100, "D": REWARDS}
    for state in state_space:
        print("\tState:", state)
        for action in action_space[state]:
            print("\taction =", action)
            possible_results = action_space[state][action]
            # print(possible_results)
            print("\t\tU_"+action+"= ", end="")
            here = 0
            for res in possible_results:
                print("%fx(%f + %f*(%f)) + "%(res[1], res[2], gamma, U[res[0]]), end="")
                here += res[1] * (res[2] + gamma * U[res[0]])
            print("\n\t\tU_"+action+"=", here)
            print()
            U_new[state] = max(U_new[state], here)

    ch = 0
    for state in state_space:
        ch = max(ch, abs(U_new[state] - U[state]))
    U = U_new
    # print(U)
    print("States after iteration number:", it_no-1)
    for state in state_space:
        print(state, ":", U[state])
    print()
    print()
    # break
    if ch < delta:
        break
