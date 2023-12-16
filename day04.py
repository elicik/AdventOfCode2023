import re
import copy
import math
import numpy as np

lines = []
with open("day04.txt") as input_file:
    lines = input_file.read().rstrip().split("\n")

# lines = [
# "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
# "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19",
# "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1",
# "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83",
# "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36",
# "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"
# ]

total = 0

num_matches_by_card = []

for line in lines:
    arr = re.match("Card\s+(\d+):\s+([\d ]+)\s+\|\s+([\d ]+)", line)
    card_num, winning_str, mine_str = arr[1], arr[2], arr[3]
    winning_nums = [int(x) for x in winning_str.split()]
    mine_nums = [int(x) for x in mine_str.split()]
    winning_nums.sort()
    mine_nums.sort()

    # Quickly compute number of matches
    winning_index = 0
    mine_index = 0
    num_matches = 0
    while winning_index < len(winning_nums) and mine_index < len(mine_nums):
        winning = winning_nums[winning_index]
        mine = mine_nums[mine_index]
        if winning == mine:
            num_matches += 1
            winning_index += 1
            mine_index += 1
        elif winning < mine:
            winning_index += 1
        else:
            mine_index += 1
    num_matches_by_card.append(num_matches)
    if num_matches > 0:
        total += 2 ** (num_matches - 1)

print("Part 1:", total)

num_copies_per_card = len(lines) * [1]

for card_num in range(len(lines)):
    for i in range(num_matches_by_card[card_num]):
        num_copies_per_card[card_num + i + 1] += num_copies_per_card[card_num]

total_copies = sum(num_copies_per_card)

print("Part 2:", total_copies)