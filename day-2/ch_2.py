#!/usr/bin/python3
"""
<https://adventofcode.com/2022/day/2> "Advent of Code - Day 2"

# Advent of Code 2022 --- Day 2

## Part Two

The Elf finishes helping with the tent aed sneaks back over to you. "Anyway,
the second column says how the round needs to end: `X` means you need to lose,
`Y` means you need to end the round in a draw, and `Z` means you need to win.
Good luck!"

The total score is still calculated in the same way, but now you need to figure
out what shape to choose so the round ends as indicated. The example above now
goes like this:

- In the first round, your opponent will choose Rock (`A`), and you need the
  round to end in a draw (`Y`), so you also choose Rock. This gives you a score
  of 1 + 3 = **4**.
- In the second round, your opponent will choose Paper (`B`), and you choose
  Rock so you lose (`X`) with a score of 1 + 0 = **1**.
- In the third round, you will defeat your opponent's Scissors with Rock for a
  score of 1 + 6 = **7**.

Now that you're correctly decrypting the ultra top secret strategy guide, you
would get a total score of **12**.

Following the Elf's instructions for the second column, **what would your total
score be if everything goes exactly according to your strategy guide?**
"""

import argparse
import re
import sys
from pathlib import Path

PAPER = "paper"
ROCK = "rock"
SCISSORS = "scissors"

DRAW = "draw"
LOSE = "lose"
WIN = "win"


def get_base_score(outcome):
    """Returns a score based on outcome or None

    Args:
        outcome (str): 'win', 'lose', or 'draw'

    Returns:
        6, 3, 0 or None
    """
    if outcome == WIN:
        return 6
    if outcome == DRAW:
        return 3
    if outcome == LOSE:
        return 0
    return None


def get_shape_score(shape):
    """Returns a score based on the input shape or None

    Args:
        shape (str): 'paper', 'scissors', or 'rock'

    Returns:
        3, 2, 1, or None
    """
    if shape == SCISSORS:
        return 3
    if shape == PAPER:
        return 2
    if shape == ROCK:
        return 1
    return None


def get_round_score(opponent_throw, outcome):
    """Returns score for the current round (set of throws)

    Args:
        opponent_throw (str): 'paper', 'scissors', or 'rock'
        outcome (str): 'win', 'lose', or 'draw'

    Returns:
        int: Total score for the current round
    """

    base_score = get_base_score(outcome)
    shape = get_required_throw(opponent_throw, outcome)
    shape_score = get_shape_score(shape)
    return base_score + shape_score


def get_total_score(rounds):
    """Returns total score tabulated from a list of rounds

    Args:
        rounds (list[list[str]]): A list of rounds (each a list of throws)

    Returns:
        int: Total score for the list of rounds
    """
    total_score = 0
    for single_round in rounds:
        opponent_throw, outcome = single_round
        round_score = get_round_score(opponent_throw, outcome)
        total_score += round_score
    return total_score


def get_losing_throw(throw):
    """Returns losing throw based on input throw or None

    Args:
        throw (str): 'paper', 'scissors', or 'rock'

    Returns:
        Losing throw ('paper', 'scissors', or 'rock') or None
    """
    if throw == PAPER:
        return ROCK
    if throw == ROCK:
        return SCISSORS
    if throw == SCISSORS:
        return PAPER
    return None


def get_required_throw(opponent_throw, outcome):
    """Returns the throw necessary to achieve the desired outcome

    Args:
        opponent_throw (str): 'paper', 'scissors', or 'rock'
        outcome: 'win', 'lose', or 'draw'

    Returns:
        str: 'paper', 'scissors', or 'rock' based on input
    """
    if outcome == DRAW:
        return opponent_throw
    loses = get_losing_throw(opponent_throw)
    if outcome == LOSE:
        return loses
    if outcome == WIN:
        return get_losing_throw(loses)
    return None


def translate(to_translate):
    """Translate input string to 'rock', 'paper', 'scissors', 'win', 'lose',
      'draw' or None

    Args:
        to_translate (str): String to translate

    Returns:
        str: 'rock', 'paper', 'scissors', 'win', 'lose', 'draw', or None based
          on input
    """
    switch = {
        'A': ROCK,
        'B': PAPER,
        'C': SCISSORS,
        'X': LOSE,
        'Y': DRAW,
        'Z': WIN
    }
    return switch.get(to_translate, None)


def translate_rounds(rounds_input):
    """Transforms a list of input rounds

    Args:
        rounds_input (list[list[str]]): A list of "encryped" round input

    Returns:
        list[list(str)]: A list of translated rounds
    """
    translated = []
    for round_input in rounds_input:
        opponent, required_outcome = round_input
        translated.append([translate(opponent), translate(required_outcome)])
    return translated


def read_input_file(file_path):
    """Reads from file and returns as a list of round data inputs

    Args:
        file_path (str): Path to input file

    Returns:
        list[list[str]]: A list of round data inputs
    """
    with Path(file_path).open(encoding='utf-8', mode='r') as file:
        lines = file.readlines()
        rounds = []
        for line in lines:
            if re.match("[ABC] [XYZ]", line):
                throw, encrypted_throw = line.strip().split(' ')
                rounds.append([throw, encrypted_throw])
        return rounds


def main():
    """Parses command line args and prints total score from file input"""
    parser = argparse.ArgumentParser(
        description="Rock Paper Scissor Score Counter",
    )
    parser.add_argument(
        "-f",
        "--file",
        help='path to "encrypted" input file',
        default="./input.txt",
    )
    args = parser.parse_args()

    if not Path(args.file).exists():
        parser.print_usage()
        sys.exit()

    rounds = read_input_file(args.file)
    translated = translate_rounds(rounds)
    total_score = get_total_score(translated)

    print(f"Total score: {total_score}")


if __name__ == '__main__':
    main()
