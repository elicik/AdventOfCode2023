import re
import copy
import math
import numpy as np
import functools
import itertools

lines = []
with open("day11.txt") as input_file:
    lines = input_file.read().rstrip().split("\n")

# lines = [
# "...#......",
# ".......#..",
# "#.........",
# "..........",
# "......#...",
# ".#........",
# ".........#",
# "..........",
# ".......#..",
# "#...#....."
# ]

empty_rows = []
for i, row in enumerate(lines):
    if all(x == "." for x in row):
        empty_rows.append(i)

empty_cols = []
for j in range(len(lines[0])):
    if all(lines[i][j] == "." for i in range(len(lines))):
        empty_cols.append(j)

galaxies = []
for i, line in enumerate(lines):
    for j, char in enumerate(line):
        if char == "#":
            galaxies.append((i, j))

def get_num_empty_rows_cols_in_range(a, b):
    min_i = min([a[0], b[0]])
    max_i = max([a[0], b[0]])
    min_j = min([a[1], b[1]])
    max_j = max([a[1], b[1]])
    num_empty_rows = 0
    num_empty_cols = 0
    for row in empty_rows:
        if min_i < row < max_i:
            num_empty_rows += 1
    for col in empty_cols:
        if min_j < col < max_j:
            num_empty_cols += 1
    return (num_empty_rows, num_empty_cols)

part1_total = 0
part2_total = 0

for (a, b) in itertools.combinations(galaxies, 2):
    num_empty_rows, num_empty_cols = get_num_empty_rows_cols_in_range(a, b)
    part1_total += (num_empty_rows + num_empty_cols) + abs(b[0] - a[0]) + abs(b[1] - a[1])
    part2_total += 999999*(num_empty_rows + num_empty_cols) + abs(b[0] - a[0]) + abs(b[1] - a[1])

print("Part 1:", part1_total)
print("Part 2:", part2_total)