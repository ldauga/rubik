class Face(object):

    center_color: int

    grid: list

    def __init__(self, color, grid=None):
        self.center_color = color
        if grid:
            self.grid = [row[:] for row in grid]  # Create a deep copy of the grid
        else:
            self.grid = [[color]*3 for _ in range(3)]

    def __eq__(self, other):
        for y in range(3):
            for x in range(3):
                if self.grid[y][x] != other.grid[y][x]:
                    return False

        return True

    def is_solved(self):
        for row in self.grid:
            for value in row:
                if value != self.center_color:
                    return False
        return True
