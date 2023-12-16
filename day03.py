import re
import copy
import math
import numpy as np

lines = []
with open("day03.txt") as input_file:
    lines = input_file.read().rstrip().split("\n")

# lines = [
# "467..114..",
# "...*......",
# "..35..633.",
# "......#...",
# "617*......",
# ".....+.58.",
# "..592.....",
# "......755.",
# "...$.*....",
# ".664.598.."
# ]

schematic = np.full((len(lines), len(lines[0])), False)
gear = np.full((len(lines), len(lines[0])), False)
for i, line in enumerate(lines):
    for j, char in enumerate(line):
        schematic[i,j] = not (char.isdigit() or char == ".")
        gear[i,j] = char == "*"

def print_box(lower_i, upper_i, lower_j, upper_j):
    for i in range(lower_i, upper_i + 1):
        print(lines[i][lower_j:upper_j + 1])

total = 0
gear_to_part_numbers = {}
for i, line in enumerate(lines):
    part_numbers = re.split("\D+", line)
    start = 0
    for part_number in part_numbers:
        if part_number != "":
            j = line.index(part_number, start)
            start = j + len(part_number)
            lower_i = max(0, i - 1)
            upper_i = min(len(lines) - 1, i + 1)
            lower_j = max(0, j - 1)
            upper_j = min(len(line) - 1, j + len(part_number))

            schematic_box = schematic[lower_i:upper_i+1,lower_j:upper_j+1]
            if schematic_box.any():
                total += int(part_number)

            gear_box = gear[lower_i:upper_i+1,lower_j:upper_j+1]
            gears_relative_pos = list(zip(*np.where(gear_box)))
            for gear_relative_pos in gears_relative_pos:
                gear_absolute_pos = (gear_relative_pos[0] + lower_i, gear_relative_pos[1] + lower_j)
                if gear_absolute_pos not in gear_to_part_numbers:
                    gear_to_part_numbers[gear_absolute_pos] = set()
                gear_to_part_numbers[gear_absolute_pos].add(int(part_number))
            # print_box(lower_i, upper_i, lower_j, upper_j)
            # print(schematic_box.any())
            # print()

print("Part 1:", total)

sum_of_gear_ratios = 0
for gear_parts in gear_to_part_numbers.values():
    if len(gear_parts) == 2:
        gear_list = list(gear_parts)
        sum_of_gear_ratios += gear_list[0] * gear_list[1]

print("Part 2:", sum_of_gear_ratios)