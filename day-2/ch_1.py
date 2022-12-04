#!/usr/bin/python3
"""
<https://adventofcode.com/2022/day/2> "Advent of Code - Day 2"

# Advent of Code 2022 --- Day 1

## Rock Paper Scissors

The Elves begin to set up camp on the beach. To decide whose tent gets to be
closest to the snack storage, a giant **Rock Paper Scissors** tournament is
already in progress.

Rock Paper Scissors is a game between two players. Each game contains many
rounds; in each round, the players each simultaneously choose one of Rock,
Paper, or Scissors using a hand shape. Then, a winner for that round is
selected: Rock defeats Scissors, Scissors defeats Paper, and Paper defeats
Rock. If both players choose the same shape, the round instead ends in a draw.

Appreciative of your help yesterday, one Elf gives you an **encrypted strategy
guide** (your puzzle input) that they say will be sure to help you win. "The
first column is what your opponent is going to play: `A` for Rock, `B` for
Paper, and `C` for Scissors. The second column--" Suddenly, the Elf is called
away to help with someone's tent.

The second column, you reason, must be what you should play in response: `X`
for Rock, `Y` for Paper, and `Z` for Scissors. Winning every time would be
suspicious, so the responses must have been carefully chosen.

The winner of the whole tournament is the player with the highest score. Your
**total score** is the sum of your scores for each round. The score for a
single round is the score for the **shape you selected** (1 for Rock, 2 for
Paper, and 3 for Scissors) plus the score for the **outcome of the round** (0
if you lost, 3 if the round was a draw, and 6 if you won).

Since you can't be sure if the Elf is trying to help you or trick you, you
should calculate the score you would get if you were to follow the strategy
guide.

For example, suppose you were given the following strategy guide:

```
A Y
B X
C Z
```

This strategy guide predicts and recommends the following:

- In the first round, your opponent will choose Rock (`A`), and you should
  choose Paper (`Y`). This ends in a win for you with a score of **8** (2
  because you chose Paper + 6 because you won).
- In the second round, your opponent will choose Paper (`B`), and you should
  choose Rock (`X`). This ends in a loss for you with a score of **1** (1 + 0).
- The third round is a draw with both players choosing Scissors, giving you a
  score of 3 + 3 = **6**.

In this example, if you were to follow the strategy guide, you would get a
total score of **15** (8 + 1 + 6).

**What would your total score be if everything goes exactly according to your
strategy guide?**
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


def get_round_score(opponent_throw, throw):
    """Returns score for the current round (set of throws)

    Args:
        opponent_throw (str): 'paper', 'scissors', or 'rock'
        throw (str): 'paper', 'scissors', or 'rock'

    Returns:
        int: Total score for the current round
    """
    outcome = rock_paper_scissors(throw, opponent_throw)
    base_score = get_base_score(outcome)
    shape_score = get_shape_score(throw)
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
        opponent_throw, throw = single_round
        round_score = get_round_score(opponent_throw, throw)
        total_score += round_score
    return total_score


def rock_paper_scissors(throw, counter):
    """Returns the outcome of a game of ROCK-PAPER-SCISSORS

    Args:
        throw (str): the opponent's throw (one of 'paper', 'scissors', or
          'rock')
        counter (str): the counter-throw (one of 'paper', 'scissors', or
          'rock')

    Returns:
        str: 'win', 'lose', or 'draw' based on the input
    """
    if throw == counter:
        return DRAW

    losing_throw = get_losing_throw(counter)
    if throw == losing_throw:
        return LOSE

    winning_throw = get_losing_throw(losing_throw)
    if throw == winning_throw:
        return WIN
    return None


def translate(to_translate):
    """Translate input string to 'rock', 'paper', 'scissors', or None

    Args:
        to_translate (str): String to translate

    Returns:
        str: 'rock', 'paper', 'scissors', or None based on input
    """
    if to_translate in ('A', 'X'):
        return ROCK
    if to_translate in ('B', 'Y'):
        return PAPER
    if to_translate in ('C', 'Z'):
        return SCISSORS
    return None


def translate_rounds(rounds_input):
    """Transforms a list of input rounds

    Args:
        rounds_input (list[list[str]]): A list of "encryped" round input

    Returns:
        list[list(str)]: A list of translated rounds
    """
    translated = []
    for round_input in rounds_input:
        opponent, throw = round_input
        translated.append([translate(opponent), translate(throw)])
    return translated


def read_input_file(file_path):
    """Reads from file and returns as a list of round data inputs

    Args:
        file_path (str): Path to input file

    Returns:
        list[list[str]]: A list of round data inputs
    """
    with Path(file_path).open(mode='r', encoding='utf-8') as file:
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

    print(f"Total score: {total_score}") # 11449


if __name__ == '__main__':
    main()
