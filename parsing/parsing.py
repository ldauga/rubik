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
    "2F",
    "2R",
    "2U",
    "2B",
    "2L",
    "2D",
    "f",
    "r",
    "u",
    "b",
    "l",
    "d",
    "f'",
    "r'",
    "u'",
    "b'",
    "l'",
    "d'",
    "2f",
    "2r",
    "2u",
    "2b",
    "2l",
    "2d",
]


def verify_moves(moves_list):
    for move in moves_list:
        if move not in ALL_MOVES:
            return move
    return True
