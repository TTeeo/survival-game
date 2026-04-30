import pygame
import random

from settings import ZOMBIE_SEPARATION_DISTANCE, ZOMBIE_SEPARATION_FORCE, ZOMBIE_SPRITE_SIZE


class Zombie:
	def __init__(self, x, y, speed, health, damage, image):
		self.x = x
		self.y = y
		self.speed = speed
		self.health = health
		self.damage = damage
		self.image = image
	
		self.size = ZOMBIE_SPRITE_SIZE  


		self.rect = self.image.get_rect(topleft=(self.x, self.y))
		self.attack_cooldown = 1000
		self.last_attack_time = 0

	def update(self, player, zombies):
		self.move(player, zombies)
		self.sync_rect()
		self.try_attack(player)

	def attack(self, player):
		now = pygame.time.get_ticks()

		if now - self.last_attack_time >= self.attack_cooldown:
			player.health -= self.damage
			self.last_attack_time = now

	def take_damage(self, amount):
		self.health -= amount

		if self.health <= 0:
			self.die()

	def draw(self, screen):
		screen.blit(self.image, (self.x, self.y))

	def die(self):
		self.is_alive = False
		self.health = 0

	def move(self, player, zombies):
		move_x, move_y = self.get_movement(player, zombies)

		self.x += move_x * self.speed
		self.y += move_y * self.speed

	def get_movement(self, player, zombies):
		move_x, move_y = self.get_direction_to_player(player)
		sep_x, sep_y = self.get_separation_between_zombies(zombies)

		move_x += sep_x
		move_y += sep_y

		chaos_x, chaos_y = self.get_chaos()
		move_x += chaos_x
		move_y += chaos_y

		return self.normalize(move_x, move_y)

	def get_direction_to_player(self, player):
		dx = player.x - self.x
		dy = player.y - self.y

		return self.normalize(dx, dy)

	def get_separation_between_zombies(self, zombies):
		sep_x = 0
		sep_y = 0

		for other in zombies:
			if other == self:
				continue

			dx = self.x - other.x
			dy = self.y - other.y
			distance = (dx**2 + dy**2) ** 0.5

			if distance != 0 and distance < ZOMBIE_SEPARATION_DISTANCE:
				sep_x += (dx / distance) * ZOMBIE_SEPARATION_FORCE
				sep_y += (dy / distance) * ZOMBIE_SEPARATION_FORCE

		return sep_x, sep_y

	def normalize(self, x, y):
		distance = (x**2 + y**2) ** 0.5

		if distance == 0:
			return 0, 0

		return x / distance, y / distance

	def get_chaos(self):
		return (random.uniform(-0.2, 0.2), random.uniform(-0.2, 0.2))

	def sync_rect(self):
		self.rect.topleft = (self.x, self.y)

	def try_attack(self, player):
		if self.rect.colliderect(player.rect):
			self.attack(player)
