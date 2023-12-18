import re
import copy
import math
import numpy as np
import functools
import itertools

lines = []
with open("day05.txt") as input_file:
    lines = input_file.read().rstrip().split("\n")

# lines = [
# "seeds: 79 14 55 13",
# "",
# "seed-to-soil map:",
# "50 98 2",
# "52 50 48",
# "",
# "soil-to-fertilizer map:",
# "0 15 37",
# "37 52 2",
# "39 0 15",
# "",
# "fertilizer-to-water map:",
# "49 53 8",
# "0 11 42",
# "42 0 7",
# "57 7 4",
# "",
# "water-to-light map:",
# "88 18 7",
# "18 25 70",
# "",
# "light-to-temperature map:",
# "45 77 23",
# "81 45 19",
# "68 64 13",
# "",
# "temperature-to-humidity map:",
# "0 69 1",
# "1 0 69",
# "",
# "humidity-to-location map:",
# "60 56 37",
# "56 93 4"
# ]

step = 1
seeds = []

# Convert to maps of format source range start -> (range length, destination range start)
seed_to_soil = {}
soil_to_fertilizer = {}
fertilizer_to_water = {}
water_to_light = {}
light_to_temperature = {}
temperature_to_humidity = {}
humidity_to_location = {}

def insert_into_map(line, map):
    destination, start, range_length = line.split()
    map[int(start)] = (int(start), int(range_length), int(destination))

def convert(source, map):
    found = False
    for source_start in sorted(list(map.keys()), reverse=True):
        if source_start <= source:
            found = True
            break
    if not found:
        return source
    _, range_length, destination = map[source_start]
    if source < source_start + range_length:
        return source - source_start + destination
    else:
        return source

def combine_maps(first_map, second_map):
    first_ranges_by_start = sorted(list(first_map.values()), key=lambda x: x[0])
    first_ranges_by_destination = sorted(list(first_map.values()), key=lambda x: x[2])
    second_ranges = sorted(list(second_map.values()), key=lambda x: x[0])
    new_map = {}
    for first_range in first_ranges_by_destination:
        first_start, first_range_length, first_destination = first_range
        for second_range in second_ranges:
            second_start, second_range_length, second_destination = second_range
            # range is too early
            if second_start + second_range_length < first_destination:
                continue
            # range is too late
            if second_start >= first_destination + first_range_length:
                break

            overlap_start = max([first_destination, second_start])
            overlap_end = min([first_destination + first_range_length, second_start + second_range_length])
            overlap_range_length = overlap_end - overlap_start
            if overlap_range_length == 0:
                continue
            new_start = first_start + (overlap_start - first_destination)
            new_destination = (second_destination - second_start) + (first_destination - first_start) + new_start
            new_map[new_start] = (new_start, overlap_range_length, new_destination)

    return new_map

def fill_map(map):
    ranges = sorted(list(map.values()), key=lambda x: x[0])
    # Check that first range has a source of 0
    if ranges[0][0] != 0:
        map[0] = (0, ranges[0][0], 0)
    # Check that last range has a range length of inf
    if ranges[-1][1] != math.inf:
        new_start = ranges[-1][0] + ranges[-1][1]
        map[new_start] = (new_start, math.inf, new_start)
    
    ranges = sorted(list(map.values()), key=lambda x: x[0])
    for i in range(len(ranges) - 1):
        curr_end = ranges[i][0] + ranges[i][1]
        next_start = ranges[i+1][0]
        if curr_end != next_start:
            new_start = curr_end
            new_range_length = next_start - curr_end
            map[new_start] = (new_start, new_range_length, new_start)

for line in lines:
    if line == "":
        step += 1
        continue
    if "map" in line:
        continue
    if step == 1:
        seeds = [int(x) for x in re.match("seeds: (.*)", line)[1].split()]
    if step == 2:
        insert_into_map(line, seed_to_soil)
    if step == 3:
        insert_into_map(line, soil_to_fertilizer)
    if step == 4:
        insert_into_map(line, fertilizer_to_water)
    if step == 5:
        insert_into_map(line, water_to_light)
    if step == 6:
        insert_into_map(line, light_to_temperature)
    if step == 7:
        insert_into_map(line, temperature_to_humidity)
    if step == 8:
        insert_into_map(line, humidity_to_location)

fill_map(seed_to_soil)
fill_map(soil_to_fertilizer)
fill_map(fertilizer_to_water)
fill_map(water_to_light)
fill_map(light_to_temperature)
fill_map(temperature_to_humidity)
fill_map(humidity_to_location)

seedrange_map = {}
for seed in seeds:
    seedrange_map[seed] = (seed, 1, seed)

seedrange_to_soil = combine_maps(seedrange_map, seed_to_soil)
seedrange_to_fertilizer = combine_maps(seedrange_to_soil, soil_to_fertilizer)
seedrange_to_water = combine_maps(seedrange_to_fertilizer, fertilizer_to_water)
seedrange_to_light = combine_maps(seedrange_to_water, water_to_light)
seedrange_to_temperature = combine_maps(seedrange_to_light, light_to_temperature)
seedrange_to_humidity = combine_maps(seedrange_to_temperature, temperature_to_humidity)
seedrange_to_location = combine_maps(seedrange_to_humidity, humidity_to_location)

print("Part 1:", min([x[2] for x in seedrange_to_location.values()]))

seedrange_map = {}
for i in range(len(seeds) // 2):
    start = seeds[2*i]
    range_length = seeds[2*i+1]
    seedrange_map[start] = (start, range_length, start)

seedrange_to_soil = combine_maps(seedrange_map, seed_to_soil)
seedrange_to_fertilizer = combine_maps(seedrange_to_soil, soil_to_fertilizer)
seedrange_to_water = combine_maps(seedrange_to_fertilizer, fertilizer_to_water)
seedrange_to_light = combine_maps(seedrange_to_water, water_to_light)
seedrange_to_temperature = combine_maps(seedrange_to_light, light_to_temperature)
seedrange_to_humidity = combine_maps(seedrange_to_temperature, temperature_to_humidity)
seedrange_to_location = combine_maps(seedrange_to_humidity, humidity_to_location)

print("Part 2:", min([x[2] for x in seedrange_to_location.values()]))