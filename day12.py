import re
import copy
import math
import numpy as np
import functools
import itertools

lines = []
with open("day12.txt") as input_file:
    lines = input_file.read().rstrip().split("\n")

# lines = [
# "???.### 1,1,3",
# ".??..??...?##. 1,1,3",
# "?#?#?#?#?#?#?#? 1,3,1,6",
# "????.#...#... 4,1,1",
# "????.######..#####. 1,6,5",
# "?###???????? 3,2,1"
# ]

@functools.cache
def num_valid_combinations(springs, sizes):
    if len(springs) == 0:
        if len(sizes) == 0:
            return 1
        else:
            return 0
    else:
        first = springs[0]
        if first == ".":
            return num_valid_combinations(springs[1:], sizes)
        elif first == "#":
            if (len(sizes) == 0) or (len(springs) < sizes[0] + 1) or (springs[sizes[0]] == "#") or ("." in springs[:sizes[0]]):
                return 0
            else:
                return num_valid_combinations(springs[sizes[0]+1:], sizes[1:])
        else:
            return num_valid_combinations("." + springs[1:], sizes) + num_valid_combinations("#" + springs[1:], sizes)

total_p1 = 0
total_p2 = 0
for line in lines:
    springs_with_unknown, actual_sizes = line.split()
    actual_sizes = tuple([int(x) for x in actual_sizes.split(",")])
    springs_with_unknown_p2 = "?".join([springs_with_unknown] * 5)
    actual_sizes_p2 = actual_sizes * 5

    total_p1 += num_valid_combinations(springs_with_unknown + ".", actual_sizes)
    total_p2 += num_valid_combinations(springs_with_unknown_p2 + ".", actual_sizes_p2)

print("Part 1:", total_p1)
print("Part 2:", total_p2)