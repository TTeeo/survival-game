import pygame


class AssetManager:
  def __init__(self):
    self.sprites = {}
    self.sheets = {}


  def load_sheet(self, name, path):
    if name not in self.sheets:
      sheet = pygame.image.load(path).convert_alpha()
      self.sheets[name] = sheet

  def get_sprite(self, name):
    if name not in self.sprites:
      raise ValueError(f"Sprite '{name}' no cargado")
    return self.sprites[name]

  def get_sprite_by_index(self, sheet_name, col, row, size):
    x = col * size
    y = row * size
    return self.get_sprite(sheet_name, x, y, size)
  
  def load_sprite_by_index(self, name, sheet_name, col, row, size):
    if sheet_name not in self.sheets:
      raise ValueError(f"Sheet '{sheet_name}' no cargado")

    sheet = self.sheets[sheet_name]

    x = col * size
    y = row * size

    sprite = sheet.subsurface((x, y, size, size)).copy()

    self.sprites[name] = sprite

  def scale_sprite(self, name, scale):
    """Escala un sprite ya cargado. Usado para tank (1.6x) y runner (0.75x)."""
    sprite = self.sprites[name]
    w, h = sprite.get_size()
    new_size = (int(w * scale), int(h * scale))
    self.sprites[name] = pygame.transform.scale(sprite, new_size)