import pygame
import threading

from settings import SCREEN_WIDTH, SCREEN_HEIGHT, DIR_DOWN, DIR_UP, DIR_LEFT, DIR_RIGHT
from factories.weapon_factory import WeaponFactory
from entities.modifier import MODIFIER_HEAL, MODIFIER_SPEED, MODIFIER_SHIELD


class Player:
  def __init__(self, config, assets):
    self.asset = config["sprite"]["asset"]
    self.size  = config["sprite"]["size"]

    self.x, self.y = config["init"]["pos"]

    self.max_health = config["stats"]["health"]
    self.health     = self.max_health
    self.speed      = config["stats"]["speed"]

    self.image     = assets.get_sprite(self.asset)
    self.direction = DIR_LEFT
    self.weapon    = WeaponFactory.create(config["init"]["weapon"], assets)

    self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    self._health_lock = threading.Lock()
    # {modifier_type: expira_en_ms}  — efectos temporales activos
    self.active_modifiers = {}

  # ------------------------------------------------------------------
  # Input & update
  # ------------------------------------------------------------------

  @property
  def _effective_speed(self):
    """Velocidad real considerando el efecto SPEED activo."""
    if "SPEED" in self.active_modifiers:
      if pygame.time.get_ticks() < self.active_modifiers["SPEED"]:
        return int(self.speed * 1.5)
      else:
        del self.active_modifiers["SPEED"]
    return self.speed

  def handle_input(self):
    keys = pygame.key.get_pressed()
    spd  = self._effective_speed

    dx = dy = 0
    if keys[pygame.K_w]: dy -= spd; self.direction = DIR_UP
    if keys[pygame.K_s]: dy += spd; self.direction = DIR_DOWN
    if keys[pygame.K_a]: dx -= spd; self.direction = DIR_LEFT
    if keys[pygame.K_d]: dx += spd; self.direction = DIR_RIGHT

    self.x += dx
    self.y += dy
    self.x = max(0, min(self.x, SCREEN_WIDTH  - self.size))
    self.y = max(0, min(self.y, SCREEN_HEIGHT - self.size))
    self.rect.topleft = (self.x, self.y)

  def update(self):
    self.handle_input()
    self._clean_expired_modifiers()

  def _clean_expired_modifiers(self):
    now = pygame.time.get_ticks()
    self.active_modifiers = {k: v for k, v in self.active_modifiers.items() if v > now}

  # ------------------------------------------------------------------
  # Modifiers
  # ------------------------------------------------------------------

  def apply_modifier(self, mod_type):
    now = pygame.time.get_ticks()
    if mod_type == MODIFIER_HEAL:
      self.health = min(self.health + 50, self.max_health)
    elif mod_type == MODIFIER_SPEED:
      self.active_modifiers[MODIFIER_SPEED]  = now + 8_000
    elif mod_type == MODIFIER_SHIELD:
      self.active_modifiers[MODIFIER_SHIELD] = now + 10_000

  # ------------------------------------------------------------------
  # Combat
  # ------------------------------------------------------------------

  def take_damage(self, amount):
    """
    Lock garantiza atomicidad en modificación de health.
    El SHIELD absorbe el próximo golpe y se consume.
    """
    with self._health_lock:
      now = pygame.time.get_ticks()
      if MODIFIER_SHIELD in self.active_modifiers:
        if self.active_modifiers[MODIFIER_SHIELD] > now:
          del self.active_modifiers[MODIFIER_SHIELD]
          return  # daño absorbido por el escudo
      self.health -= amount


  # ------------------------------------------------------------------
  # Draw
  # ------------------------------------------------------------------

  def draw(self, screen):
    screen.blit(self.image, self.rect)
    screen.blit(self.weapon.image, (self.rect.centerx, self.rect.centery))

  # ------------------------------------------------------------------
  # Shoot
  # ------------------------------------------------------------------

  def shoot(self):
    dir_x = dir_y = 0
    if self.direction == DIR_UP:    dir_y = -1
    elif self.direction == DIR_DOWN:  dir_y =  1
    elif self.direction == DIR_LEFT:  dir_x = -1
    elif self.direction == DIR_RIGHT: dir_x =  1

    return self.weapon.shoot(
      self.rect.centerx,
      self.rect.centery,
      (dir_x, dir_y),
    )
