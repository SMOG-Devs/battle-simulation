# use left mouse button to select start
# and right mouse button to select end
import math

import pygame
from src.Visualization.camera import Camera
from src.Visualization.grid import Terrain


class Game:
    def __init__(self, size: int):
        pygame.init()
        self.FPS = 20
        self.WINDOW_SIZE = (800, 800)
        self.screen = pygame.display.set_mode(self.WINDOW_SIZE)
        pygame.display.set_caption("Pathfinding tester")
        self.done = False
        self.clock = pygame.time.Clock()
        self.terrain = Terrain(size, size)  # TODO: automatic size of terrain
        self.camera = Camera(0, 0, size, 50)
        self.running = True  # state of simulation (running / stopped)

        self.path_start: (int, int) = None
        self.path_end: (int, int) = None

        self.path: [(int, int)] = []

        # run the game
        self.__main_loop()

    # Buttons functions

    def __input_handler(self):
        screen_size = self.WINDOW_SIZE
        cells_x = self.camera.width
        cells_y = math.ceil(cells_x / screen_size[0] * screen_size[1])

        cells_size = math.ceil(screen_size[0] / cells_y)

        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                self.done = True  # Flag that we are done so we exit this loop
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.path_start = self.camera.screen_to_grid_point(*pygame.mouse.get_pos(), cells_size)
                elif event.button == 3:
                    self.path_end = self.camera.screen_to_grid_point(*pygame.mouse.get_pos(), cells_size)
                    if self.path_start is not None:
                        start = pygame.time.get_ticks()
                        self.path = self.terrain.shortest_path(self.path_start, self.path_end)
                        print("Time: ", (pygame.time.get_ticks() - start) / 1000, "lenght: ", len(self.path))

    def __render_terrain(self):
        screen_size = self.WINDOW_SIZE
        cells_x = self.camera.width
        cells_y = math.ceil(cells_x / screen_size[0] * screen_size[1])

        cells_size = math.ceil(screen_size[0] / cells_y)

        grid = self.terrain.get_grid()
        colors_dict = self.terrain.get_colors()
        for row in range(cells_x):
            for column in range(cells_y):
                color = colors_dict.get(grid[row + self.camera.x][column + self.camera.y],
                                        (0, 0, 0))  # default color is black
                pygame.draw.rect(self.screen,
                                 color,
                                 [cells_size * row,
                                  cells_size * column,
                                  cells_size,
                                  cells_size])

        if self.path_start:
            pygame.draw.rect(self.screen,
                             (0, 0, 0),
                             [cells_size * self.path_start[0],
                              cells_size * self.path_start[1],
                              cells_size,
                              cells_size])
        if self.path_end:
            pygame.draw.rect(self.screen,
                             (0, 0, 0),
                             [cells_size * self.path_end[0],
                              cells_size * self.path_end[1],
                              cells_size,
                              cells_size])

    def __render_path(self):
        screen_size = self.WINDOW_SIZE
        cells_x = self.camera.width
        cells_y = math.ceil(cells_x / screen_size[0] * screen_size[1])

        cells_size = math.ceil(screen_size[0] / cells_y)

        for node in self.path:
            pygame.draw.rect(self.screen,
                             (255, 0, 0),
                             [cells_size * node[0],
                              cells_size * node[1],
                              cells_size,
                              cells_size])

    def __main_loop(self):
        while True:
            # input
            self.__input_handler()

            # render grid
            self.screen.fill(pygame.Color(200, 200, 200))
            self.__render_terrain()  # TODO: optimize, rendering the same terrain every time is a waste
            self.__render_path()

            # finish
            pygame.display.flip()
            if self.done:
                break
            self.clock.tick(self.FPS)

        pygame.quit()


if __name__ == "__main__":
    Game(100)
