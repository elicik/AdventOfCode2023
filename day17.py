import re
import copy
import math
import numpy as np
import functools
import itertools
import queue

lines = []
with open("day17.txt") as input_file:
    lines = input_file.read().rstrip().split("\n")

lines = [
"2413432311323",
"3215453535623",
"3255245654254",
"3446585845452",
"4546657867536",
"1438598798454",
"4457876987766",
"3637877979653",
"4654967986887",
"4564679986453",
"1224686865563",
"2546548887735",
"4322674655533"
]

grid = np.zeros((len(lines), len(lines[0])), np.ubyte)

for i, line in enumerate(lines):
    for j, char in enumerate(line):
        grid[i, j] = char

def reconstruct_path(came_from, curr):
    total_path = [curr]
    while curr in came_from:
        curr = came_from[curr]
        total_path.append(curr)
    return reversed(total_path)

def three_in_a_row(came_from, node):
    # todo
    # if 

def heuristic(node, goal):
    return np.sum(np.abs(np.array(goal) - np.array(node)))

def a_star(start, goal):
    open_set = queue.PriorityQueue()
    open_set.put(heuristic(start, goal), start)

    came_from = {}
    g = { start: 0 }

    while open_set:
        curr = open_set.get()
        if curr == goal:
            return reconstruct_path(came_from, curr)
        neighbors = []
        if curr[0] != 0:
            neighbors.append((curr[0]))
            # todo