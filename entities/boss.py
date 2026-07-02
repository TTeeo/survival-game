import pygame
import threading
import time

from entities.zombie import Zombie
from settings import ZOMBIE_SPRITE_SIZE, BOSS_CONFIG, ZOMBIE_BASIC


class BossThread(threading.Thread):
    """
    Hilo dedicado a la máquina de estados del Boss.

    Corre de forma independiente al game loop y actualiza
    el vector de movimiento del Boss via Lock compartido.

    Estados:
      CHASE      → persecución lenta, ~3.5 s
      TELEGRAPH  → pausa breve (advertencia visual) antes de embestir, ~0.7 s
      CHARGE     → embestida rápida en dirección fijada al inicio, ~0.9 s
    """

    _CHASE_DURATION     = 3.5
    _TELEGRAPH_DURATION = 0.7
    _CHARGE_DURATION    = 0.9
    _TICK_INTERVAL      = 0.05  # 20 Hz de actualización de IA

    def __init__(self, boss, player):
        super().__init__(daemon=True, name="BossThread")
        self._boss        = boss
        self._player      = player
        self._stop_event  = threading.Event()
        self._state       = "CHASE"
        self._state_start = time.time()
        self._charge_dir  = (0.0, 0.0)

    @property
    def state(self):
        return self._state

    def run(self):
        while not self._stop_event.is_set():
            self._tick()
            self._stop_event.wait(timeout=self._TICK_INTERVAL)

    def _tick(self):
        elapsed = time.time() - self._state_start

        if self._state == "CHASE":
            self._boss.set_ai(self._dir_to_player(), speed_mult=1.0)
            if elapsed >= self._CHASE_DURATION:
                self._transition("TELEGRAPH")

        elif self._state == "TELEGRAPH":
            # Boss se detiene — señal visual para el jugador
            self._boss.set_ai((0.0, 0.0), speed_mult=0.0)
            if elapsed >= self._TELEGRAPH_DURATION:
                self._charge_dir = self._dir_to_player()
                self._transition("CHARGE")

        elif self._state == "CHARGE":
            # Embestida en dirección fija a alta velocidad
            self._boss.set_ai(self._charge_dir, speed_mult=4.5)
            if elapsed >= self._CHARGE_DURATION:
                self._transition("CHASE")

    def _dir_to_player(self):
        dx = self._player.x - self._boss.x
        dy = self._player.y - self._boss.y
        dist = (dx**2 + dy**2) ** 0.5
        return (dx / dist, dy / dist) if dist else (0.0, 0.0)

    def _transition(self, new_state):
        self._state       = new_state
        self._state_start = time.time()

    def stop(self):
        self._stop_event.set()


class BossZombie(Zombie):
    """
    Zombie jefe con hilo de IA dedicado (BossThread).

    Integración con el ThreadPoolExecutor existente:
      - compute_movement() es llamado desde el pool como cualquier zombie,
        pero devuelve el vector pre-calculado por BossThread bajo Lock.
      - apply_movement() usa el vector ya escalado (ignora self.speed).

    El Lock garantiza exclusión mutua entre el BossThread (escritura)
    y los workers del ThreadPoolExecutor (lectura).
    """

    _STATE_COLORS = {
        "CHASE":     ( 180,  20,  20),  # rojo oscuro — persecución
        "TELEGRAPH": ( 255, 200,   0),  # amarillo    — advertencia
        "CHARGE":    ( 255,  40,  40),  # rojo vivo   — embestida
    }

    def __init__(self, x, y, assets, player):
        # Sprite base escalado 2× con tinte rojizo
        base  = assets.get_sprite(ZOMBIE_BASIC)
        size  = ZOMBIE_SPRITE_SIZE * 2
        image = pygame.transform.scale(base, (size, size))
        tinted = image.copy()
        tinted.fill((90, 0, 0, 0), special_flags=pygame.BLEND_RGB_ADD)

        super().__init__(
            x=x, y=y,
            speed=BOSS_CONFIG["speed"],
            health=BOSS_CONFIG["health"],
            damage=BOSS_CONFIG["damage"],
            image=tinted,
            score_value=BOSS_CONFIG["score_value"],
        )

        self._max_health = BOSS_CONFIG["health"]

        # Estado compartido protegido por Lock
        self._ai_lock       = threading.Lock()
        self._ai_direction  = (0.0, 0.0)
        self._ai_speed_mult = 1.0

        self._boss_thread = BossThread(self, player)
        self._boss_thread.start()

    # ------------------------------------------------------------------
    # Escritura desde BossThread (bajo Lock)
    # ------------------------------------------------------------------

    def set_ai(self, direction, speed_mult):
        with self._ai_lock:
            self._ai_direction  = direction
            self._ai_speed_mult = speed_mult

    # ------------------------------------------------------------------
    # Lectura desde ThreadPoolExecutor (bajo Lock)
    # ------------------------------------------------------------------

    def compute_movement(self, player, zombies, obstacles=None):
        with self._ai_lock:
            vx, vy = self._ai_direction
            mult   = self._ai_speed_mult
        return (vx * mult, vy * mult)

    def apply_movement(self, move_x, move_y):
        """El vector ya incluye la magnitud deseada; se escala solo por self.speed."""
        self.x += move_x * self.speed
        self.y += move_y * self.speed
        self.sync_rect()

    # ------------------------------------------------------------------
    # Visual
    # ------------------------------------------------------------------

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

        state = self._boss_thread.state
        color = self._STATE_COLORS.get(state, (180, 20, 20))
        pygame.draw.rect(screen, color, self.rect, 3)

        # Barra de vida encima del sprite
        hp_pct = max(self.health / self._max_health, 0)
        bar_w  = self.size
        pygame.draw.rect(screen, (80, 0, 0),
                         (self.x, self.y - 12, bar_w, 7))
        pygame.draw.rect(screen, (220, 30, 30),
                         (self.x, self.y - 12, int(bar_w * hp_pct), 7))

    # ------------------------------------------------------------------
    # Cleanup
    # ------------------------------------------------------------------

    def stop_thread(self):
        self._boss_thread.stop()
