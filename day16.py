import re
import copy
import math
import numpy as np
import functools
import itertools

lines = []
with open("day16.txt") as input_file:
    lines = input_file.read().rstrip().split("\n")

# lines = [
# ".|...\\....",
# "|.-.\\.....",
# ".....|-...",
# "........|.",
# "..........",
# ".........\\",
# "..../.\\\\..",
# ".-.-/..|..",
# ".|....-|.\\",
# "..//.|...."
# ]

def up(curr_beam):
    return (curr_beam[0] - 1, curr_beam[1], "up")
def down(curr_beam):
    return (curr_beam[0] + 1, curr_beam[1], "down")
def left(curr_beam):
    return (curr_beam[0], curr_beam[1] - 1, "left")
def right(curr_beam):
    return (curr_beam[0], curr_beam[1] + 1, "right")

def get_num_energized_beams(initial_beam):
    curr_beams_stack = [initial_beam]
    seen_beams = set()

    while len(curr_beams_stack) != 0:
        curr_beam = curr_beams_stack.pop()
        i, j, direction = curr_beam
        if curr_beam not in seen_beams and not (i < 0 or i >= len(lines) or j < 0 or j >= len(lines[0])):
            match lines[i][j]:
                case "|" if (direction == "left" or direction == "right"):
                    curr_beams_stack.append(up(curr_beam))
                    curr_beams_stack.append(down(curr_beam))
                case "-" if (direction == "up" or direction == "down"):
                    curr_beams_stack.append(left(curr_beam))
                    curr_beams_stack.append(right(curr_beam))
                case "\\":
                    match direction:
                        case "right":
                            curr_beams_stack.append(down(curr_beam))
                        case "down":
                            curr_beams_stack.append(right(curr_beam))
                        case "left":
                            curr_beams_stack.append(up(curr_beam))
                        case "up":
                            curr_beams_stack.append(left(curr_beam))
                case "/":
                    match direction:
                        case "right":
                            curr_beams_stack.append(up(curr_beam))
                        case "up":
                            curr_beams_stack.append(right(curr_beam))
                        case "left":
                            curr_beams_stack.append(down(curr_beam))
                        case "down":
                            curr_beams_stack.append(left(curr_beam))
                case _:
                    match direction:
                        case "right":
                            curr_beams_stack.append(right(curr_beam))
                        case "up":
                            curr_beams_stack.append(up(curr_beam))
                        case "left":
                            curr_beams_stack.append(left(curr_beam))
                        case "down":
                            curr_beams_stack.append(down(curr_beam))
            seen_beams.add(curr_beam)

    energized = set()
    for beam in seen_beams:
        energized.add((beam[0], beam[1]))

    return len(energized)

print("Part 1:", get_num_energized_beams((0, 0, "right")))

max_beams = -math.inf
beams_to_check = []
for i in range(len(lines)):
    beams_to_check.append((i, 0, "right"))
    beams_to_check.append((i, len(lines[0]) - 1, "left"))

for j in range(len(lines[0])):
    beams_to_check.append((0, j, "down"))
    beams_to_check.append((len(lines) - 1, j, "up"))

for beam in beams_to_check:
    num_beams = get_num_energized_beams(beam)
    if num_beams > max_beams:
        max_beams = num_beams

print("Part 2:", max_beams)