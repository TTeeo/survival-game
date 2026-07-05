import random
import pygame
import sys

from settings import (
    SCREEN_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, FPS,
    ROUND_DELAY,
    PLAYER_CONFIG,
    WEAPON_SHEET, WEAPONS,
    BULLET_SHEET, BULLETS,
    ZOMBIES, ZOMBIE_SPRITE_SIZE,
    MODIFIER_DROP_CHANCE,
    BOSS_ROUND_INTERVAL,
)
from entities.player import Player
from entities.modifier import (
    Modifier,
    MODIFIER_HEAL, MODIFIER_SPEED, MODIFIER_SHIELD,
    _LABELS as MODIFIER_LABELS,
)
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

        # SCALED mantiene la resolución lógica de 900x600 y la escala al monitor,
        # así ninguna coordenada del juego cambia al pasar a pantalla completa.
        self.screen = pygame.display.set_mode(SCREEN_SIZE, pygame.SCALED)
        pygame.display.set_caption("Zombie Survival")

        self.font        = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 54)
        self.font_large  = pygame.font.Font(None, 80)

        self.assets = AssetManager()
        self._load_assets()

        self.zombie_spawner = ZombieSpawner(self.assets)
        self.clock          = pygame.time.Clock()
        self.running        = True

        self._init_game_state()

    # ------------------------------------------------------------------
    # Setup
    # ------------------------------------------------------------------

    def _load_assets(self):
        self.assets.load_sheet(PLAYER_CONFIG["sprite"]["asset"],
                               PLAYER_CONFIG["sprite"]["path"])
        self.assets.load_sprite_by_index(
            PLAYER_CONFIG["sprite"]["asset"],
            PLAYER_CONFIG["sprite"]["asset"],
            0, 0, PLAYER_CONFIG["sprite"]["size"],
        )

        self.assets.load_sheet(WEAPON_SHEET["asset"], WEAPON_SHEET["path"])
        for wname, wdata in WEAPONS.items():
            s = wdata["sprite"]
            self.assets.load_sprite_by_index(
                wname, WEAPON_SHEET["asset"], s["col"], s["row"], WEAPON_SHEET["size"]
            )

        self.assets.load_sheet(BULLET_SHEET["asset"], BULLET_SHEET["path"])
        for bname, bdata in BULLETS.items():
            s = bdata["sprite"]
            self.assets.load_sprite_by_index(
                bname, bdata["asset"], s["col"], s["row"], bdata["size"]
            )

        for zname, zdata in ZOMBIES.items():
            sprite = zdata["sprite"]
            self.assets.load_sheet(sprite["asset"], sprite["path"])
            self.assets.load_sprite_by_index(
                zname, sprite["asset"], 0, 0, ZOMBIE_SPRITE_SIZE
            )
            scale = zdata.get("scale", 1.0)
            if scale != 1.0:
                self.assets.scale_sprite(zname, scale)

    def _init_game_state(self):
        self.player               = Player(PLAYER_CONFIG, self.assets)
        self.bullets              = []
        self.modifiers            = []
        self.score                = 0
        self.current_round_number = 1
        self.state                = GameState.PLAYING
        self.round_completed_time = 0
        self.current_round        = self._create_round()

    def _create_round(self):
        return Round(self.current_round_number, self.zombie_spawner, self.player)

    def restart(self):
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
                elif event.key == pygame.K_f:
                    pygame.display.toggle_fullscreen()

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

        score_gained, dead_positions = self.current_round.update(self.player)
        self.score += score_gained

        for pos in dead_positions:
            self._maybe_spawn_modifier(pos)

        for bullet in self.bullets:
            bullet.update()

        self.clean_bullets()
        self.handle_bullet_zombie_collisions()
        self._resolve_player_obstacle_collision()
        self._update_modifiers()

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
            self.modifiers = []           # limpiar drops entre rondas
            self.current_round_number += 1
            self.current_round = self._create_round()
            self.state = GameState.PLAYING

    def update_game_over(self):
        pass

    # ------------------------------------------------------------------
    # Modifiers / drops
    # ------------------------------------------------------------------

    def _maybe_spawn_modifier(self, pos):
        if random.random() < MODIFIER_DROP_CHANCE:
            mod_type = random.choice([MODIFIER_HEAL, MODIFIER_SPEED, MODIFIER_SHIELD])
            self.modifiers.append(Modifier(pos[0], pos[1], mod_type))

    def _update_modifiers(self):
        self.modifiers = [m for m in self.modifiers if not m.is_expired()]
        for mod in self.modifiers[:]:
            if self.player.rect.colliderect(mod.rect):
                self.player.apply_modifier(mod.type)
                self.modifiers.remove(mod)

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
        obstacles = self.current_round._obstacles
        self.bullets = [
            b for b in self.bullets
            if b.rect.right  > 0
            and b.rect.left  < SCREEN_WIDTH
            and b.rect.bottom > 0
            and b.rect.top   < SCREEN_HEIGHT
            and not any(b.rect.colliderect(obs.rect) for obs in obstacles)
        ]

    def _resolve_player_obstacle_collision(self):
        """Empuja al jugador fuera de los obstáculos en el eje de menor solapamiento."""
        for obs in self.current_round._obstacles:
            if not self.player.rect.colliderect(obs.rect):
                continue
            dx = self.player.rect.centerx - obs.rect.centerx
            dy = self.player.rect.centery - obs.rect.centery
            overlap_x = (self.player.rect.width  + obs.rect.width)  / 2 - abs(dx)
            overlap_y = (self.player.rect.height + obs.rect.height) / 2 - abs(dy)
            if overlap_x < overlap_y:
                self.player.x += overlap_x * (1 if dx > 0 else -1)
            else:
                self.player.y += overlap_y * (1 if dy > 0 else -1)
            self.player.rect.topleft = (int(self.player.x), int(self.player.y))

    # ------------------------------------------------------------------
    # Draw
    # ------------------------------------------------------------------

    def draw(self):
        self.screen.fill((30, 30, 30))

        self.player.draw(self.screen)
        self.current_round.draw(self.screen)

        for bullet in self.bullets:
            bullet.draw(self.screen)

        for mod in self.modifiers:
            mod.draw(self.screen)

        self.draw_hud()

        if self.state == GameState.WAITING_NEXT_ROUND:
            self.draw_round_completed()
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over()

        pygame.display.flip()

    def draw_hud(self):
        # Vida
        health_text = self.font.render(
            f"Vida: {self.player.health}", True, (255, 255, 255)
        )
        self.screen.blit(health_text, (20, 20))

        # Puntaje
        score_text = self.font.render(
            f"Puntaje: {self.score}", True, (255, 215, 0)
        )
        self.screen.blit(score_text, (20, 55))

        # Efectos activos del jugador
        now     = pygame.time.get_ticks()
        activos = [
            MODIFIER_LABELS.get(k, k)
            for k, v in self.player.active_modifiers.items()
            if v > now
        ]
        if activos:
            fx_text = self.font.render(
                "FX: " + "  ".join(activos), True, (130, 210, 255)
            )
            self.screen.blit(fx_text, (20, 90))

        # Ronda (esquina superior derecha)
        round_text = self.font.render(
            f"Ronda: {self.current_round_number}", True, (200, 200, 200)
        )
        self.screen.blit(round_text, round_text.get_rect(topright=(SCREEN_WIDTH - 20, 20)))

        # Indicador de ronda de jefe
        if self.current_round_number % BOSS_ROUND_INTERVAL == 0:
            boss_text = self.font.render("RONDA DE JEFE", True, (220, 60, 60))
            self.screen.blit(boss_text, boss_text.get_rect(topright=(SCREEN_WIDTH - 20, 55)))

    def draw_round_completed(self):
        cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

        overlay = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        self.screen.blit(overlay, (0, 0))

        title = self.font_medium.render(
            f"¡Ronda {self.current_round_number} completada!", True, (100, 230, 100)
        )
        self.screen.blit(title, title.get_rect(center=(cx, cy - 30)))

        score_surf = self.font.render(f"Puntaje: {self.score}", True, (255, 215, 0))
        self.screen.blit(score_surf, score_surf.get_rect(center=(cx, cy + 25)))

        # Aviso si la próxima es ronda de jefe
        next_num = self.current_round_number + 1
        if next_num % BOSS_ROUND_INTERVAL == 0:
            boss_warn = self.font.render(
                "⚠  PRÓXIMA RONDA: JEFE", True, (220, 80, 80)
            )
            self.screen.blit(boss_warn, boss_warn.get_rect(center=(cx, cy + 65)))
            bottom = cy + 105
        else:
            bottom = cy + 65

        next_surf = self.font.render(
            "Preparate para la siguiente ronda...", True, (170, 170, 170)
        )
        self.screen.blit(next_surf, next_surf.get_rect(center=(cx, bottom)))

    def draw_game_over(self):
        cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

        overlay = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 190))
        self.screen.blit(overlay, (0, 0))

        title = self.font_large.render("GAME OVER", True, (220, 60, 60))
        self.screen.blit(title, title.get_rect(center=(cx, cy - 100)))

        pygame.draw.line(
            self.screen, (180, 60, 60),
            (cx - 170, cy - 55), (cx + 170, cy - 55), 2
        )

        score_surf = self.font_medium.render(
            f"Puntaje: {self.score}", True, (255, 215, 0)
        )
        self.screen.blit(score_surf, score_surf.get_rect(center=(cx, cy)))

        round_surf = self.font.render(
            f"Ronda alcanzada: {self.current_round_number}", True, (200, 200, 200)
        )
        self.screen.blit(round_surf, round_surf.get_rect(center=(cx, cy + 52)))

        restart_surf = self.font.render(
            "Presioná  R  para reiniciar", True, (130, 220, 130)
        )
        self.screen.blit(restart_surf, restart_surf.get_rect(center=(cx, cy + 105)))
