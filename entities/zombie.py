import pygame
import random

from settings import (
	ZOMBIE_SEPARATION_DISTANCE, ZOMBIE_SEPARATION_FORCE,
	ZOMBIE_OBSTACLE_AVOID_DISTANCE, ZOMBIE_OBSTACLE_AVOID_FORCE,
)


class Zombie:
	def __init__(self, x, y, speed, health, damage, image, score_value=0):
		self.x = x
		self.y = y
		self.speed = speed
		self.health = health
		self.damage = damage
		self.image = image
		self.score_value = score_value

		# El tamaño se deriva de la imagen para soportar zombies escalados (tank, runner).
		self.size = image.get_width()

		self.rect = self.image.get_rect(topleft=(self.x, self.y))
		self.attack_cooldown = 1000
		self.last_attack_time = 0
		self.hit_flash_until = 0

	def compute_movement(self, player, zombies, obstacles=None):
		"""
		Calcula el vector de movimiento sin modificar estado.
		Solo lectura: seguro para ejecutarse en paralelo con ThreadPoolExecutor.
		"""
		return self.get_movement(player, zombies, obstacles)

	def apply_movement(self, move_x, move_y):
		"""
		Aplica el vector calculado. Siempre ejecutado en el hilo principal
		para evitar escrituras concurrentes sobre x, y y rect.
		"""
		self.x += move_x * self.speed
		self.y += move_y * self.speed
		self.sync_rect()

	def update(self, player, zombies):
		move_x, move_y = self.compute_movement(player, zombies)
		self.apply_movement(move_x, move_y)
		self.try_attack(player)

	def attack(self, player):
		now = pygame.time.get_ticks()

		if now - self.last_attack_time >= self.attack_cooldown:
			player.take_damage(self.damage)
			self.last_attack_time = now

	def take_damage(self, amount):
		self.health -= amount
		self.hit_flash_until = pygame.time.get_ticks() + 120

		if self.health <= 0:
			self.die()

	def draw(self, screen):
		if pygame.time.get_ticks() < self.hit_flash_until:
			flash = self.image.copy()
			flash.fill((255, 255, 255, 0), special_flags=pygame.BLEND_RGBA_ADD)
			screen.blit(flash, (self.x, self.y))
		else:
			screen.blit(self.image, (self.x, self.y))

	def die(self):
		self.is_alive = False
		self.health = 0

	def move(self, player, zombies):
		move_x, move_y = self.get_movement(player, zombies)

		self.x += move_x * self.speed
		self.y += move_y * self.speed

	def get_movement(self, player, zombies, obstacles=None):
		move_x, move_y = self.get_direction_to_player(player)
		sep_x, sep_y   = self.get_separation_between_zombies(zombies)
		move_x += sep_x
		move_y += sep_y

		if obstacles:
			avoid_x, avoid_y = self.get_obstacle_avoidance(obstacles)
			move_x += avoid_x
			move_y += avoid_y

		chaos_x, chaos_y = self.get_chaos()
		move_x += chaos_x
		move_y += chaos_y

		return self.normalize(move_x, move_y)

	def get_obstacle_avoidance(self, obstacles):
		"""Fuerza de repulsión frente a obstáculos — ejecutado en paralelo (solo lectura)."""
		avoid_x = avoid_y = 0.0
		cx = self.x + self.size / 2
		cy = self.y + self.size / 2
		for obs in obstacles:
			closest_x = max(obs.rect.left, min(cx, obs.rect.right))
			closest_y = max(obs.rect.top,  min(cy, obs.rect.bottom))
			dx = cx - closest_x
			dy = cy - closest_y
			dist = (dx**2 + dy**2) ** 0.5
			if 0 < dist < ZOMBIE_OBSTACLE_AVOID_DISTANCE:
				avoid_x += (dx / dist) * ZOMBIE_OBSTACLE_AVOID_FORCE
				avoid_y += (dy / dist) * ZOMBIE_OBSTACLE_AVOID_FORCE
		return avoid_x, avoid_y

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
