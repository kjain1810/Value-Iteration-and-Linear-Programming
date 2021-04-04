import random
import time
random.seed(time.time())
f = open("lastiteration.txt", "r")

lines = f.readlines()

i = 0

dit = {}

while i < len(lines):
    X = [lines[i][0], lines[i][2], lines[i][4], lines[i][6], lines[i][8]]
    dit[''.join(X)] = lines[i + 1][:-1]
    i += 2

position = ["C", "2", "0", "R", "4"]


def doAction(action, position, new_state):
    prob = random.random()
    if action == "SHOOT":
        new_state[0] = position[0]
        new_state[1] = position[1]
        new_state[2] = chr(ord(position[2]) - 1)
        if (position[0] == 'C' and prob <= 0.5) or (position[0] == 'E' and prob <= 0.9) or (position[0] == 'W' and prob <= 0.25):
            new_state[4] = chr(ord(position[4]) - 1)
        else:
            new_state[4] = position[4]
    elif action == "HIT":
        new_state[0] = position[0]
        new_state[1] = position[1]
        new_state[2] = position[2]
        if (position[0] == 'C' and prob <= 0.1) or (position[0] == 'E' and prob <= 0.2):
            new_state[4] = max('0', chr(ord(position[4]) - 2))
        else:
            new_state[4] = position[4]
    elif action == "GATHER":
        new_state[0] = position[0]
        if prob <= 0.75:
            new_state[1] = max('2', chr(ord(position[1]) + 1))
        else:
            new_state[1] = position[1]
        new_state[2] = position[2]
        new_state[4] = position[4]
    elif action == "CRAFT":
        new_state[0] = position[0]
        new_state[1] = chr(ord(position[1]) - 1)
        if prob <= 0.5:
            new_state[2] = max('3', chr(ord(position[2]) + 1))
        elif prob <= 0.85:
            new_state[2] = max('3', chr(ord(position[2]) + 2))
        else:
            new_state[2] = max('3', chr(ord(position[2]) + 3))
        new_state[4] = position[4]
    else:
        new_state[1] = position[1]
        new_state[2] = position[2]
        new_state[4] = position[4]
        if action == "STAY":
            if position[0] == "E" or position[0] == "W":
                new_state[0] = position[0]
            elif prob <= 0.85:
                new_state[0] = position[0]
            else:
                new_state[0] = 'E'
        elif position[0] == 'E' or position[0] == 'W':
            new_state[0] = 'C'
        else:
            if position[0] == 'N' or position[0] == 'S':
                if prob <= 0.85:
                    new_state[0] = 'C'
                else:
                    new_state[0] = 'E'
            else:
                if prob > 0.85 or action == "RIGHT":
                    new_state[0] = 'E'
                elif action == "LEFT":
                    new_state[0] = 'W'
                elif action == "UP":
                    new_state[0] = 'N'
                elif action == "DOWN":
                    new_state[0] = 'S'
                    print("here")


while True:
    action = dit[''.join(position)]
    print(position)
    print(action)
    if action[0] == "e":
        break
    new_state = ['', '', '', '', '']

    mm_prob = random.random()

    mm_shooting = False
    if position[3] == 'D':
        if mm_prob <= 0.2:
            new_state[3] = 'R'
        else:
            new_state[3] = 'D'
    else:
        if mm_prob <= 0.5:
            mm_shooting = True
            new_state[3] = 'D'
        else:
            new_state[3] = 'R'
    if mm_shooting:
        if position[0] != 'E' and position[0] != 'C':
            doAction(action, position, new_state)
        else:
            new_state[0] = position[0]
            new_state[1] = position[1]
            new_state[2] = '0'
            new_state[4] = min('4', chr(ord(position[3]) + 1))
    else:
        doAction(action, position, new_state)
    position = new_state

print("Game over!")
