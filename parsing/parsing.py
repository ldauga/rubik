ALL_MOVES = [
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


def verify_moves(moves_list):
    for move in moves_list:
        if move not in ALL_MOVES:
            return move
    return True
