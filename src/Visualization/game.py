import math

import pygame
from .camera import Camera
from .UI import Button
from .grid import GridPickle


class Game:
    def __init__(self, logs_path: str):
        pygame.init()
        self.FPS = 20
        self.STEP_TIME = 2.0
        self.WINDOW_SIZE = (800, 800)
        self.screen = pygame.display.set_mode(self.WINDOW_SIZE)
        pygame.display.set_caption("Battle")
        self.done = False
        self.clock = pygame.time.Clock()
        self.grid = GridPickle(300, logs_path)
        self.buttons: [Button] = []
        self.camera = Camera(0, 0, 200, 50)
        self.frame = 0  # frames counter (pygame frames, not related to simulation steps)
        self.running = True  # state of simulation (running / stopped)
        self.FONT_SIZE = 15
        self.FONT = pygame.font.Font("Lato-Regular.ttf", self.FONT_SIZE)

        # UI
        self.__button_start_stop: Button = None

        # run the game
        self.__init_ui()
        self.__main_loop()

    # Buttons functions
    def __update_rate_plus(self):
        if self.STEP_TIME >= 0.06:
            self.STEP_TIME /= 1.2

    def __update_rate_minus(self):
        if self.STEP_TIME < 3.0:
            self.STEP_TIME *= 1.2

    def __start_stop_simulation(self):
        if self.running:
            self.running = False
            self.__button_start_stop.set_text("START")
        else:
            self.running = True
            self.__button_start_stop.set_text("STOP")

    def __init_ui(self):
        color = pygame.Color(100, 100, 100)
        self.buttons = [
            Button(325 - 75, 730, 70, 70, "STOP", self.screen, color, self.__start_stop_simulation),
            Button(325 - 150, 730, 70, 70, "|<=", self.screen, color, self.grid.to_start),
            Button(325, 730, 70, 70, "+", self.screen, color, self.__update_rate_plus),
            Button(325 + 75, 730, 70, 70, "-", self.screen, color, self.__update_rate_minus),
            Button(325 + 150, 730, 70, 70, "Next", self.screen, color, self.grid.step),
            Button(325 + 225, 730, 70, 70, "Prev", self.screen, color, self.grid.prev_step)
        ]

        self.__button_start_stop = self.buttons[0]

    # render text with linebreaks (\n)
    def __draw_text(self, text: str, x: int, y: int, line_spacing: int = 2):
        text = text.split('\n')
        text_surfaces: [pygame.Surface, (int, int)] = []
        height = 0
        for t in text:
            text_surface = self.FONT.render(t, True, (0, 0, 0))
            rect = text_surface.get_rect()
            rect.topleft = (x, y + height)
            text_surfaces.append((text_surface, rect))
            height += line_spacing + self.FONT_SIZE
        self.screen.blits(text_surfaces)

    # size of text to be rendered in pixels
    def __text_size(self, text: str, line_spacing: int = 2) -> (int, int):
        text = text.split('\n')
        width = 0
        height = 0
        for t in text:
            width = max(width, self.FONT.size(t)[0])
            height += self.FONT_SIZE + line_spacing
        return width, height

    def __draw_unit_info(self, text: str):
        rect = pygame.Rect(pygame.mouse.get_pos(), self.__text_size(text))
        rect.bottomright = pygame.mouse.get_pos()
        if pygame.mouse.get_pos()[0] < rect.width:
            rect.left = pygame.mouse.get_pos()[0]
        if pygame.mouse.get_pos()[1] < rect.height:
            rect.top = pygame.mouse.get_pos()[1]
        if pygame.mouse.get_pos()[0] < rect.width and pygame.mouse.get_pos()[1] < rect.height:
            rect.topleft = (rect.topleft[0] + 10, rect.topleft[1] + 10)
        pygame.draw.rect(self.screen, (123, 123, 123),
                         rect)
        self.__draw_text(text, *rect.topleft)

    def __input_handler(self):
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                self.done = True  # Flag that we are done so we exit this loop
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Buttons
                for button in self.buttons:
                    if button.rect().collidepoint(event.pos):
                        button.clicked()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:
                    self.camera.zoom_in()
                elif event.key == pygame.K_l:
                    self.camera.zoom_out()
                elif event.key == pygame.K_a:
                    self.camera.move(-5, 0)
                elif event.key == pygame.K_d:
                    self.camera.move(5, 0)
                elif event.key == pygame.K_w:
                    self.camera.move(0, -5)
                elif event.key == pygame.K_s:
                    self.camera.move(0, 5)

    def __render_grid(self, grid: [[int]]):
        self.screen.fill(pygame.Color(200, 200, 200))
        screen_size = self.WINDOW_SIZE
        cells_x = self.camera.width
        cells_y = math.ceil(cells_x / screen_size[0] * screen_size[1])

        cells_size = math.ceil(screen_size[0] / cells_y)
        for row in range(cells_x):
            for column in range(cells_y):
                color = pygame.Color("white")
                # ignore empty
                if grid[row + self.camera.x][column + self.camera.y] == 0:
                    continue
                # camera should take care of not showing any tiles outside a grid,
                # but it needs to have max_width the same as grid cell_count
                # if row + self.camera.x < len(grid[0]) and column + self.camera.y < len(grid):

                if grid[row + self.camera.x][column + self.camera.y] == 1:
                    color = pygame.Color("black")

                elif grid[row + self.camera.x][column + self.camera.y] == 2:
                    color = pygame.Color("green")

                elif grid[row + self.camera.x][column + self.camera.y] == 3:
                    color = pygame.Color("red")

                elif grid[row + self.camera.x][column + self.camera.y] != 0:  # shouldn't happen
                    color = pygame.Color("yellow")

                pygame.draw.rect(self.screen,
                                 color,
                                 [cells_size * row,
                                  cells_size * column,
                                  cells_size,
                                  cells_size])

                # unit on mouse hover info
                mouse_over_ui = False
                for button in self.buttons:
                    if button.rect().collidepoint(pygame.mouse.get_pos()):
                        mouse_over_ui = True
                        break
                if not mouse_over_ui:
                    click_x, click_y = self.camera.screen_to_grid_point(*pygame.mouse.get_pos(), cells_size)
                    if grid[click_x][click_y] != 0:
                        self.__draw_unit_info("Value:\n" + str(grid[click_x][click_y]))

    def __render_ui(self):
        for button in self.buttons:
            button.draw()

    def __main_loop(self):
        while True:
            grid = self.grid.get_grid()

            # input
            self.__input_handler()

            # render grid
            self.__render_grid(grid)

            # render UI
            self.__render_ui()

            # finish
            pygame.display.flip()
            self.frame += 1
            if self.done:
                break
            # update simulation step once per STEP_TIME seconds
            if self.running and self.frame % (round(self.FPS * self.STEP_TIME)) == 0:
                self.grid.step()

            self.clock.tick(self.FPS)

        pygame.quit()
