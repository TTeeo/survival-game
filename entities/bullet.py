class Bullet:
  def __init__(self, x, y, direction, speed, damage, image):
    self.x = x
    self.y = y
    self.dx, self.dy = direction
    self.speed = speed
    self.damage = damage
    self.image = image
    self.rect = self.image.get_rect(center=(x, y))

  def update(self):
    self.x += self.dx * self.speed
    self.y += self.dy * self.speed
    self.rect.center = (self.x, self.y)

  def draw(self, screen):
    screen.blit(self.image, self.rect)