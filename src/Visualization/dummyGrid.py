import random


class GridTest:
    def __init__(self, cell_count):
        self.cell_count = cell_count
        self.grid = []
        y = 0
        x = 0
        for row in range(cell_count):
            # Add an empty array that will hold each cell
            # in this row
            self.grid.append([])
            y += 1
            for column in range(cell_count):
                self.grid[row].append(0 if random.randint(0, 2) == 1 else 1)  # Append a cell
                x += 1

    def step(self):
        ngrid = []
        for x in range(self.cell_count):
            ngrid.append([])
            for y in range(self.cell_count):
                ngrid[x].append(0)

        for x in range(1, self.cell_count - 1):
            for y in range(1, self.cell_count - 1):
                neig = 0
                if self.grid[x - 1][y - 1] == 1:
                    neig += 1
                if self.grid[x][y - 1] == 1:
                    neig += 1
                if self.grid[x - 1][y] == 1:
                    neig += 1
                if self.grid[x + 1][y + 1] == 1:
                    neig += 1
                if self.grid[x][y + 1] == 1:
                    neig += 1
                if self.grid[x + 1][y] == 1:
                    neig += 1
                if self.grid[x - 1][y + 1] == 1:
                    neig += 1
                if self.grid[x + 1][y - 1] == 1:
                    neig += 1

                if neig <= 1 or neig >= 4:
                    ngrid[x][y] = 0
                else:
                    ngrid[x][y] = 1

        self.grid = ngrid
