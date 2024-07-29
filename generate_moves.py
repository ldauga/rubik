import subprocess
import urllib.parse
import random
import sys

# Define the list of possible moves
moves = [
    "F",
    "R",
    "U",
    "B",
    "L",
    "D",
    "F'",
    "R'",
    "U'",
    "B'",
    "L'",
    "D'",
    "2F",
    "2R",
    "2U",
    "2B",
    "2L",
    "2D",
]


def generate_moves(n):
    return


if len(sys.argv) < 2:
    print("Need one param.")
    exit()
if len(sys.argv) > 2:
    print("Need only one param.")
    exit()

subprocess.run(
    [
        "python3",
        "rubik.py",
        urllib.parse.quote(" ".join(random.choices(moves, k=int(sys.argv[1])))),
    ]
)
