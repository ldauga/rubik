import random
import sys
import time
import urllib.parse

from Class.rubik import Rubik
from parsing import verify_moves
from parsing.parsing import ALL_MOVES

if len(sys.argv) < 2:
    print("Need one param.")
    exit()
if len(sys.argv) > 2:
    print("Need only one param.")
    exit()

moves = urllib.parse.unquote(sys.argv[1]).split()

if (false_move := verify_moves(moves)) != True:
    print(f"Mix Param is not good. {false_move}")
    exit()


rubik = Rubik()
rubik.move_cube(moves, hide=True)

# rubik.move_cube(
#     [
#         "F",
#         "R",
#         "U",
#         "B",
#         "L",
#         "D",
#         "F",
#         "R",
#         "U",
#         "B",
#         "L",
#         "D",
#         "F'",
#         "R'",
#         "U'",
#         "B'",
#         "L'",
#         "D'",
#         "F",
#         "2F",
#         "2R",
#         "2U",
#         "2B",
#         "2L",
#         "2D",
#     ]
# )


rubik.move_cube(
    [
        # "U", # TOP LEFT CORNER WRONG PLACE POS TOP BOTTOM RIGHT
        # "2B",
        # "U'",
        # "R'",
        # "B",
        # "R",
        # "B",

        # "U", # TOP LEFT CORNER WRONG PLACE POS TOP BOTTOM RIGHT
        # "B",
        # "U'",
        # "B",

        # "L'",    # TOP LEFT CORNER GOOD PLACE WRONG ORIENTATION
        # "B'",
        # "L",
        # "B",
        # "L'",
        # "B'",
        # "L",


        # "U",
        # "B'",
        # "U'",
        # "L'",
    ]
)

rubik.set_solve_mode()

# rubik.display_cube()

# rubik.brute_force()

# rubik.display_cube()

# second_rubik = rubik.copy()

# second_rubik.move_cube('F')

# print(second_rubik == rubik)

# for move in ALL_MOVES:
#     tmp = rubik.copy()
#     tmp.move_cube(move)
#     print(tmp.is_in_g1())


rubik.thistlethwaite_solver()

# print("do_white_cross")
# rubik.do_white_cross()
# # print("do_good_white_cross")
# rubik.do_good_white_cross()
# # print("do_white_face")
# rubik.do_white_face()
# # print("do_white_first_crown")
# rubik.do_second_crown()
# print(f"FINISH {rubik.move_number}")



f = open("mean.txt", "a")
f.write(f"{rubik.move_number}\n")
f.close()

# time.sleep(0.2)

# rubik.F(dir="clockwise")
# rubik.D(dir="clockwise", number=2)
# rubik.D(dir="clockwise", number=2)
# rubik.L(dir="clockwise")
# rubik.D(dir="counter-clockwise")
# rubik.R(dir="clockwise")
# rubik.display_cube()

# while not rubik.is_solved():
#     rubik.B(dir="clockwise")
#     rubik.L(dir="clockwise")
#     rubik.F(dir="counter-clockwise")
#     rubik.R(dir="clockwise")
# rubik.move_cube(random.sample(moves_list, k=1))
# rubik.display_cube()
# rubik.U(dir="counter-clockwise")

# rubik.display_cube()
# rubik.set_center_face("left")
# rubik.display_cube()
# rubik.F(dir="clockwise")
# rubik.display_cube()
