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
    "F2",
    "R2",
    "U2",
    "B2",
    "L2",
    "D2",
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
