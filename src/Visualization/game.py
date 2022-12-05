# move with keys: w a s d 
# zoom in/out with keys: k l

import math

import pygame
from camera import Camera
from UI import Button
from dummyGrid import GridTest
import grid

# FPS constants
FPS = 20
# update grid once per x frames:
update_rate = 40 # once per 2 seconds



# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Initialize pygame
pygame.init()

# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [800, 800]
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set title of screen
pygame.display.set_caption("Battle")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()


# UI
def ration_plus():
    global update_rate
    update_rate += 1


def ration_minus():
    global update_rate
    if update_rate > 2:
        update_rate -= 1

buttons = []
button = Button(325, 730, 70, 70, "+", screen, (100, 100, 100), ration_plus)
buttons.append(button)
button2 = Button(325+75, 730, 70, 70, "-", screen, (100, 100, 100), ration_minus)
buttons.append(button2)
camera = Camera(0, 0, 200, 50)  # camera size mush be the same as grid size

frames_counter = 0

grid_obj = GridTest(200)
for i in range(4):
    grid_obj.step()

grid_new = grid.GridPickle(300, 'logs.plk')

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Buttons
            for button in buttons:
                if button.rect().collidepoint(event.pos):
                    button.clicked()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_k:
                camera.zoom_in()
            elif event.key == pygame.K_l:
                camera.zoom_out()
            elif event.key == pygame.K_a:
                camera.move(-5, 0)
            elif event.key == pygame.K_d:
                camera.move(5, 0)
            elif event.key == pygame.K_w:
                camera.move(0, -5)
            elif event.key == pygame.K_s:
                camera.move(0, 5)

    # Set the screen background
    screen.fill(BLACK)

    # Draw the grid
    screen_size = screen.get_size()
    cells_x = camera.width
    cells_y = math.ceil(cells_x / screen_size[0] * screen_size[1])

    cells_size = math.ceil(screen_size[0] / cells_y)

    grid = grid_obj.grid
    grid = grid_new.get_grid()
    for row in range(cells_x):
        for column in range(cells_y):
            color = WHITE
            if row + camera.x < len(grid[0]) and column + camera.y < len(grid):
                if grid[row + camera.y][column + camera.x] == 1:
                    color = BLACK
                if grid[row + camera.y][column + camera.x] == 2:
                    color = GREEN
                if grid[row + camera.y][column + camera.x] == 3:
                    color = RED
            pygame.draw.rect(screen,
                             color,
                             [cells_size * column,
                              cells_size * row,
                              cells_size,
                              cells_size])

    grid_new.step()
    # Draw UI
    for button in buttons:
        button.draw()


    # TODO: refactor this part
    def text_objects(text):
        font = pygame.font.SysFont("comicsansms", 20)
        text_surface = font.render(text, True, (0, 0, 0))
        return text_surface, text_surface.get_rect()
    text_surf, text_rect = text_objects("Update once per " + str(update_rate / FPS) + " seconds")
    text_rect.center = (400, 700)
    screen.blit(text_surf, text_rect)

    if frames_counter % update_rate == 0:  # update grid once per UPDATE_RATE frames
        grid_obj.step()

    clock.tick(FPS)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    frames_counter += 1

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()
