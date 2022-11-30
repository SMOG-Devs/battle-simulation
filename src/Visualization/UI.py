from typing import Callable
import pygame


def text_objects(text):
    font = pygame.font.SysFont("comicsansms", 20)
    text_surface = font.render(text, True, (255, 255, 255))
    return text_surface, text_surface.get_rect()


class Button:
    """Clickable button"""
    def __init__(self, x: int, y: int, width: int, height: int, text: str, screen: pygame.Surface, color: pygame.Color,
                 action=None):
        self.width = width
        self.height = height
        self.on_click = action
        self.text = text
        self.screen = screen
        self.color = color
        self.x = x
        self.y = y

    def draw(self):
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height))
        text_surf, text_rect = text_objects(self.text)
        text_rect.center = (self.x + self.width / 2, self.y + self.height / 2)
        self.screen.blit(text_surf, text_rect)

    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def clicked(self) -> None:
        if self.on_click is not None:
            self.on_click()
