import re
import copy
import math
import numpy as np
import functools
import itertools

lines = []
with open("day05.txt") as input_file:
    lines = input_file.read().rstrip().split("\n")

lines = [
"seeds: 79 14 55 13",
"",
"seed-to-soil map:",
"50 98 2",
"52 50 48",
"",
"soil-to-fertilizer map:",
"0 15 37",
"37 52 2",
"39 0 15",
"",
"fertilizer-to-water map:",
"49 53 8",
"0 11 42",
"42 0 7",
"57 7 4",
"",
"water-to-light map:",
"88 18 7",
"18 25 70",
"",
"light-to-temperature map:",
"45 77 23",
"81 45 19",
"68 64 13",
"",
"temperature-to-humidity map:",
"0 69 1",
"1 0 69",
"",
"humidity-to-location map:",
"60 56 37",
"56 93 4"
]

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
    destination, source, range_length = line.split()
    map[int(source)] = (int(range_length), int(destination))

@functools.lru_cache()
def convert_seed_to_soil(seed):
    return convert(seed, seed_to_soil)

@functools.lru_cache()
def convert_soil_to_fertilizer(soil):
    return convert(soil, soil_to_fertilizer)

@functools.lru_cache()
def convert_fertilizer_to_water(fertilizer):
    return convert(fertilizer, fertilizer_to_water)

@functools.lru_cache()
def convert_water_to_light(water):
    return convert(water, water_to_light)

@functools.lru_cache()
def convert_light_to_temperature(light):
    return convert(light, light_to_temperature)

@functools.lru_cache()
def convert_temperature_to_humidity(temperature):
    return convert(temperature, temperature_to_humidity)

@functools.lru_cache()
def convert_humidity_to_location(humidity):
    return convert(humidity, humidity_to_location)

def convert(source, map):
    found = False
    for source_start in sorted(list(map.keys()), reverse=True):
        if source_start <= source:
            found = True
            break
    if not found:
        return source
    range_length, destination = map[source_start]
    if source < source_start + range_length:
        return source - source_start + destination
    else:
        return source

@functools.lru_cache()
def convert_seed_to_location(seed):
    soil = convert_seed_to_soil(seed)
    fertilizer = convert_soil_to_fertilizer(soil)
    water = convert_fertilizer_to_water(fertilizer)
    light = convert_water_to_light(water)
    temperature = convert_light_to_temperature(light)
    humidity = convert_temperature_to_humidity(temperature)
    location = convert_humidity_to_location(humidity)
    # print(seed, soil, fertilizer, water, light, temperature, humidity, location)
    return location

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

min_location = math.inf
for seed in seeds:
    location = convert_seed_to_location(seed)
    if location < min_location:
        min_location = location

print("Part 1:", min_location)

all_seed_ranges = []
for i in range(len(seeds) // 2):
    start = seeds[2*i]
    range_length = seeds[2*i+1]
    end = start + range_length - 1
    all_seed_ranges.append((start, end))

all_seed_ranges.sort(key=lambda x: x[0])
new_seed_ranges = [all_seed_ranges[0]]

for seed_range in all_seed_ranges[1:]:
    last_seed_range = new_seed_ranges[-1]
    if seed_range[0] > last_seed_range[1]:
        new_seed_ranges.append(seed_range)
    elif seed_range[1] > last_seed_range[1]:
        # combine seed ranges
        new_seed_ranges[-1] = (last_seed_range[0], seed_range[1])
    # elif seed_range[1] <= last_seed_range[1]:
        # do nothing

# print(new_seed_ranges)

min_location = math.inf
for seed_range in new_seed_ranges:
    for seed in range(seed_range[0], seed_range[1] + 1):
        location = convert_seed_to_location(seed)
        if location < min_location:
            min_location = location

print("Part 2:", min_location)