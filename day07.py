import re
import copy
import math
import numpy as np
import functools
import itertools

lines = []
with open("day07.txt") as input_file:
    lines = input_file.read().rstrip().split("\n")

# lines = [
# "32T3K 765",
# "T55J5 684",
# "KK677 28",
# "KTJJT 220",
# "QQQJA 483"
# ]

card_types_p1 = ["2","3","4","5","6","7","8","9","T","J","Q","K","A"]  
card_types_p2 = ["J", "2","3","4","5","6","7","8","9","T","Q","K","A"]  
hand_types = ["high card", "one pair", "two pairs", "three of a kind", "full house", "four of a kind", "five of a kind"]

def get_hand_type_p1(hand):
    # Determine card type
    distribution = {card_type : 0 for card_type in card_types_p1}
    for card in hand:
        distribution[card] += 1
    distribution_values = list(distribution.values())
    if 5 in distribution_values:
        hand_type = "five of a kind"
    elif 4 in distribution_values:
        hand_type = "four of a kind"
    elif 3 in distribution_values:
        if 2 in distribution_values:
            hand_type = "full house"
        else:
            hand_type = "three of a kind"
    elif 2 in distribution_values:
        if distribution_values.count(2) == 2:
            hand_type = "two pairs"
        else:
            hand_type = "one pair"
    else:
        hand_type = "high card"
    
    return hand_type

def get_hand_type_p2(hand):
    # Determine card type
    distribution = {card_type : 0 for card_type in card_types_p1}
    for card in hand:
        distribution[card] += 1
    jokers = distribution["J"]
    del distribution["J"]
    distribution_values = list(distribution.values())
    max_value = max(distribution_values)

    if max_value + jokers == 5:
        hand_type = "five of a kind"
    elif max_value + jokers == 4:
        hand_type = "four of a kind"
    elif max_value + jokers == 3:
        if jokers == 2:
            hand_type = "three of a kind"
        elif jokers == 1:
            if distribution_values.count(2) == 2:
                hand_type = "full house"
            else:
                hand_type = "three of a kind"
        elif 2 in distribution_values:
            hand_type = "full house"
        else:
            hand_type = "three of a kind"
    elif jokers == 1:
        hand_type = "one pair"
    elif 2 in distribution_values:
        if distribution_values.count(2) == 2:
            hand_type = "two pairs"
        else:
            hand_type = "one pair"
    else:
        hand_type = "high card"
    
    return hand_type

def compare_hands_p1(hand1, hand2):
    if hand1["type_p1"] == hand2["type_p1"]:
        for card1, card2 in zip(hand1["hand"], hand2["hand"]):
            if card1 != card2:
                card1_index = card_types_p1.index(card1)
                card2_index = card_types_p1.index(card2)
                return card1_index - card2_index
    else:
        type1_index = hand_types.index(hand1["type_p1"])
        type2_index = hand_types.index(hand2["type_p1"])
        return type1_index - type2_index

def compare_hands_p2(hand1, hand2):
    if hand1["type_p2"] == hand2["type_p2"]:
        for card1, card2 in zip(hand1["hand"], hand2["hand"]):
            if card1 != card2:
                card1_index = card_types_p2.index(card1)
                card2_index = card_types_p2.index(card2)
                return card1_index - card2_index
    else:
        type1_index = hand_types.index(hand1["type_p2"])
        type2_index = hand_types.index(hand2["type_p2"])
        return type1_index - type2_index

hands = []
for line in lines:
    hand_str, bid_str = line.split()

    hand = {
        "hand": hand_str,
        "type_p1": get_hand_type_p1(hand_str),
        "type_p2": get_hand_type_p2(hand_str),
        "bid": int(bid_str),
    }

    hands.append(hand)

hands.sort(key=functools.cmp_to_key(compare_hands_p1))

total = 0
for rank, hand in enumerate(hands, start=1):
    total += hand["bid"] * rank

print("Part 1:", total)

hands.sort(key=functools.cmp_to_key(compare_hands_p2))

total = 0
for rank, hand in enumerate(hands, start=1):
    total += hand["bid"] * rank

print("Part 2:", total)