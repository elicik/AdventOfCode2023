import re
import copy
import math
import numpy as np
import functools
import itertools

lines = []
with open("day10.txt") as input_file:
    lines = input_file.read().rstrip().split("\n")

# lines = [
# "7-F7-",
# ".FJ|7",
# "SJLL7",
# "|F--J",
# "LJ.LJ"
# ]

# lines = [
# "FF7FSF7F7F7F7F7F---7",
# "L|LJ||||||||||||F--J",
# "FL-7LJLJ||||||LJL-77",
# "F--JF--7||LJLJIF7FJ-",
# "L---JF-JLJIIIIFJLJJ7",
# "|F|F-JF---7IIIL7L|7|",
# "|FFJF7L7F-JF7IIL---7",
# "7-L-JL7||F7|L7F-7F7|",
# "L.L7LFJ|||||FJL7||LJ",
# "L7JLJL-JLJLJL--JLJ.L"
# ]

# Find S, look around it, start following a pipe until I see S again

for i, line in enumerate(lines):
    found = False
    for j, letter in enumerate(line):
        if letter == "S":
            S = (i, j)
            found = True
            break
    if found:
        break

def get_starting_location():
    if S[0] != 0:
        letter = lines[S[0] - 1][S[1]]
        if letter in ["7","F","|"]:
            return (S[0] - 1, S[1])
    if S[0] != len(lines) - 1:
        letter = lines[S[0] + 1][S[1]]
        if letter in ["L","J","|"]:
            return (S[0] + 1, S[1])
    if S[1] != 0:
        letter = lines[S[0]][S[1] - 1]
        if letter in ["F","L","-"]:
            return (S[0], S[1] - 1)

start = get_starting_location()

prev = S
curr = start
steps = 1
loop = set(S)
inner = set()
outer = set()
while curr != S:
    loop.add(curr)
    steps += 1
    letter = lines[curr[0]][curr[1]]
    # print(curr, letter)
    # input()
    if curr[0] == prev[0] - 1:
        prev = curr
        if letter == "F":
            outer.add((curr[0], curr[1] - 1))
            outer.add((curr[0] - 1, curr[1]))
            curr = (curr[0], curr[1] + 1)
        elif letter == "7":
            inner.add((curr[0], curr[1] + 1))
            inner.add((curr[0] - 1, curr[1]))
            curr = (curr[0], curr[1] - 1)
        else:
            outer.add((curr[0], curr[1] - 1))
            inner.add((curr[0], curr[1] + 1))
            curr = (curr[0] - 1, curr[1])
    elif curr[0] == prev[0] + 1:
        prev = curr
        if letter == "L":
            inner.add((curr[0], curr[1] - 1))
            inner.add((curr[0] + 1, curr[1]))
            curr = (curr[0], curr[1] + 1)
        elif letter == "J":
            outer.add((curr[0], curr[1] + 1))
            outer.add((curr[0] + 1, curr[1]))
            curr = (curr[0], curr[1] - 1)
        else:
            inner.add((curr[0], curr[1] - 1))
            outer.add((curr[0], curr[1] + 1))
            curr = (curr[0] + 1, curr[1])
    elif curr[1] == prev[1] + 1:
        prev = curr
        if letter == "7":
            outer.add((curr[0] - 1, curr[1]))
            outer.add((curr[0], curr[1] + 1))
            curr = (curr[0] + 1, curr[1])
        elif letter == "J":
            inner.add((curr[0] + 1, curr[1]))
            inner.add((curr[0], curr[1] + 1))
            curr = (curr[0] - 1, curr[1])
        else:
            outer.add((curr[0] - 1, curr[1]))
            inner.add((curr[0] + 1, curr[1]))
            curr = (curr[0], curr[1] + 1)
    else:
        prev = curr
        if letter == "F":
            inner.add((curr[0] - 1, curr[1]))
            inner.add((curr[0], curr[1] - 1))
            curr = (curr[0] + 1, curr[1])
        elif letter == "L":
            outer.add((curr[0] + 1, curr[1]))
            outer.add((curr[0], curr[1] - 1))
            curr = (curr[0] - 1, curr[1])
        else:
            inner.add((curr[0] - 1, curr[1]))
            outer.add((curr[0] + 1, curr[1]))
            curr = (curr[0], curr[1] - 1)

print("Part 1:", steps // 2)

def remove_out_of_bounds_and_loop(my_set):
    for (i, j) in my_set.copy():
        if (i < 0) or (i > len(lines) - 1) or (j < 0) or (j > len(lines[0]) - 1):
            my_set.remove((i, j))
    my_set -= loop

remove_out_of_bounds_and_loop(inner)
remove_out_of_bounds_and_loop(outer)

while True:
    inner_size = len(inner)
    set_to_add = set()
    for (i, j) in inner:
        set_to_add.add((i - 1, j))
        set_to_add.add((i + 1, j))
        set_to_add.add((i, j - 1))
        set_to_add.add((i, j + 1))
    inner |= set_to_add
    remove_out_of_bounds_and_loop(inner)
    if len(inner) == inner_size:
        break

while True:
    outer_size = len(outer)
    set_to_add = set()
    for (i, j) in outer:
        set_to_add.add((i - 1, j))
        set_to_add.add((i + 1, j))
        set_to_add.add((i, j - 1))
        set_to_add.add((i, j + 1))
    outer |= set_to_add
    remove_out_of_bounds_and_loop(outer)
    if len(outer) == outer_size:
        break

if outer.isdisjoint([(0, 0), (len(lines) - 1, 0), (0, len(lines[0]) - 1), (len(lines) - 1, len(lines[0]) - 1)]):
    # Swap if needed
    temp = outer
    outer = inner
    inner = temp

print("Part 2:", len(inner))