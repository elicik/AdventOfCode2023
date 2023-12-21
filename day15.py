import re
import copy
import math
import numpy as np
import functools
import itertools

lines = []
with open("day15.txt") as input_file:
    lines = input_file.read().rstrip().split("\n")

# lines = [
# "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"
# ]

inputs = lines[0].split(",")
longest_input = max([len(input) for input in inputs])
multiples_of_seventeen = [17 ** x for x in range(longest_input + 1)]

def hash(input):
    output = 0
    for i, char in enumerate(input):
        output += ord(char) * multiples_of_seventeen[len(input) - i]
    return output % 256

total = 0
for input in inputs:
    total += hash(input)

print("Part 1:", total)

hashmap = []
for i in range(256):
    hashmap.append([])

for input in inputs:
    arr = re.match("(\w+)([=-])(\d*)", input)
    label, operation, focal_length = arr[1], arr[2], arr[3]
    box_number = hash(label)
    if operation == "=":
        found = False
        for i, lens in enumerate(hashmap[box_number]):
            if lens[0] == label:
                hashmap[box_number][i] = (label, focal_length)
                found = True
                break
        if not found:
            hashmap[box_number].append((label, focal_length))
    else:
        for i, lens in enumerate(hashmap[box_number]):
            if lens[0] == label:
                del hashmap[box_number][i]
                break

focusing_power = 0
for box_number in range(256):
    for i, lens in enumerate(hashmap[box_number], start=1):
        focusing_power += (box_number + 1) * i * int(lens[1])

print("Part 2:", focusing_power)