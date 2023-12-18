import re
import copy
import math
import numpy as np
import functools
import itertools

lines = []
with open("day08.txt") as input_file:
    lines = input_file.read().rstrip().split("\n")

# lines = [
# "RL",
# "",
# "AAA = (BBB, CCC)",
# "BBB = (DDD, EEE)",
# "CCC = (ZZZ, GGG)",
# "DDD = (DDD, DDD)",
# "EEE = (EEE, EEE)",
# "GGG = (GGG, GGG)",
# "ZZZ = (ZZZ, ZZZ)"
# ]

map = {}
for line in lines[2:]:
    arr = re.match("(\w{3}) = \((\w{3}), (\w{3})\)", line)
    map[arr[1]] = (arr[2], arr[3])

curr = "AAA"
steps = 0
directions = itertools.cycle(lines[0])
while curr != "ZZZ":
    steps += 1
    direction = next(directions)
    if direction == "L":
        curr = map[curr][0]
    else:
        curr = map[curr][1]


print("Part 1:", steps)

def steps_needed(node):
    curr = node
    steps = 0
    directions = itertools.cycle(lines[0])
    while not curr.endswith("Z"):
        steps += 1
        direction = next(directions)
        if direction == "L":
            curr = map[curr][0]
        else:
            curr = map[curr][1]
    return steps

steps = []
for node in map.keys():
    if node.endswith("A"):
        steps.append(steps_needed(node))
steps.append(len(lines[0]))

print("Part 2:", math.lcm(*steps))