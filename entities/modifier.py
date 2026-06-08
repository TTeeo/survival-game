import pygame

MODIFIER_HEAL   = "HEAL"
MODIFIER_SPEED  = "SPEED"
MODIFIER_SHIELD = "SHIELD"

_LIFETIME_MS = 9000

_COLORS = {
    MODIFIER_HEAL:   (50,  210,  80),
    MODIFIER_SPEED:  (80,  160, 255),
    MODIFIER_SHIELD: (220, 180,  40),
}

_LABELS = {
    MODIFIER_HEAL:   "CURA +25",
    MODIFIER_SPEED:  "VEL x1.5",
    MODIFIER_SHIELD: "ESCUDO",
}


class Modifier:
    RADIUS = 10

    def __init__(self, x, y, modifier_type):
        self.x    = x
        self.y    = y
        self.type = modifier_type
        self.rect = pygame.Rect(
            x - self.RADIUS, y - self.RADIUS,
            self.RADIUS * 2,  self.RADIUS * 2,
        )
        self._color      = _COLORS[modifier_type]
        self._expires_at = pygame.time.get_ticks() + _LIFETIME_MS

    def is_expired(self):
        return pygame.time.get_ticks() > self._expires_at

    def draw(self, screen):
        pygame.draw.circle(screen, self._color,     (self.x, self.y), self.RADIUS)
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), self.RADIUS, 2)
