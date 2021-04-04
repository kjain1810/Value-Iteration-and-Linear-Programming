import random

f = open("lastiteration.txt", "r")

lines = f.readlines()

i = 0

dit = {}

while i < len(lines):
    dit[lines[i]] = lines[i + 1]
    i += 2

position = "W 0 0 D 4\n"

while True:
    action = dit[position]
