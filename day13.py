import re
import copy
import math
import numpy as np
import functools
import itertools

lines = []
with open("day13.txt") as input_file:
    lines = input_file.read().rstrip().split("\n")

# lines = [
# "#.##..##.",
# "..#.##.#.",
# "##......#",
# "##......#",
# "..#.##.#.",
# "..##..##.",
# "#.#.##.#.",
# "",
# "#...##..#",
# "#....#..#",
# "..##..###",
# "#####.##.",
# "#####.##.",
# "..##..###",
# "#....#..#"
# ]

maps_strs = []
curr_map = []
for line in lines:
    if line == "":
        maps_strs.append(curr_map)
        curr_map = []
    else:
        curr_map.append(line)
maps_strs.append(curr_map)

maps = []
for map_str in maps_strs:
    map = np.full((len(map_str), len(map_str[0])), False)
    for i, line in enumerate(map_str):
        for j, char in enumerate(line):
            map[i,j] = char == "#"
    maps.append(map)

def get_line_of_reflection(map, presmudge_reflection=(None,None)):
    reflect_row, reflect_col = None, None
    for row in range(1, map.shape[0]):
        size = min([row, map.shape[0] - row])
        up = map[row - size:row]
        down = map[row:row+size][::-1]
        if np.array_equal(up, down) and row != presmudge_reflection[0]:
            reflect_row = row
    for col in range(1, map.shape[1]):
        size = min([col, map.shape[1] - col])
        left = map[:,col - size:col]
        right = map[:,col:col+size][:,::-1]
        if np.array_equal(left, right) and col != presmudge_reflection[1]:
            reflect_col = col
    return (reflect_row, reflect_col)

total_p1 = 0
total_p2 = 0
for map in maps:
    row, col = get_line_of_reflection(map)
    if row is not None:
        total_p1 += row * 100
    if col is not None:
        total_p1 += col

    found = False
    for i in range(map.shape[0]):
        for j in range(map.shape[1]):
            new_map = np.copy(map)
            new_map[i,j] = not new_map[i,j]
            new_row, new_col = get_line_of_reflection(new_map, (row, col))
            if new_row is not None or new_col is not None:
                found = True
                break
        if found:
            break
    if new_row is not None:
        total_p2 += new_row * 100
    if new_col is not None:
        total_p2 += new_col

print("Part 1:", total_p1)
print("Part 2:", total_p2)