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
from managers.round import Round
from spawners.zombie_spawner import ZombieSpawner
from managers.asset_manager import AssetManager


class GameState:
    PLAYING            = "playing"
    WAITING_NEXT_ROUND = "waiting_next_round"
    GAME_OVER          = "game_over"


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("Zombie Survival")

        self.font        = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 54)
        self.font_large  = pygame.font.Font(None, 80)

        self.assets = AssetManager()
        self._load_assets()

        self.zombie_spawner = ZombieSpawner(self.assets)

        self.clock   = pygame.time.Clock()
        self.running = True

        self._init_game_state()

    # ------------------------------------------------------------------
    # Setup
    # ------------------------------------------------------------------

    def _load_assets(self):
        """Carga todos los sprites una sola vez al iniciar el juego."""
        # Jugador
        self.assets.load_sheet(
            PLAYER_CONFIG["sprite"]["asset"],
            PLAYER_CONFIG["sprite"]["path"],
        )
        self.assets.load_sprite_by_index(
            PLAYER_CONFIG["sprite"]["asset"],
            PLAYER_CONFIG["sprite"]["asset"],
            0, 0,
            PLAYER_CONFIG["sprite"]["size"],
        )

        # Armas
        self.assets.load_sheet(WEAPON_SHEET["asset"], WEAPON_SHEET["path"])
        for weapon_name, weapon_data in WEAPONS.items():
            s = weapon_data["sprite"]
            self.assets.load_sprite_by_index(
                weapon_name, WEAPON_SHEET["asset"],
                s["col"], s["row"], WEAPON_SHEET["size"],
            )

        # Balas
        self.assets.load_sheet(BULLET_SHEET["asset"], BULLET_SHEET["path"])
        for bullet_name, bullet_data in BULLETS.items():
            s = bullet_data["sprite"]
            self.assets.load_sprite_by_index(
                bullet_name, bullet_data["asset"],
                s["col"], s["row"], bullet_data["size"],
            )

        # Zombies — aplica escala para tank (1.6x) y runner (0.75x)
        for zombie_name, zombie_data in ZOMBIES.items():
            sprite = zombie_data["sprite"]
            self.assets.load_sheet(sprite["asset"], sprite["path"])
            self.assets.load_sprite_by_index(
                zombie_name, sprite["asset"],
                0, 0, ZOMBIE_SPRITE_SIZE,
            )
            scale = zombie_data.get("scale", 1.0)
            if scale != 1.0:
                self.assets.scale_sprite(zombie_name, scale)

    def _init_game_state(self):
        """Inicializa (o reinicia) el estado del juego sin recargar assets."""
        self.player              = Player(PLAYER_CONFIG, self.assets)
        self.bullets             = []
        self.score               = 0
        self.current_round_number = 1
        self.state               = GameState.PLAYING
        self.round_completed_time = 0
        self.current_round       = self._create_round()

    def _create_round(self):
        return Round(self.current_round_number, self.zombie_spawner)

    def restart(self):
        """Detiene la ronda actual y reinicia el juego desde el principio."""
        self.current_round.stop()
        self._init_game_state()

    # ------------------------------------------------------------------
    # Game loop
    # ------------------------------------------------------------------

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        self.current_round.stop()
        pygame.quit()
        sys.exit()

    # ------------------------------------------------------------------
    # Events
    # ------------------------------------------------------------------

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and self.state == GameState.GAME_OVER:
                    self.restart()

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------

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

        score_gained = self.current_round.update(self.player)
        self.score += score_gained

        for bullet in self.bullets:
            bullet.update()

        self.clean_bullets()
        self.handle_bullet_zombie_collisions()

        if self.player.health <= 0:
            self.current_round.stop()
            self.state = GameState.GAME_OVER
            return

        if self.current_round.is_completed():
            self.current_round.stop()
            self.state = GameState.WAITING_NEXT_ROUND
            self.round_completed_time = pygame.time.get_ticks()

    def update_waiting_next_round(self):
        now = pygame.time.get_ticks()
        if now - self.round_completed_time >= ROUND_DELAY:
            self.current_round_number += 1
            self.current_round = self._create_round()
            self.state = GameState.PLAYING

    def update_game_over(self):
        pass

    # ------------------------------------------------------------------
    # Collisions
    # ------------------------------------------------------------------

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
            b for b in self.bullets
            if b.rect.right  > 0
            and b.rect.left  < SCREEN_WIDTH
            and b.rect.bottom > 0
            and b.rect.top   < SCREEN_HEIGHT
        ]

    # ------------------------------------------------------------------
    # Draw
    # ------------------------------------------------------------------

    def draw(self):
        self.screen.fill((30, 30, 30))

        self.player.draw(self.screen)
        self.current_round.draw(self.screen)

        for bullet in self.bullets:
            bullet.draw(self.screen)

        self.draw_hud()

        if self.state == GameState.WAITING_NEXT_ROUND:
            self.draw_round_completed()
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over()

        pygame.display.flip()

    def draw_hud(self):
        health_text = self.font.render(
            f"Vida: {self.player.health}", True, (255, 255, 255)
        )
        self.screen.blit(health_text, (20, 20))

        score_text = self.font.render(
            f"Puntaje: {self.score}", True, (255, 215, 0)
        )
        self.screen.blit(score_text, (20, 55))

        round_text = self.font.render(
            f"Ronda: {self.current_round_number}", True, (200, 200, 200)
        )
        round_rect = round_text.get_rect(topright=(SCREEN_WIDTH - 20, 20))
        self.screen.blit(round_text, round_rect)

    def draw_round_completed(self):
        cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

        overlay = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        self.screen.blit(overlay, (0, 0))

        title = self.font_medium.render(
            f"¡Ronda {self.current_round_number} completada!", True, (100, 230, 100)
        )
        self.screen.blit(title, title.get_rect(center=(cx, cy - 25)))

        score_surf = self.font.render(
            f"Puntaje: {self.score}", True, (255, 215, 0)
        )
        self.screen.blit(score_surf, score_surf.get_rect(center=(cx, cy + 30)))

        next_surf = self.font.render(
            "Preparate para la siguiente ronda...", True, (170, 170, 170)
        )
        self.screen.blit(next_surf, next_surf.get_rect(center=(cx, cy + 70)))

    def draw_game_over(self):
        cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

        overlay = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 190))
        self.screen.blit(overlay, (0, 0))

        # Título
        title = self.font_large.render("GAME OVER", True, (220, 60, 60))
        self.screen.blit(title, title.get_rect(center=(cx, cy - 100)))

        # Separador visual
        pygame.draw.line(
            self.screen, (180, 60, 60),
            (cx - 170, cy - 55), (cx + 170, cy - 55), 2
        )

        # Puntaje final
        score_surf = self.font_medium.render(
            f"Puntaje: {self.score}", True, (255, 215, 0)
        )
        self.screen.blit(score_surf, score_surf.get_rect(center=(cx, cy)))

        # Ronda alcanzada
        round_surf = self.font.render(
            f"Ronda alcanzada: {self.current_round_number}", True, (200, 200, 200)
        )
        self.screen.blit(round_surf, round_surf.get_rect(center=(cx, cy + 52)))

        # Prompt de reinicio
        restart_surf = self.font.render(
            "Presioná  R  para reiniciar", True, (130, 220, 130)
        )
        self.screen.blit(restart_surf, restart_surf.get_rect(center=(cx, cy + 105)))
