from settings import WEAPONS
from entities.weapon import Weapon


class WeaponFactory:
  @staticmethod
  def create(weapon_type, assets):
    data = WEAPONS[weapon_type]

    image = assets.get_sprite(weapon_type)

    bullet_image = assets.get_sprite(data["bullet_type"])
    return Weapon(
      damage=data["damage"],
      cooldown=data["cooldown"],
      bullet_speed=data["bullet_speed"],
      projectiles=data["projectiles"],
      spread=data["spread"],
      range=data["range"],
      image=image,
      bullet_image=bullet_image
    )