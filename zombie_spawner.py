import random
from settings import SPAWN_POINTS
from factories.zombie_factory import ZombieFactory


class ZombieSpawner:
	def __init__(self, assets):
		self.assets = assets
	def spawn(self, zombie_type):
		x, y = random.choice(SPAWN_POINTS)
		return ZombieFactory.create(zombie_type, x, y, self.assets)
