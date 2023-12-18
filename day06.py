import re
import copy
import math
import numpy as np
import functools
import itertools

lines = []
with open("day06.txt") as input_file:
    lines = input_file.read().rstrip().split("\n")

# lines = [
# "Time:      7  15   30",
# "Distance:  9  40  200"
# ]

arr_time = re.match("Time:\s+(.*)", lines[0])
arr_distance = re.match("Distance:\s+(.*)", lines[1])

times = [int(x) for x in arr_time[1].split()]
distances = [int(x) for x in arr_distance[1].split()]

combined_time = int(arr_time[1].replace(" ",""))
combined_distance = int(arr_distance[1].replace(" ",""))

# b^2 - tb + d < 0
# b between the roots is negative
def get_num_answers(t, d):
    sqrt = math.sqrt(t * t - 4 * d)
    b_1 = (t + sqrt) / 2
    b_2 = (t - sqrt) / 2
    if b_1.is_integer():
        b_1 -= 1
    if b_2.is_integer():
        b_2 += 1
    return math.floor(b_1) - math.ceil(b_2) + 1
    # print(b_1, b_2, number_of_answers)

total = 1
for t, d in zip(times, distances):
    total *= get_num_answers(t, d)

print("Part 1:", total)

print("Part 2:", get_num_answers(combined_time, combined_distance))