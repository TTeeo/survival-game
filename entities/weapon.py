import pygame

from settings import BULLETS
from entities.bullet import Bullet

class Weapon:
  def __init__(self, damage, cooldown, bullet_speed, projectiles, spread, range, image, bullet_image):
    self.damage = damage
    self.cooldown = cooldown
    self.bullet_speed = bullet_speed
    self.projectiles = projectiles
    self.spread = spread
    self.range = range
    self.image = image
    self.bullet_image = bullet_image
    self.last_shot_time = 0
  
  def can_shoot(self):
    now = pygame.time.get_ticks()
    return now - self.last_shot_time >= self.cooldown


  def shoot(self, x, y, direction):

    if not self.can_shoot():
      return None
    
    self.last_shot_time = pygame.time.get_ticks()

    return Bullet(
      x=x,
      y=y,
      direction=direction,
      speed=self.bullet_speed,
      damage=self.damage,
      image=self.bullet_image
    )