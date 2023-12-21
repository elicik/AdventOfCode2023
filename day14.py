import re
import copy
import math
import numpy as np
import functools
import itertools

lines = []
with open("day14.txt") as input_file:
    lines = input_file.read().rstrip().split("\n")

# lines = [
# "O....#....",
# "O.OO#....#",
# ".....##...",
# "OO.#O....O",
# ".O.....O#.",
# "O.#..O.#.#",
# "..O..#O..O",
# ".......O..",
# "#....###..",
# "#OO..#...."
# ]

cube_rocks = np.full((len(lines), len(lines[0])), False)
round_rocks = np.full((len(lines), len(lines[0])), False)
load_weights = np.arange(len(lines), 0, -1)

for i, line in enumerate(lines):
    for j, char in enumerate(line):
        cube_rocks[i,j] = char == "#"
        round_rocks[i,j] = char == "O"

original_round_rocks = np.copy(round_rocks)

def tilt_north():
    for col in range(cube_rocks.shape[1]):
        cube_rock_indexes = [-1] + cube_rocks[:,col].nonzero()[0].tolist() + [cube_rocks.shape[0]]
        for i in range(len(cube_rock_indexes) - 1):
            start = cube_rock_indexes[i] + 1
            end = cube_rock_indexes[i+1]
            if start == end:
                continue
            num_rocks = np.count_nonzero(round_rocks[start:end,col])
            round_rocks[start:start+num_rocks,col] = True
            round_rocks[start+num_rocks:end,col] = False

def tilt_west():
    for row in range(cube_rocks.shape[0]):
        cube_rock_indexes = [-1] + cube_rocks[row,:].nonzero()[0].tolist() + [cube_rocks.shape[1]]
        for i in range(len(cube_rock_indexes) - 1):
            start = cube_rock_indexes[i] + 1
            end = cube_rock_indexes[i+1]
            if start == end:
                continue
            num_rocks = np.count_nonzero(round_rocks[row,start:end])
            round_rocks[row,start:start+num_rocks] = True
            round_rocks[row,start+num_rocks:end] = False

def tilt_south():
    for col in range(cube_rocks.shape[1]):
        cube_rock_indexes = [-1] + cube_rocks[:,col].nonzero()[0].tolist() + [cube_rocks.shape[0]]
        for i in range(len(cube_rock_indexes) - 1):
            start = cube_rock_indexes[i] + 1
            end = cube_rock_indexes[i+1]
            if start == end:
                continue
            num_rocks = np.count_nonzero(round_rocks[start:end,col])
            round_rocks[end-num_rocks:end,col] = True
            round_rocks[start:end-num_rocks,col] = False

def tilt_east():
    for row in range(cube_rocks.shape[0]):
        cube_rock_indexes = [-1] + cube_rocks[row,:].nonzero()[0].tolist() + [cube_rocks.shape[1]]
        for i in range(len(cube_rock_indexes) - 1):
            start = cube_rock_indexes[i] + 1
            end = cube_rock_indexes[i+1]
            if start == end:
                continue
            num_rocks = np.count_nonzero(round_rocks[row,start:end])
            round_rocks[row,end-num_rocks:end] = True
            round_rocks[row,start:end-num_rocks] = False

def get_load():
    sum_of_round_rocks_per_row = np.sum(round_rocks, axis=1)
    return np.dot(load_weights, sum_of_round_rocks_per_row)

tilt_north()
load = get_load()
print("Part 1:", get_load())
round_rocks = original_round_rocks


load_p2 = None
previous_results = []
for current_index in range(1000000000):
    tilt_north()
    tilt_west()
    tilt_south()
    tilt_east()
    found = False
    for found_index, previous_result in enumerate(previous_results):
        if np.array_equal(round_rocks, previous_result):
            found = True
            break
    if found:
        cycle_length = current_index - found_index
        # 0th index was after 1 cycle, so we want the (1000000000 - 1)th index
        index_within_cycle = (1000000000 - 1 - current_index) % cycle_length
        index_to_check_load_of = found_index + index_within_cycle
        round_rocks = previous_results[index_to_check_load_of]
        load_p2 = get_load()
        break
    previous_results.append(np.copy(round_rocks))

print("Part 2:", load_p2)