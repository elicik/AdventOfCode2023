import re
import copy

lines = []
with open("day01.txt") as input_file:
    lines = input_file.read().rstrip().split("\n")

# lines = [
# "1abc2",
# "pqr3stu8vwx",
# "a1b2c3d4e5f",
# "treb7uchet"
# ]

total = 0
for line in lines:
    first = None
    for char in line:
        if char.isdigit():
            last = char
            if first is None:
                first = last
    value = int(first + last)
    total += value

print("Part 1:", total)

# lines = [
# "two1nine",
# "eightwothree",
# "abcone2threexyz",
# "xtwone3four",
# "4nineeightseven2",
# "zoneight234",
# "7pqrstsixteen"
# ]

words = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
total = 0
for line in lines:
    first = None
    for i in range(len(line)):
        subline = line[i:]
        for index, word in enumerate(words, start=1):
            if subline.startswith(word):
                last = str(index)
                if first is None:
                    first = last
                break
        char = line[i]
        if char.isdigit():
            last = char
            if first is None:
                first = last

    value = int(first + last)
    total += value

print("Part 2:", total)