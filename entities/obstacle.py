import pygame


class Obstacle:
    _COLOR   = (100, 70, 40)
    _OUTLINE = (55, 35, 10)

    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self, screen):
        pygame.draw.rect(screen, self._COLOR,   self.rect)
        pygame.draw.rect(screen, self._OUTLINE, self.rect, 2)
