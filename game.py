from entities import bullet
import pygame
import sys

from settings import (
	SCREEN_SIZE,
	SCREEN_WIDTH,
	SCREEN_HEIGHT,
	FPS,
	ROUND_DELAY,
	PLAYER_CONFIG,
	WEAPON_SHEET,
	WEAPONS,
	BULLET_SHEET,
	BULLETS,
	ZOMBIES,
	ZOMBIE_SPRITE_SIZE,
)
from entities.player import Player
from entities.bullet import Bullet
from round import Round
from zombie_spawner import ZombieSpawner
from managers.asset_manager import AssetManager



class GameState:
	PLAYING = "playing"
	WAITING_NEXT_ROUND = "waiting_next_round"
	GAME_OVER = "game_over"


class Game:
	def __init__(self):
		pygame.init()

		self.screen = pygame.display.set_mode(SCREEN_SIZE)
		pygame.display.set_caption("Zombie Survival")
		self.font = pygame.font.Font(None, 36)

		self.assets = AssetManager()

	
		# PLAYER
		self.assets.load_sheet(
			PLAYER_CONFIG["sprite"]["asset"],
			PLAYER_CONFIG["sprite"]["path"]
		)

		self.assets.load_sprite_by_index(
			PLAYER_CONFIG["sprite"]["asset"],
			PLAYER_CONFIG["sprite"]["asset"],
			0,
			0,
			PLAYER_CONFIG["sprite"]["size"]
		)


		# WEAPONS
		self.assets.load_sheet(
			WEAPON_SHEET["asset"],
			WEAPON_SHEET["path"]
		)

		for weapon_name, weapon_data in WEAPONS.items():
			sprite = weapon_data["sprite"]

			self.assets.load_sprite_by_index(
				weapon_name,
				WEAPON_SHEET["asset"],
				sprite["col"],
				sprite["row"],
				WEAPON_SHEET["size"]
			)


		# BULLETS
		self.assets.load_sheet(
			BULLET_SHEET["asset"],
			BULLET_SHEET["path"]
		)

		for bullet_name, bullet_data in BULLETS.items():
			sprite = bullet_data["sprite"]

			self.assets.load_sprite_by_index(
				bullet_name,
				bullet_data["asset"],
				sprite["col"],
				sprite["row"],
				bullet_data["size"]
			)


		# ZOMBIES
		for zombie_name, zombie_data in ZOMBIES.items():
			sprite = zombie_data["sprite"]

			self.assets.load_sheet(
				sprite["asset"],
				sprite["path"]
			)

			self.assets.load_sprite_by_index(
				zombie_name,
				sprite["asset"],
				0,
				0,
				ZOMBIE_SPRITE_SIZE
			)
		


		self.clock = pygame.time.Clock()
		self.running = True
		self.state = GameState.PLAYING

		self.player = Player(PLAYER_CONFIG, self.assets)
		self.bullets = []
		self.zombie_spawner = ZombieSpawner(self.assets)
		self.score = 0
		self.current_round_number = 1
		self.current_round = self.create_round()

		self.round_completed_time = 0

	def create_round(self):
		return Round(
			self.current_round_number,
			self.zombie_spawner
		)

	def run(self):
		while self.running:
			self.handle_events()
			self.update()
			self.draw()
			self.clock.tick(FPS)

		pygame.quit()
		sys.exit()

	def handle_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False

	def update(self):
		if self.state == GameState.PLAYING:
			self.update_playing()

		elif self.state == GameState.WAITING_NEXT_ROUND:
			self.update_waiting_next_round()

		elif self.state == GameState.GAME_OVER:
			self.update_game_over()

	def update_playing(self):
		self.player.update()

		keys = pygame.key.get_pressed()

		if keys[pygame.K_SPACE]:
			bullet = self.player.shoot()
			if bullet:
				self.bullets.append(bullet)

		self.current_round.update(self.player)

		for bullet in self.bullets:
			bullet.update()

		self.clean_bullets();
		self.handle_bullet_zombie_collisions()

		if self.player.health <= 0:
			self.state = GameState.GAME_OVER
			return

		if self.current_round.is_completed():
			self.state = GameState.WAITING_NEXT_ROUND
			self.round_completed_time = pygame.time.get_ticks()

	def update_waiting_next_round(self):
		now = pygame.time.get_ticks()

		if now - self.round_completed_time >= ROUND_DELAY:
			self.next_round()
			self.state = GameState.PLAYING

	def update_game_over(self):
		pass


	def handle_bullet_zombie_collisions(self):
		for bullet in self.bullets[:]:
			for zombie in self.current_round.zombies[:]:
				if bullet.rect.colliderect(zombie.rect):
					zombie.take_damage(bullet.damage)

					if bullet in self.bullets:
						self.bullets.remove(bullet)

					break
	  

	def clean_bullets(self):
		self.bullets = [
			bullet for bullet in self.bullets
			if bullet.rect.right > 0
			and bullet.rect.left < SCREEN_WIDTH
			and bullet.rect.bottom > 0
			and bullet.rect.top < SCREEN_HEIGHT
		]
	def next_round(self):
		self.current_round_number += 1
		self.current_round = self.create_round()

	def draw(self):
		self.screen.fill((30, 30, 30))

		self.player.draw(self.screen)
		self.current_round.draw(self.screen)

		for bullet in self.bullets:
			bullet.draw(self.screen)
		self.draw_hud()

		pygame.display.flip()

	def draw_hud(self):
		health_text = self.font.render(
			f"Vida: {self.player.health}", True, (255, 255, 255)
		)

		self.screen.blit(health_text, (20, 20))