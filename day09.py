import re
import copy
import math
import numpy as np
import functools
import itertools

lines = []
with open("day09.txt") as input_file:
    lines = input_file.read().rstrip().split("\n")

# lines = [
# "0 3 6 9 12 15",
# "1 3 6 10 15 21",
# "10 13 16 21 30 45"
# ]

total_p1 = 0
total_p2 = 0
for line in lines:
    history = [int(x) for x in line.split()]
    differences = [history]
    while not all(x == 0 for x in differences[-1]):
        new_difference = []
        for i in range(len(differences[-1]) - 1):
            diff = differences[-1][i+1] - differences[-1][i]
            new_difference.append(diff)
        differences.append(new_difference)

    right_sum = 0
    for difference in differences:
        right_sum += difference[-1]
    total_p1 += right_sum

    left_sum = 0
    for difference in differences[::-1]:
        left_sum = difference[0] - left_sum
    total_p2 += left_sum

print("Part 1:", total_p1)
print("Part 2:", total_p2)