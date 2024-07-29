import time
from typing import List, Literal, Union
from Class.face import Face
from parsing.parsing import ALL_MOVES


RED = 0
BLUE = 1
WHITE = 2
GREEN = 3
YELLOW = 4
ORANGE = 5

"""
	   #######
	   #     #
	   # R 0 #
	   #     #
	   #######
#####################
#     ##     ##     #
# B 1 ## W 2 ## G 3 #
#     ##     ##     #
#####################
       #######
       #     #
       # O 5 #
       #     #
       #######
	   #######
	   #     #
	   # Y 4 #
	   #     #
	   #######
"""


class Rubik:

    mode: Union[Literal["mix"], Literal["solve"]] = "mix"

    move_number = 0

    center_face: Face
    faces: dict

    def __init__(self):
        self.faces = {
            "front": Face(WHITE),
            "back": Face(YELLOW),
            "left": Face(BLUE),
            "right": Face(GREEN),
            "up": Face(RED),
            "down": Face(ORANGE),
        }

        self.center_face = self.faces["front"]

    def set_solve_mode(self):
        self.mode = "solve"

    def is_solved(self):
        for pos in self.faces:
            if not self.faces[pos].is_solved():
                return False
        return True

    def set_center_face(self, face_name):
        if face_name in self.faces:
            self.center_face = self.faces[face_name]
        else:
            raise ValueError(f"No face named {face_name} in the cube.")

    def get_up(self) -> Face:
        if self.center_face == self.faces["front"]:
            return self.faces["up"]
        elif self.center_face == self.faces["back"]:
            return self.faces["up"]
        elif self.center_face == self.faces["left"]:
            return self.faces["up"]
        elif self.center_face == self.faces["right"]:
            return self.faces["up"]
        elif self.center_face == self.faces["up"]:
            return self.faces["back"]
        elif self.center_face == self.faces["down"]:
            return self.faces["front"]

    def get_down(self) -> Face:
        if self.center_face == self.faces["front"]:
            return self.faces["down"]
        elif self.center_face == self.faces["back"]:
            return self.faces["down"]
        elif self.center_face == self.faces["left"]:
            return self.faces["down"]
        elif self.center_face == self.faces["right"]:
            return self.faces["down"]
        elif self.center_face == self.faces["up"]:
            return self.faces["front"]
        elif self.center_face == self.faces["down"]:
            return self.faces["back"]

    def get_left(self) -> Face:
        if self.center_face == self.faces["front"]:
            return self.faces["left"]
        elif self.center_face == self.faces["back"]:
            return self.faces["right"]
        elif self.center_face == self.faces["left"]:
            return self.faces["back"]
        elif self.center_face == self.faces["right"]:
            return self.faces["front"]
        elif self.center_face == self.faces["up"]:
            return self.faces["left"]
        elif self.center_face == self.faces["down"]:
            return self.faces["left"]

    def get_right(self) -> Face:
        if self.center_face == self.faces["front"]:
            return self.faces["right"]
        elif self.center_face == self.faces["back"]:
            return self.faces["left"]
        elif self.center_face == self.faces["left"]:
            return self.faces["front"]
        elif self.center_face == self.faces["right"]:
            return self.faces["back"]
        elif self.center_face == self.faces["up"]:
            return self.faces["right"]
        elif self.center_face == self.faces["down"]:
            return self.faces["right"]

    def get_face_by_center(self, center_color) -> Face:
        face = next(
            (
                self.faces[pos]
                for pos in self.faces
                if self.faces[pos].center_color == center_color
            )
        )
        return face

    def row_to_string(self, row):

        color_string = {
            "reset": "\033[0m",
            RED: "\033[91m",
            BLUE: "\033[94m",
            WHITE: "\033[97m",
            GREEN: "\033[92m",
            YELLOW: "\033[93m",
            ORANGE: "\033[95m",
        }

        string = ""

        for value in row:
            string += color_string[value] + "█"
        string += color_string["reset"]

        return string

    def display_cube(self):

        face_up = self.get_up()
        face_down = self.get_down()
        face_left = self.get_left()
        face_right = self.get_right()
        face_front = self.center_face
        face_back = next(
            (
                self.faces[pos]
                for pos in self.faces
                if self.faces[pos]
                not in [
                    face_up,
                    face_down,
                    face_left,
                    face_right,
                    face_front,
                ]
            )
        )

        for i in range(3):
            print("   " + self.row_to_string(face_up.grid[i]))
        for i in range(3):
            print(
                self.row_to_string(face_left.grid[i])
                + self.row_to_string(face_front.grid[i])
                + self.row_to_string(face_right.grid[i])
            )
        for i in range(3):
            print("   " + self.row_to_string(face_down.grid[i]))
        for i in range(3):
            print("   " + self.row_to_string(face_back.grid[i]))

        print()

    def F(
        self,
        dir: Union[Literal["clockwise"], Literal["counter-clockwise"]] = "clockwise",
        number: int = 1,
    ):
        left_face = self.get_left()
        up_face = self.get_up()
        down_face = self.get_down()
        right_face = self.get_right()

        for _ in range(number):
            if dir == "clockwise":
                temp_left = []
                for i in range(3):
                    temp_left.append(left_face.grid[i][2])

                temp_up = [up_face.grid[2][2 - i] for i in range(3)]
                for i in range(3):
                    up_face.grid[2][2 - i] = temp_left[i]

                temp_right = []
                for i in range(3):
                    temp_right.append(right_face.grid[2 - i][0])
                    right_face.grid[2 - i][0] = temp_up[i]

                temp_down = [down_face.grid[0][i] for i in range(3)]
                for i in range(3):
                    down_face.grid[0][i] = temp_right[i]

                for i in range(3):
                    left_face.grid[i][2] = temp_down[i]

                self.center_face.grid = [
                    list(row) for row in zip(*self.center_face.grid[::-1])
                ]
            else:
                temp_left = []
                for i in range(3):
                    temp_left.append(left_face.grid[i][2])

                temp_down = [down_face.grid[0][i] for i in range(3)]
                for i in range(3):
                    down_face.grid[0][i] = temp_left[i]

                temp_right = []
                for i in range(3):
                    temp_right.append(right_face.grid[2 - i][0])
                    right_face.grid[2 - i][0] = temp_down[i]

                temp_up = [up_face.grid[2][2 - i] for i in range(3)]
                for i in range(3):
                    up_face.grid[2][2 - i] = temp_right[i]

                for i in range(3):
                    left_face.grid[i][2] = temp_up[i]

                self.center_face.grid = [
                    list(row) for row in zip(*self.center_face.grid)
                ][::-1]

    def R(
        self,
        dir: Union[Literal["clockwise"], Literal["counter-clockwise"]] = "clockwise",
        number: int = 1,
    ):
        face_up = self.get_up()
        face_down = self.get_down()
        face_left = self.get_left()
        face_right = self.get_right()
        face_front = self.center_face
        face_back = next(
            (
                self.faces[pos]
                for pos in self.faces
                if self.faces[pos]
                not in [
                    face_up,
                    face_down,
                    face_left,
                    face_right,
                    face_front,
                ]
            )
        )

        for _ in range(number):
            if dir == "clockwise":
                temp_front = [face_front.grid[i][2] for i in range(3)]

                temp_up = [face_up.grid[i][2] for i in range(3)]
                for i in range(3):
                    face_up.grid[i][2] = temp_front[i]

                temp_back = [face_back.grid[i][2] for i in range(3)]
                for i in range(3):
                    face_back.grid[i][2] = temp_up[i]

                temp_down = [face_down.grid[i][2] for i in range(3)]
                for i in range(3):
                    face_down.grid[i][2] = temp_back[i]

                for i in range(3):
                    face_front.grid[i][2] = temp_down[i]

                face_right.grid = [list(row) for row in zip(*face_right.grid[::-1])]
            else:
                temp_front = [face_front.grid[i][2] for i in range(3)]

                temp_down = [face_down.grid[i][2] for i in range(3)]
                for i in range(3):
                    face_down.grid[i][2] = temp_front[i]

                temp_back = [face_back.grid[i][2] for i in range(3)]
                for i in range(3):
                    face_back.grid[i][2] = temp_down[i]

                temp_up = [face_up.grid[i][2] for i in range(3)]
                for i in range(3):
                    face_up.grid[i][2] = temp_back[i]

                for i in range(3):
                    face_front.grid[i][2] = temp_up[i]

                face_right.grid = [list(row) for row in zip(*face_right.grid)][::-1]

    def U(
        self,
        dir: Union[Literal["clockwise"], Literal["counter-clockwise"]] = "clockwise",
        number: int = 1,
    ):
        face_up = self.get_up()
        face_down = self.get_down()
        face_left = self.get_left()
        face_right = self.get_right()
        face_front = self.center_face
        face_back = next(
            (
                self.faces[pos]
                for pos in self.faces
                if self.faces[pos]
                not in [
                    face_up,
                    face_down,
                    face_left,
                    face_right,
                    face_front,
                ]
            )
        )

        for _ in range(number):
            if dir == "clockwise":
                temp_front = face_front.grid[0]

                temp_left = face_left.grid[0]
                face_left.grid[0] = temp_front

                temp_back = [face_back.grid[2][2 - i] for i in range(3)]
                for i in range(3):
                    face_back.grid[2][2 - i] = temp_left[i]

                temp_right = face_right.grid[0]
                face_right.grid[0] = temp_back

                face_front.grid[0] = temp_right

                face_up.grid = [list(row) for row in zip(*face_up.grid[::-1])]
            else:
                temp_front = face_front.grid[0]

                temp_right = face_right.grid[0]
                face_right.grid[0] = temp_front

                temp_back = [face_back.grid[2][2 - i] for i in range(3)]
                for i in range(3):
                    face_back.grid[2][2 - i] = temp_right[i]

                temp_left = face_left.grid[0]
                face_left.grid[0] = temp_back

                face_front.grid[0] = temp_left

                face_up.grid = [list(row) for row in zip(*face_up.grid)][::-1]

    def B(
        self,
        dir: Union[Literal["clockwise"], Literal["counter-clockwise"]] = "clockwise",
        number: int = 1,
    ):
        face_up = self.get_up()
        face_down = self.get_down()
        face_left = self.get_left()
        face_right = self.get_right()
        face_front = self.center_face
        face_back = next(
            (
                self.faces[pos]
                for pos in self.faces
                if self.faces[pos]
                not in [
                    face_up,
                    face_down,
                    face_left,
                    face_right,
                    face_front,
                ]
            )
        )

        for _ in range(number):
            if dir == "clockwise":
                temp_up = face_up.grid[0]

                temp_right = [face_right.grid[i][2] for i in range(3)]
                for i in range(3):
                    face_right.grid[i][2] = temp_up[i]

                temp_down = [face_down.grid[2][2 - i] for i in range(3)]
                for i in range(3):
                    face_down.grid[2][2 - i] = temp_right[i]

                temp_left = [face_left.grid[2 - i][0] for i in range(3)]
                for i in range(3):
                    face_left.grid[2 - i][0] = temp_down[i]

                face_up.grid[0] = temp_left

                face_back.grid = [list(row) for row in zip(*face_back.grid)][::-1]
            else:
                temp_up = face_up.grid[0]

                temp_left = [face_left.grid[2 - i][0] for i in range(3)]
                for i in range(3):
                    face_left.grid[2 - i][0] = temp_up[i]

                temp_down = [face_down.grid[2][2 - i] for i in range(3)]
                for i in range(3):
                    face_down.grid[2][2 - i] = temp_left[i]

                temp_right = [face_right.grid[i][2] for i in range(3)]
                for i in range(3):
                    face_right.grid[i][2] = temp_down[i]

                face_up.grid[0] = temp_right

                face_back.grid = [list(row) for row in zip(*face_back.grid[::-1])]

    def L(
        self,
        dir: Union[Literal["clockwise"], Literal["counter-clockwise"]] = "clockwise",
        number: int = 1,
    ):
        face_up = self.get_up()
        face_down = self.get_down()
        face_left = self.get_left()
        face_right = self.get_right()
        face_front = self.center_face
        face_back = next(
            (
                self.faces[pos]
                for pos in self.faces
                if self.faces[pos]
                not in [
                    face_up,
                    face_down,
                    face_left,
                    face_right,
                    face_front,
                ]
            )
        )

        for _ in range(number):
            if dir == "clockwise":
                temp_front = [face_front.grid[i][0] for i in range(3)]

                temp_down = [face_down.grid[i][0] for i in range(3)]
                for i in range(3):
                    face_down.grid[i][0] = temp_front[i]

                temp_back = [face_back.grid[i][0] for i in range(3)]
                for i in range(3):
                    face_back.grid[i][0] = temp_down[i]

                temp_up = [face_up.grid[i][0] for i in range(3)]
                for i in range(3):
                    face_up.grid[i][0] = temp_back[i]

                for i in range(3):
                    face_front.grid[i][0] = temp_up[i]

                face_left.grid = [list(row) for row in zip(*face_left.grid[::-1])]
            else:
                temp_front = [face_front.grid[i][0] for i in range(3)]

                temp_up = [face_up.grid[i][0] for i in range(3)]
                for i in range(3):
                    face_up.grid[i][0] = temp_front[i]

                temp_back = [face_back.grid[i][0] for i in range(3)]
                for i in range(3):
                    face_back.grid[i][0] = temp_up[i]

                temp_down = [face_down.grid[i][0] for i in range(3)]
                for i in range(3):
                    face_down.grid[i][0] = temp_back[i]

                for i in range(3):
                    face_front.grid[i][0] = temp_down[i]

                face_left.grid = [list(row) for row in zip(*face_left.grid)][::-1]

    def D(
        self,
        dir: Union[Literal["clockwise"], Literal["counter-clockwise"]] = "clockwise",
        number: int = 1,
    ):
        face_up = self.get_up()
        face_down = self.get_down()
        face_left = self.get_left()
        face_right = self.get_right()
        face_front = self.center_face
        face_back = next(
            (
                self.faces[pos]
                for pos in self.faces
                if self.faces[pos]
                not in [
                    face_up,
                    face_down,
                    face_left,
                    face_right,
                    face_front,
                ]
            )
        )

        for _ in range(number):
            if dir == "clockwise":
                temp_front = face_front.grid[2]

                temp_right = face_right.grid[2]
                face_right.grid[2] = temp_front

                temp_back = [face_back.grid[0][2 - i] for i in range(3)]
                for i in range(3):
                    face_back.grid[0][2 - i] = temp_right[i]

                temp_left = face_left.grid[2]
                face_left.grid[2] = temp_back

                face_front.grid[2] = temp_left

                face_down.grid = [list(row) for row in zip(*face_down.grid[::-1])]
            else:
                temp_front = face_front.grid[2]

                temp_left = face_left.grid[2]
                face_left.grid[2] = temp_front

                temp_back = [face_back.grid[0][2 - i] for i in range(3)]
                for i in range(3):
                    face_back.grid[0][2 - i] = temp_left[i]

                temp_right = face_right.grid[2]
                face_right.grid[2] = temp_back

                face_front.grid[2] = temp_right

                face_down.grid = [list(row) for row in zip(*face_down.grid)][::-1]

    def move_cube(self, moves, hide=False):
        if isinstance(moves, str):
            moves = [moves]

        moves_list = {
            "F": self.F,
            "R": self.R,
            "U": self.U,
            "B": self.B,
            "L": self.L,
            "D": self.D,
        }

        for move in moves:
            initial_move = move

            number = 1
            dir = "clockwise"

            if move[0] == "2":
                number = 2
                move = move[1:]

            if "'" in move:
                dir = "counter-clockwise"

            moves_list[move[0]](dir=dir, number=number)

            if self.mode == "solve":
                self.move_number += 1

            if not hide:
                print(f"MOVE: {initial_move}")
                self.display_cube()
            # time.sleep(1)

    def do_white_cross(self):

        while not all(
            [
                self.center_face.grid[0][1] == WHITE,  # UP
                self.center_face.grid[1][2] == WHITE,  # RIGHT
                self.center_face.grid[2][1] == WHITE,  # DOWN
                self.center_face.grid[1][0] == WHITE,  # LEFT
            ]
        ):
            stop = False

            moves = []

            left_face = self.get_left()

            if left_face.grid[0][1] == WHITE:  # UP
                if not self.center_face.grid[1][0] == WHITE:  # LEFT
                    moves.append("F")
                elif not self.center_face.grid[1][2] == WHITE:  # RIGHT
                    moves.append("F'")
                elif not self.center_face.grid[2][1] == WHITE:  # DOWN
                    moves.append("2F")
                moves.append("U'")
            elif left_face.grid[2][1] == WHITE:  # DOWN
                if not self.center_face.grid[1][0] == WHITE:  # LEFT
                    moves.append("F'")
                elif not self.center_face.grid[1][2] == WHITE:  # RIGHT
                    moves.append("F")
                elif not self.center_face.grid[0][1] == WHITE:  # UP
                    moves.append("2F")
                moves.append("D")
            elif left_face.grid[1][0] == WHITE:  # LEFT
                if not self.center_face.grid[1][0] == WHITE:  # LEFT
                    moves.append("L'")
                    moves.append("F'")
                    moves.append("D")
                elif not self.center_face.grid[2][1] == WHITE:  # DOWN
                    moves.append("F")
                    moves.append("L'")
                    moves.append("F'")
                    moves.append("D")
                elif not self.center_face.grid[0][1] == WHITE:  # UP
                    moves.append("F'")
                    moves.append("L")
                    moves.append("F")
                    moves.append("U'")
                elif not self.center_face.grid[1][2] == WHITE:  # RIGHT
                    moves.append("2F")
                    moves.append("L")
                    moves.append("F")
                    moves.append("U'")
            elif left_face.grid[1][2] == WHITE:  # RIGHT
                moves.append("L'")
                moves.append("F")
                moves.append("U'")

            if (
                left_face.grid[0][1] == WHITE
                or left_face.grid[2][1] == WHITE
                or left_face.grid[1][0] == WHITE
                or left_face.grid[1][2] == WHITE
            ):
                print("left_face")
                self.move_cube(moves)
                continue

            right_face = self.get_right()

            if right_face.grid[0][1] == WHITE:  # UP
                if not self.center_face.grid[1][0] == WHITE:  # LEFT
                    moves.append("F")
                elif not self.center_face.grid[1][2] == WHITE:  # RIGHT
                    moves.append("F'")
                elif not self.center_face.grid[2][1] == WHITE:  # DOWN
                    moves.append("2F")
                moves.append("U")
            elif right_face.grid[2][1] == WHITE:  # DOWN
                if not self.center_face.grid[1][0] == WHITE:  # LEFT
                    moves.append("F'")
                elif not self.center_face.grid[1][2] == WHITE:  # RIGHT
                    moves.append("F")
                elif not self.center_face.grid[0][1] == WHITE:  # UP
                    moves.append("2F")
                moves.append("D")
            elif right_face.grid[1][0] == WHITE:  # LEFT
                moves.append("R")
                moves.append("F'")
                moves.append("U")
            elif right_face.grid[1][2] == WHITE:  # RIGHT
                if not self.center_face.grid[1][2] == WHITE:  # RIGHT
                    moves.append("R'")
                    moves.append("F'")
                    moves.append("U")
                elif not self.center_face.grid[2][1] == WHITE:  # DOWN
                    moves.append("F'")
                    moves.append("R'")
                    moves.append("F'")
                    moves.append("U")
                elif not self.center_face.grid[0][1] == WHITE:  # UP
                    moves.append("F")
                    moves.append("R'")
                    moves.append("F'")
                    moves.append("U")
                elif not self.center_face.grid[1][0] == WHITE:  # LEFT
                    moves.append("2F")
                    moves.append("R'")
                    moves.append("F'")
                    moves.append("U")

            if (
                right_face.grid[0][1] == WHITE
                or right_face.grid[2][1] == WHITE
                or right_face.grid[1][0] == WHITE
                or right_face.grid[1][2] == WHITE
            ):
                print("right_face")
                self.move_cube(moves)
                continue

            up_face = self.get_up()

            if up_face.grid[1][0] == WHITE:  # LEFT
                if not self.center_face.grid[0][1] == WHITE:  # TOP
                    moves.append("F'")
                elif not self.center_face.grid[1][2] == WHITE:  # RIGHT
                    moves.append("2F")
                elif not self.center_face.grid[2][1] == WHITE:  # DOWN
                    moves.append("F")
                moves.append("L")
            elif up_face.grid[1][2] == WHITE:  # RIGHT
                if not self.center_face.grid[0][1] == WHITE:  # TOP
                    moves.append("F")
                elif not self.center_face.grid[1][0] == WHITE:  # LEFT
                    moves.append("2F")
                elif not self.center_face.grid[2][1] == WHITE:  # DOWN
                    moves.append("F'")
                moves.append("R'")
            elif up_face.grid[2][1] == WHITE:  # DOWN
                moves.append("U")
                moves.append("F'")
                moves.append("L")
            elif up_face.grid[0][1] == WHITE:  # UP
                if not self.center_face.grid[0][1] == WHITE:  # UP
                    moves.append("U'")
                    moves.append("F'")
                    moves.append("L")
                elif not self.center_face.grid[1][0] == WHITE:  # LEFT
                    moves.append("F")
                    moves.append("U'")
                    moves.append("F'")
                    moves.append("L")
                elif not self.center_face.grid[1][2] == WHITE:  # RIGHT
                    moves.append("F'")
                    moves.append("U")
                    moves.append("F")
                    moves.append("R'")
                elif not self.center_face.grid[2][1] == WHITE:  # DOWN
                    moves.append("2F")
                    moves.append("U'")
                    moves.append("F'")
                    moves.append("L")

            if (
                up_face.grid[0][1] == WHITE
                or up_face.grid[2][1] == WHITE
                or up_face.grid[1][0] == WHITE
                or up_face.grid[1][2] == WHITE
            ):
                print("up_face")
                self.move_cube(moves)
                continue

            down_face = self.get_down()

            if down_face.grid[1][0] == WHITE:  # LEFT
                if not self.center_face.grid[0][1] == WHITE:  # TOP
                    moves.append("F'")
                elif not self.center_face.grid[1][2] == WHITE:  # RIGHT
                    moves.append("2F")
                elif not self.center_face.grid[2][1] == WHITE:  # DOWN
                    moves.append("F")
                moves.append("L'")
            elif down_face.grid[1][2] == WHITE:  # RIGHT
                if not self.center_face.grid[0][1] == WHITE:  # TOP
                    moves.append("F")
                elif not self.center_face.grid[1][0] == WHITE:  # LEFT
                    moves.append("2F")
                elif not self.center_face.grid[2][1] == WHITE:  # DOWN
                    moves.append("F'")
                moves.append("R")
            elif down_face.grid[0][1] == WHITE:  # UP
                moves.append("D")
                moves.append("F'")
                moves.append("R")
            elif down_face.grid[2][1] == WHITE:  # DOWN
                if not self.center_face.grid[2][1] == WHITE:  # DOWN
                    moves.append("D'")
                    moves.append("F'")
                    moves.append("R")
                elif not self.center_face.grid[1][0] == WHITE:  # LEFT
                    moves.append("F'")
                    moves.append("D")
                    moves.append("F")
                    moves.append("L'")
                elif not self.center_face.grid[1][2] == WHITE:  # RIGHT
                    moves.append("F")
                    moves.append("D'")
                    moves.append("F'")
                    moves.append("R'")
                elif not self.center_face.grid[0][1] == WHITE:  # UP
                    moves.append("2F")
                    moves.append("D'")
                    moves.append("F'")
                    moves.append("R'")

            if (
                down_face.grid[0][1] == WHITE
                or down_face.grid[2][1] == WHITE
                or down_face.grid[1][0] == WHITE
                or down_face.grid[1][2] == WHITE
            ):
                print("down_face")
                self.move_cube(moves)
                continue

            back_face = next(
                (
                    self.faces[pos]
                    for pos in self.faces
                    if self.faces[pos]
                    not in [
                        self.center_face,
                        left_face,
                        right_face,
                        up_face,
                        down_face,
                    ]
                )
            )

            if back_face.grid[1][0] == WHITE:  # LEFT
                if not self.center_face.grid[0][1] == WHITE:  # TOP
                    moves.append("F'")
                elif not self.center_face.grid[1][2] == WHITE:  # RIGHT
                    moves.append("2F")
                elif not self.center_face.grid[2][1] == WHITE:  # DOWN
                    moves.append("F")
                moves.append("2L")
            elif back_face.grid[1][2] == WHITE:  # RIGHT
                if not self.center_face.grid[0][1] == WHITE:  # TOP
                    moves.append("F")
                elif not self.center_face.grid[1][0] == WHITE:  # LEFT
                    moves.append("2F")
                elif not self.center_face.grid[2][1] == WHITE:  # DOWN
                    moves.append("F'")
                moves.append("2R")
            elif back_face.grid[0][1] == WHITE:  # TOP
                if not self.center_face.grid[1][2] == WHITE:  # RIGHT
                    moves.append("F")
                elif not self.center_face.grid[1][0] == WHITE:  # LEFT
                    moves.append("F'")
                elif not self.center_face.grid[0][1] == WHITE:  # TOP
                    moves.append("2F")
                moves.append("2D")
            elif back_face.grid[2][1] == WHITE:  # DOWN
                if not self.center_face.grid[2][1] == WHITE:  # DOWN
                    moves.append("2F")
                elif not self.center_face.grid[1][0] == WHITE:  # LEFT
                    moves.append("F")
                elif not self.center_face.grid[1][2] == WHITE:  # RIGHT
                    moves.append("F'")
                moves.append("2U")

            if (
                back_face.grid[0][1] == WHITE
                or back_face.grid[2][1] == WHITE
                or back_face.grid[1][0] == WHITE
                or back_face.grid[1][2] == WHITE
            ):
                print("back_face")
                self.move_cube(moves)
                continue

    def do_good_white_cross(self):
        up_face = self.get_up()
        left_face = self.get_left()
        down_face = self.get_down()
        right_face = self.get_right()
        if not all(
            [
                up_face.grid[2][1] == up_face.center_color,  # DOWN
                left_face.grid[1][2] == left_face.center_color,  # RIGHT
                down_face.grid[0][1] == down_face.center_color,  # UP
                right_face.grid[1][0] == right_face.center_color,  # LEFT
            ]
        ):
            center_data = [
                up_face.center_color,
                left_face.center_color,
                down_face.center_color,
                right_face.center_color,
            ]
            cross_data = [
                up_face.grid[2][1],
                left_face.grid[1][2],
                down_face.grid[0][1],
                right_face.grid[1][0],
            ]

            moves_counter_clockwise = 0
            max_matching_value = len(
                [0 for i in range(4) if center_data[i] == cross_data[i]]
            )
            while max_matching_value < 2 and moves_counter_clockwise != 3:
                obj = cross_data.pop()
                cross_data.insert(0, obj)
                max_matching_value = len(
                    [0 for i in range(4) if center_data[i] == cross_data[i]]
                )
                moves_counter_clockwise += 1
            print(moves_counter_clockwise)

            if moves_counter_clockwise == 1:
                self.move_cube("F'")
            elif moves_counter_clockwise == 2:
                self.move_cube("2F")
            elif moves_counter_clockwise == 3:
                self.move_cube("F")

        max_matching_value = sum(
            [
                1 if up_face.grid[2][1] == up_face.center_color else 0,  # DOWN
                1 if left_face.grid[1][2] == left_face.center_color else 0,  # RIGHT
                1 if down_face.grid[0][1] == down_face.center_color else 0,  # UP
                1 if right_face.grid[1][0] == right_face.center_color else 0,  # LEFT
            ]
        )

        stored_item = {"value": -1, "pos": ""}
        while max_matching_value != 4:
            if stored_item["value"] < 0:
                if up_face.grid[2][1] != up_face.center_color:  # DOWN
                    stored_item["pos"] = "UP"
                    stored_item["value"] = up_face.grid[2][1]
                    self.move_cube("2U")
                elif left_face.grid[1][2] != left_face.center_color:  # RIGHT
                    stored_item["pos"] = "LEFT"
                    stored_item["value"] = left_face.grid[1][2]
                    self.move_cube("2L")
                elif down_face.grid[0][1] != down_face.center_color:  # RIGHT
                    stored_item["pos"] = "DOWN"
                    stored_item["value"] = down_face.grid[0][1]
                    self.move_cube("2D")
                elif right_face.grid[1][0] != right_face.center_color:  # RIGHT
                    stored_item["pos"] = "RIGHT"
                    stored_item["value"] = right_face.grid[1][0]
                    self.move_cube("2D")
            else:
                moves_clockwise = 0
                good_pos = "UP"
                print('stored_item["value"]', stored_item["value"])
                if left_face.center_color == stored_item["value"]:
                    moves_clockwise = 3
                    good_pos = "LEFT"
                elif down_face.center_color == stored_item["value"]:
                    moves_clockwise = 2
                    good_pos = "DOWN"
                elif right_face.center_color == stored_item["value"]:
                    moves_clockwise = 1
                    good_pos = "RIGHT"

                print(moves_clockwise)
                if stored_item["pos"] == "DOWN":
                    moves_clockwise += 2
                elif stored_item["pos"] == "RIGHT":
                    moves_clockwise += 3
                elif stored_item["pos"] == "LEFT":
                    moves_clockwise += 1

                print(moves_clockwise)

                if moves_clockwise % 4 == 1:
                    self.move_cube("B")
                elif moves_clockwise % 4 == 2:
                    self.move_cube("2B")
                elif moves_clockwise % 4 == 3:
                    self.move_cube("B'")

                stored_item["value"] = -1

                if good_pos == "DOWN":
                    if self.center_face.grid[2][1] == WHITE:
                        stored_item["value"] = down_face.grid[0][1]
                        stored_item["pos"] = "DOWN"
                    self.move_cube("2D")
                elif good_pos == "RIGHT":
                    if self.center_face.grid[1][2] == WHITE:
                        stored_item["value"] = right_face.grid[1][0]
                        stored_item["pos"] = "RIGHT"
                    self.move_cube("2R")
                elif good_pos == "UP":
                    if self.center_face.grid[0][1] == WHITE:
                        stored_item["value"] = up_face.grid[2][1]
                        stored_item["pos"] = "UP"
                    self.move_cube("2U")
                elif good_pos == "LEFT":
                    if self.center_face.grid[1][0] == WHITE:
                        stored_item["value"] = left_face.grid[1][2]
                        stored_item["pos"] = "LEFT"
                    self.move_cube("2L")

            max_matching_value = sum(
                [
                    (
                        1
                        if up_face.grid[2][1] == up_face.center_color
                        and self.center_face.grid[0][1] == WHITE
                        else 0
                    ),  # DOWN
                    (
                        1
                        if left_face.grid[1][2] == left_face.center_color
                        and self.center_face.grid[1][2] == WHITE
                        else 0
                    ),  # RIGHT
                    (
                        1
                        if down_face.grid[0][1] == down_face.center_color
                        and self.center_face.grid[2][1] == WHITE
                        else 0
                    ),  # UP
                    (
                        1
                        if right_face.grid[1][0] == right_face.center_color
                        and self.center_face.grid[1][0] == WHITE
                        else 0
                    ),  # LEFT
                ]
            )

    def check_white_face(self) -> bool:
        for row in self.center_face:
            for value in row:
                if value != self.center_face.center_color:
                    return False

        return True

    def do_white_face(self):
        face_up = self.get_up()
        face_down = self.get_down()
        face_left = self.get_left()
        face_right = self.get_right()
        face_front = self.center_face
        face_back = next(
            (
                self.faces[pos]
                for pos in self.faces
                if self.faces[pos]
                not in [
                    face_up,
                    face_down,
                    face_left,
                    face_right,
                    face_front,
                ]
            )
        )

        if face_front.grid[0][0] != face_front.center_color:  # TOP LEFT CORNER
            if face_up.grid[2][0] == face_front.center_color:
                self.move_cube(["U", "2B", "U'", "L'", "2B", "L"])
            elif face_left.grid[0][2] == face_front.center_color:
                self.move_cube(["L'", "2B", "L", "U", "2B", "U'"])
            else:
                while (
                    face_back.grid[2][0] != face_front.center_color
                    and face_left.grid[0][0] != face_front.center_color
                    and face_up.grid[0][0] != face_front.center_color
                ):
                    self.move_cube("B")
                if face_left.grid[0][0] == face_front.center_color:
                    self.move_cube(["L'", "B", "L"])
                elif face_up.grid[0][0] == face_front.center_color:
                    self.move_cube(["U", "B'", "U'"])
                else:
                    self.move_cube(["L'", "2B", "L", "B'", "L'", "B", "L"])

        if face_front.grid[0][2] != face_front.center_color:  # TOP RIGHT CORNER
            if face_up.grid[2][2] == face_front.center_color:
                self.move_cube(["U'", "2B", "U", "R", "2B", "R'"])
            elif face_right.grid[0][0] == face_front.center_color:
                self.move_cube(["R", "2B", "R'", "U'", "2B", "U"])
            else:
                while (
                    face_back.grid[2][2] != face_front.center_color
                    and face_right.grid[0][2] != face_front.center_color
                    and face_up.grid[0][2] != face_front.center_color
                ):
                    self.move_cube("B")
                if face_right.grid[0][2] == face_front.center_color:
                    self.move_cube(["R", "B'", "R'"])
                elif face_up.grid[0][2] == face_front.center_color:
                    self.move_cube(["U'", "B", "U"])
                else:
                    self.move_cube(["R", "2B", "R'", "B", "R", "B'", "R'"])

        if face_front.grid[2][0] != face_front.center_color:  # BOTTOM LEFT CORNER
            if face_down.grid[0][0] == face_front.center_color:
                self.move_cube(["D'", "2B", "D", "L", "2B", "L'"])
            elif face_left.grid[2][2] == face_front.center_color:
                self.move_cube(["L", "2B", "L'", "D'", "2B", "D"])
            else:
                while (
                    face_back.grid[0][0] != face_front.center_color
                    and face_left.grid[2][0] != face_front.center_color
                    and face_down.grid[2][0] != face_front.center_color
                ):
                    self.move_cube("B")
                if face_left.grid[2][0] == face_front.center_color:
                    self.move_cube(["L", "B'", "L'"])
                elif face_down.grid[2][0] == face_front.center_color:
                    self.move_cube(["D'", "B", "D"])
                else:
                    self.move_cube(["L", "2B", "L'", "B", "L", "B'", "L'"])

        if face_front.grid[2][2] != face_front.center_color:  # BOTTOM RIGHT CORNER
            if face_down.grid[0][2] == face_front.center_color:
                self.move_cube(["D", "2B", "D'", "R'", "2B", "R"])
            elif face_right.grid[2][0] == face_front.center_color:
                self.move_cube(["R'", "2B", "R", "D", "2B", "D'"])
            else:
                while (
                    face_back.grid[0][2] != face_front.center_color
                    and face_right.grid[2][2] != face_front.center_color
                    and face_down.grid[2][2] != face_front.center_color
                ):
                    self.move_cube("B")
                if face_right.grid[2][2] == face_front.center_color:
                    self.move_cube(["R'", "B", "R"])
                elif face_down.grid[2][2] == face_front.center_color:
                    self.move_cube(["D", "B'", "D'"])
                else:
                    self.move_cube(["R'", "2B", "R", "B'", "R'", "B", "R"])

    def check_white_first_crown(self) -> bool:
        face_up = self.get_up()
        face_down = self.get_down()
        face_left = self.get_left()
        face_right = self.get_right()
        face_front = self.center_face
        face_back = next(
            (
                self.faces[pos]
                for pos in self.faces
                if self.faces[pos]
                not in [
                    face_up,
                    face_down,
                    face_left,
                    face_right,
                    face_front,
                ]
            )
        )

        if not (
            face_front.grid[0][0] == face_front.center_color  # FRONT FACE | TOP LEFT
            and face_left.grid[0][2] == face_left.center_color  # LEFT FACE | TOP RIGHT
            and face_up.grid[2][0] == face_up.center_color  # UP FACE | DOWN LEFT
        ):
            return False

        if not (
            face_front.grid[0][2] == face_front.center_color  # FRONT FACE | TOP RIGHT
            and face_up.grid[2][2] == face_up.center_color  # UP FACE | DOWN RIGHT
            and face_right.grid[0][0]
            == face_right.center_color  # RIGHT FACE | DOWN RIGHT
        ):
            return False

        if not (
            face_front.grid[2][0] == face_front.center_color  # FRONT FACE | DOWN LEFT
            and face_left.grid[2][2] == face_left.center_color  # LEFT FACE | DOWN RIGHT
            and face_down.grid[0][0] == face_down.center_color  # DOWN FACE | UP LEFT
        ):
            return False

        if not (
            face_front.grid[2][2] == face_front.center_color  # FRONT FACE | DOWN RIGHT
            and face_down.grid[0][2] == face_down.center_color  # DOWN FACE | TOP RIGHT
            and face_right.grid[2][0]
            == face_right.center_color  # RIGHT FACE | DOWN LEFT
        ):
            return False

        # face_front[0][2]  # FRONT FACE | TOP RIGHT
        # face_front[2][0]  # FRONT FACE | DOWN LEFT
        # face_front[2][2]  # FRONT FACE | DOWN RIGHT

        return True

    def do_white_first_crown(self):
        face_up = self.get_up()
        face_down = self.get_down()
        face_left = self.get_left()
        face_right = self.get_right()
        face_front = self.center_face
        face_back = next(
            (
                self.faces[pos]
                for pos in self.faces
                if self.faces[pos]
                not in [
                    face_up,
                    face_down,
                    face_left,
                    face_right,
                    face_front,
                ]
            )
        )

        while not self.check_white_first_crown():
            pass


# while not all(
#     [
#         up_face.grid[2][1] == up_face.center_color, # DOWN
#         left_face.grid[1][2] == left_face.center_color, # RIGHT
#         down_face.grid[0][1] == down_face.center_color, # UP
#         right_face.grid[1][0] == right_face.center_color, # LEFT
#     ]
# ):
#     pass