from settings import ZOMBIES
from entities.zombie import Zombie


class ZombieFactory:

  @staticmethod
  def create(zombie_type, x, y, assets):
    data = ZOMBIES[zombie_type]

    image = assets.get_sprite(zombie_type)

    return Zombie(
      x=x,
      y=y,
      speed=data["stats"]["speed"],
      health=data["stats"]["health"],
      damage=data["stats"]["damage"],
      image=image,
      score_value=data["stats"]["score_value"],
    )