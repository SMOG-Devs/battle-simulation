import math

import pygame
from pygame import Color
from .camera import Camera
from .UI import Button
from .grid import GridPickle, Terrain
from pygame import mixer




class Game:
    def __init__(self, logs_path: str):
        pygame.init()
        self.FPS = 20
        self.STEP_TIME = 0.4
        self.WINDOW_SIZE = (800, 800)
        self.screen = pygame.display.set_mode(self.WINDOW_SIZE)
        pygame.display.set_caption("Battle")
        self.done = False
        self.clock = pygame.time.Clock()
        self.grid = GridPickle(400, logs_path)  # TODO: automatic size of camera and grid from model.constrains
        self.terrain = Terrain(400, 400)  # TODO: automatic size of terrain from model.constrains
        self.terrain_texture = None
        self.camera = Camera(0, 0, 400)
        self.buttons: [Button] = []
        self.frame = 0  # frames counter (pygame frames, not related to simulation steps)
        self.step = 0  # step in simulation
        self.running = True  # state of simulation (running / stopped)
        self.FONT_SIZE = 15
        self.FONT = pygame.font.Font("Lato-Regular.ttf", self.FONT_SIZE)

        # UI
        self.__button_start_stop: Button = None

        # music
        # Instantiate mixer
        mixer.init()

        # Load audio file
        mixer.music.load('glorious_morning.mp3')

        print("music started playing....")

        # Set preferred volume
        mixer.music.set_volume(0.2)

        # Play the music
        mixer.music.play()

        # run the game
        self.__load_sprites()
        self.__prepare_texture()
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

    def __music_start_stop(self):
        if mixer.music.get_busy():
            mixer.music.pause()
            self.__button_music.set_text("O")
        else:
            mixer.music.unpause()
            self.__button_music.set_text("X")

    def __next_step(self):
        self.step += 1
        self.grid.step()

    def __prev_step(self):
        self.step -= 1
        self.grid.prev_step()

    def __init_ui(self):
        color = pygame.Color(100, 100, 100)
        # start/stop button is always first
        # music button is second
        self.buttons = [
            Button(325 - 75, 730, 70, 70, "STOP", self.screen, color, self.__start_stop_simulation),
            Button(0, 0, 20, 20, "O", self.screen, color, self.__music_start_stop),
            Button(325 - 150, 730, 70, 70, "|<=", self.screen, color, self.grid.to_start),
            Button(325, 730, 70, 70, "+", self.screen, color, self.__update_rate_plus),
            Button(325 + 75, 730, 70, 70, "-", self.screen, color, self.__update_rate_minus),
            Button(325 + 150, 730, 70, 70, "Next", self.screen, color, self.__next_step),
            Button(325 + 225, 730, 70, 70, "Prev", self.screen, color, self.__prev_step)
        ]

        self.__button_start_stop = self.buttons[0]
        self.__button_music = self.buttons[1]

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
    # popup menu displaying info about units

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
        screen_size = self.WINDOW_SIZE
        cells_x = self.camera.width
        cells_y = math.ceil(cells_x / screen_size[0] * screen_size[1])
        cells_size = math.ceil(screen_size[0] / cells_y)
        if self.camera.width < 50:
            self.__render_unit_close(grid, cells_x, cells_y, cells_size)
        else:
            self.__render_unit_far_away(grid, cells_x, cells_y, cells_size)

        # unit on mouse hover info
        mouse_over_ui = False
        for button in self.buttons:
            if button.rect().collidepoint(pygame.mouse.get_pos()):
                mouse_over_ui = True
                break
        if not mouse_over_ui:
            click_x, click_y = self.camera.screen_to_grid_point(*pygame.mouse.get_pos(), cells_size)
            if grid[click_x][click_y] != 0:
                self.__draw_unit_info(self.grid.get_description(click_x, click_y))

    def __render_unit_close(self, grid: [[int]], cells_x: int, cells_y: int, cells_size: int):
        for row in range(cells_x):
            for column in range(cells_y):
                color = pygame.Color("white")
                # ignore empty
                if grid[row + self.camera.x][column + self.camera.y] == 0:
                    continue
                # camera should take care of not showing any tiles outside a grid,
                # but it needs to have max_width the same as grid cell_count
                # if row + self.camera.x < len(grid[0]) and column + self.camera.y < len(grid):

                unit_type = grid[row + self.camera.x][column + self.camera.y]
                texture = []
                if unit_type == 2:
                    texture = self.rejter_blue[self.camera.size]
                elif unit_type == 3:
                    texture = self.hussar_blue[self.camera.size]
                elif unit_type == 4:
                    texture = self.cannon_blue[self.camera.size]
                elif unit_type == 5:
                    texture = self.rejter_blue[self.camera.size]
                elif unit_type == 6:
                    texture = self.infantry_blue[self.camera.size]
                if unit_type == 7:
                    texture = self.rejter_red[self.camera.size]
                elif unit_type == 8:
                    texture = self.hussar_red[self.camera.size]
                elif unit_type == 9:
                    texture = self.cannon_red[self.camera.size]
                elif unit_type == 10:
                    texture = self.rejter_red[self.camera.size]
                elif unit_type == 11:
                    texture = self.infantry_red[self.camera.size]

                self.screen.blit(texture, (cells_size * row, cells_size * column))

                # if grid[row + self.camera.x][column + self.camera.y] == 2:
                #     self.screen.blit(self.infantry_red[self.camera.size], (cells_size * row, cells_size * column))
                #     continue
                #
                # elif grid[row + self.camera.x][column + self.camera.y] == 3:
                #     self.screen.blit(self.infantry_blue[self.camera.size], (cells_size * row, cells_size * column))
                #     continue



    def __render_unit_far_away(self, grid: [[int]], cells_x: int, cells_y: int, cells_size: int):
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

                elif 2 <= grid[row + self.camera.x][column + self.camera.y] <= 6:
                    color = pygame.Color("blue")

                elif 7 <= grid[row + self.camera.x][column + self.camera.y] <= 11:
                    color = pygame.Color("red")

                elif grid[row + self.camera.x][column + self.camera.y] != 0:  # shouldn't happen
                    color = pygame.Color("yellow")

                pygame.draw.rect(self.screen,
                                 color,
                                 [cells_size * row,
                                  cells_size * column,
                                  cells_size,
                                  cells_size])

    def __load_sprites(self):
        blue_infantry = pygame.image.load("src/Visualization/Sprites/infantry_blue.png").convert()
        red_infantry = pygame.image.load("src/Visualization/Sprites/infantry_red.png").convert()

        blue_cannon = pygame.image.load("src/Visualization/Sprites/canon_blue.png").convert()
        red_cannon = pygame.image.load("src/Visualization/Sprites/canon_red.png").convert()

        blue_cavalry = pygame.image.load("src/Visualization/Sprites/cavalry_blue.png").convert()
        red_cavalry = pygame.image.load("src/Visualization/Sprites/cavalry_red.png").convert()

        blue_rajter = pygame.image.load("src/Visualization/Sprites/rajter_blue.png").convert()
        red_rajter = pygame.image.load("src/Visualization/Sprites/rajter_red.png").convert()

        self.infantry_blue = [pygame.transform.scale(blue_infantry, (self.WINDOW_SIZE[0] / size, self.WINDOW_SIZE[1] / size)) for size in self.camera.allowed_width]
        for blue_infantry in self.infantry_blue:
            blue_infantry.set_colorkey((255, 255, 255))

        self.infantry_red = [pygame.transform.scale(red_infantry, (self.WINDOW_SIZE[0] / size, self.WINDOW_SIZE[1] / size)) for size in self.camera.allowed_width]
        for red_infantry in self.infantry_red:
            red_infantry.set_colorkey((255, 255, 255))

        # hussars
        self.hussar_blue = [pygame.transform.scale(blue_cavalry, (self.WINDOW_SIZE[0] / size, self.WINDOW_SIZE[1] / size))
                          for size in self.camera.allowed_width]
        for unit in self.hussar_blue:
            unit.set_colorkey((255, 255, 255))
        self.hussar_red = [pygame.transform.scale(red_cavalry, (self.WINDOW_SIZE[0] / size, self.WINDOW_SIZE[1] / size))
                          for size in self.camera.allowed_width]
        for unit in self.hussar_red:
            unit.set_colorkey((255, 255, 255))

        # rejters
        self.rejter_blue = [pygame.transform.scale(blue_rajter, (self.WINDOW_SIZE[0] / size, self.WINDOW_SIZE[1] / size))
                          for size in self.camera.allowed_width]
        for unit in self.rejter_blue:
            unit.set_colorkey((255, 255, 255))
        self.rejter_red = [pygame.transform.scale(red_rajter, (self.WINDOW_SIZE[0] / size, self.WINDOW_SIZE[1] / size))
                          for size in self.camera.allowed_width]
        for unit in self.rejter_red:
            unit.set_colorkey((255, 255, 255))

        # cannons
        self.cannon_blue = [
            pygame.transform.scale(blue_cannon, (self.WINDOW_SIZE[0] / size, self.WINDOW_SIZE[1] / size))
            for size in self.camera.allowed_width]
        for unit in self.cannon_blue:
            unit.set_colorkey((255, 255, 255))
        self.cannon_red = [pygame.transform.scale(red_cannon, (self.WINDOW_SIZE[0] / size, self.WINDOW_SIZE[1] / size))
                           for size in self.camera.allowed_width]
        for unit in self.cannon_red:
            unit.set_colorkey((255, 255, 255))

    def __prepare_texture(self):
        self.terrain_texture = pygame.Surface((400*32, 400*32))  # TODO: make it dynamic (size)
        self.terrain_texture.fill((123, 178, 0))
        tree = pygame.image.load("src/Visualization/Sprites/tree.png").convert()
        tree.set_colorkey((255, 255, 255))
        mountains = pygame.image.load("src/Visualization/Sprites/mountains.png").convert()
        river = pygame.image.load("src/Visualization/Sprites/river.png").convert()
        dark_grass = pygame.image.load("src/Visualization/Sprites/dark_grass.png").convert()

        terrain = self.terrain.get_grid()
        for i, row in enumerate(terrain):
            for j, elem in enumerate(row):
                if elem == 3:  # mountains
                    self.terrain_texture.blit(mountains, (i*32, j*32))
                elif elem == 10:  # river
                    self.terrain_texture.blit(river, (i*32, j*32))
                else:  # grass and default
                    self.terrain_texture.blit(tree, (i*32, j*32))
                    # if water is nearby, draw dark grass
                    if 0 < i < len(terrain) - 1 and 0 < j < len(terrain[0]) - 1:
                        if terrain[i-1][j] == 10 or terrain[i+1][j] == 10 or terrain[i][j-1] == 10 or terrain[i][j+1] == 10:
                            self.terrain_texture.blit(dark_grass, (i*32, j*32))




    def __render_terrain(self):
        screen_size = self.WINDOW_SIZE
        cells_x = self.camera.width
        cells_y = math.ceil(cells_x / screen_size[0] * screen_size[1])

        cells_size = math.ceil(screen_size[0] / cells_y)

        # grid = self.terrain.get_grid()
        # colors_dict = self.terrain.get_colors()
        # for row in range(cells_x):
        #     for column in range(cells_y):
        #         color = colors_dict.get(grid[row + self.camera.x][column + self.camera.y], (0, 0, 0))  # default color is black
        #         pygame.draw.rect(self.screen,
        #                          color,
        #                          [cells_size * row,
        #                           cells_size * column,
        #                           cells_size,
        #                           cells_size])

        terr_copy = self.terrain_texture.subsurface((self.camera.x * 32, self.camera.y * 32, cells_x*32, cells_y*32))
        scaled_x = cells_size * cells_x
        scaled_y = cells_size * cells_y
        terr_copy = pygame.transform.scale(terr_copy, (scaled_x, scaled_y))

        self.screen.blit(terr_copy, (0, 0))


    def __render_ui(self):
        for button in self.buttons:
            button.draw()

    def __main_loop(self):
        while True:
            grid = self.grid.get_grid()
            # input
            self.__input_handler()

            self.screen.fill(pygame.Color(200, 200, 200))
            # render terrain
            self.__render_terrain()
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
                self.step += 1
                self.grid.step()

            self.clock.tick(self.FPS)

        pygame.quit()
