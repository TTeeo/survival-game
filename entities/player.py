import pygame

from settings import SCREEN_WIDTH, SCREEN_HEIGHT, DIR_DOWN, DIR_UP, DIR_LEFT, DIR_RIGHT
from factories.weapon_factory import WeaponFactory



class Player:
  def __init__(self, config, assets):
    self.asset = config["sprite"]["asset"]
    self.size = config["sprite"]["size"]

    self.x, self.y = config["init"]["pos"]

    self.health = config["stats"]["health"]
    self.speed = config["stats"]["speed"]

    self.image = assets.get_sprite(self.asset)
    self.direction = DIR_LEFT
    self.weapon = WeaponFactory.create(config["init"]["weapon"], assets)

    self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

  def handle_input(self):
    keys = pygame.key.get_pressed()

    dx = 0
    dy = 0

    if keys[pygame.K_w]:
      dy -= self.speed
      self.direction = DIR_UP
    if keys[pygame.K_s]:
      dy += self.speed
      self.direction = DIR_DOWN
    if keys[pygame.K_a]:
      dx -= self.speed
      self.direction = DIR_LEFT
    if keys[pygame.K_d]:
      dx += self.speed
      self.direction = DIR_RIGHT

    self.x += dx
    self.y += dy

    self.x = max(0, min(self.x, SCREEN_WIDTH - self.size))
    self.y = max(0, min(self.y, SCREEN_HEIGHT - self.size))

    self.rect.topleft = (self.x, self.y)

  def update(self):
    self.handle_input()

  def draw(self, screen):
    screen.blit(self.image, self.rect)

    weapon_x = self.rect.centerx
    weapon_y = self.rect.centery

    screen.blit(self.weapon.image, (weapon_x, weapon_y))


  def shoot(self):
    dir_x, dir_y = 0, 0

    if self.direction == DIR_UP:
      dir_y = -1
    elif self.direction == DIR_DOWN:
      dir_y = 1
    elif self.direction == DIR_LEFT:
      dir_x = -1
    elif self.direction == DIR_RIGHT:
      dir_x = 1

    return self.weapon.shoot(
      self.rect.centerx,
      self.rect.centery,
      (dir_x, dir_y)
    )
  def take_damage(self, amount):
    self.health -= amount

    if self.health <= 0:
      self.die()

  def die(self):
    print("Player died")