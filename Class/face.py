class Face(object):

    center_color: int

    grid: list

    def __init__(self, center_color):
        self.center_color = center_color
        self.grid = [
            [center_color, center_color, center_color],
            [center_color, center_color, center_color],
            [center_color, center_color, center_color],
        ]

    def is_solved(self):
        for row in self.grid:
            for value in row:
                if value != self.center_color:
                    return False
        return True
