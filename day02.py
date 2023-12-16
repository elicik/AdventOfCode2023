import re
import copy
import math

lines = []
with open("day02.txt") as input_file:
    lines = input_file.read().rstrip().split("\n")

# lines = [
# "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
# "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
# "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
# "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
# "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"
# ]

bag = {
    "red": 12,
    "green": 13,
    "blue": 14
}

def subgame_possible(subgame):
    dice_by_color = subgame.split(",")
    for num_color_str in dice_by_color:
        arr = re.match(" (\d+) (\w+)", num_color_str)
        num, color = int(arr[1]), arr[2]
        if num > bag[color]:
            return False
    return True

def game_possible(subgames):
    for subgame in subgames:
        if not subgame_possible(subgame):
            return False
    return True

total = 0
for line in lines:
    arr = re.match("Game (\d+):(.+)", line)
    id, subgames = int(arr[1]), arr[2].split(";")
    if game_possible(subgames):
        total += id

print("Part 1:", total)

total = 0
for line in lines:
    arr = re.match("Game (\d+):(.+)", line)
    id, subgames = int(arr[1]), arr[2].split(";")
    min_cubes = {
        "blue": 0,
        "red": 0,
        "green": 0,
    }
    for subgame in subgames:
        dice_by_color = subgame.split(",")
        for num_color_str in dice_by_color:
            arr = re.match(" (\d+) (\w+)", num_color_str)
            num, color = int(arr[1]), arr[2]
            if num > min_cubes[color]:
                min_cubes[color] = num
    power = min_cubes["blue"] * min_cubes["red"] * min_cubes["green"]
    total += power
        

print("Part 2:", total)