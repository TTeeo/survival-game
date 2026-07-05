import queue
from concurrent.futures import ThreadPoolExecutor

from settings import (
    get_round_config,
    SCREEN_WIDTH, SCREEN_HEIGHT,
    OBSTACLES as _OBSTACLES_CFG,
    BOSS_ROUND_INTERVAL,
)
from spawners.zombie_spawner import SpawnerThread
from entities.obstacle import Obstacle
from entities.boss import BossZombie


class RoundState:
    SPAWNING  = "spawning"
    ACTIVE    = "active"
    COMPLETED = "completed"


class Round:
    def __init__(self, number, zombie_spawner, player=None):
        self.number        = number
        self.zombie_spawner = zombie_spawner

        self.state         = RoundState.SPAWNING
        self.zombies       = []
        self.spawned_count = 0
        self._stopped      = False

        self.load_config()

        # Obstáculos estáticos — compartidos con la IA de zombies
        self._obstacles = [Obstacle(*cfg) for cfg in _OBSTACLES_CFG]

        # --- Concurrencia ---
        self._spawn_queue = queue.Queue()
        self._executor    = ThreadPoolExecutor(
            max_workers=4, thread_name_prefix="zombie_ai"
        )
        self._spawner_thread = SpawnerThread(
            total_zombies=self.total_zombies,
            spawn_delay_ms=self.spawn_delay,
            zombie_weights=self.zombie_weights,
            spawn_queue=self._spawn_queue,
        )
        self._spawner_thread.start()

        # Jefe — spawnea al inicio de cada ronda múltiplo de BOSS_ROUND_INTERVAL
        if player and number % BOSS_ROUND_INTERVAL == 0:
            self._spawn_boss(player, zombie_spawner.assets)

    def load_config(self):
        config = get_round_config(self.number)
        self.total_zombies  = config["total_zombies"]
        self.spawn_delay    = config["spawn_delay"]
        self.zombie_weights = config["zombie_weights"]

    # ------------------------------------------------------------------
    # Boss
    # ------------------------------------------------------------------

    def _spawn_boss(self, player, assets):
        boss = BossZombie(
            x=SCREEN_WIDTH  // 2 - 32,
            y=SCREEN_HEIGHT // 2 - 32,
            assets=assets,
            player=player,
        )
        self.zombies.append(boss)

    # ------------------------------------------------------------------
    # Spawn queue (Producer-Consumer)
    # ------------------------------------------------------------------

    def _drain_spawn_queue(self):
        """Consume pedidos del SpawnerThread y crea Zombies en el hilo principal."""
        while True:
            try:
                zombie_type = self._spawn_queue.get_nowait()
            except queue.Empty:
                break
            zombie = self.zombie_spawner.spawn(zombie_type)
            self.zombies.append(zombie)
            self.spawned_count += 1
            if self.spawned_count >= self.total_zombies:
                self.state = RoundState.ACTIVE

    # ------------------------------------------------------------------
    # AI paralela (ThreadPoolExecutor)
    # ------------------------------------------------------------------

    def _compute_ai_parallel(self, player):
        """
        Fase de lectura paralela: cada zombie calcula su vector de movimiento.
        Trabaja sobre un snapshot y pasa los obstáculos para la evasión.
        BossZombie devuelve el vector pre-calculado por su propio hilo.
        """
        if not self.zombies:
            return [], []
        snapshot  = list(self.zombies)
        obstacles = self._obstacles
        futures   = [
            self._executor.submit(zombie.compute_movement, player, snapshot, obstacles)
            for zombie in snapshot
        ]
        movements = [f.result() for f in futures]
        return snapshot, movements

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------

    def update(self, player):
        self._drain_spawn_queue()

        snapshot, movements = self._compute_ai_parallel(player)

        # Fase secuencial: aplicar movimientos y ataques en el hilo principal
        for zombie, (move_x, move_y) in zip(snapshot, movements):
            if zombie in self.zombies:
                zombie.apply_movement(move_x, move_y)
                zombie.try_attack(player)

        # Detectar muertes antes de limpiar la lista
        dead_zombies   = [z for z in self.zombies if z.health <= 0]
        score_gained   = sum(z.score_value for z in dead_zombies)
        dead_positions = [(z.rect.centerx, z.rect.centery) for z in dead_zombies]

        # Detener hilo del boss si murió
        for z in dead_zombies:
            if isinstance(z, BossZombie):
                z.stop_thread()

        self.zombies = [z for z in self.zombies if z.health > 0]

        if self.state == RoundState.ACTIVE and len(self.zombies) == 0:
            self.state = RoundState.COMPLETED

        return score_gained, dead_positions

    # ------------------------------------------------------------------
    # Draw
    # ------------------------------------------------------------------

    def draw(self, screen):
        # Obstáculos primero (fondo)
        for obs in self._obstacles:
            obs.draw(screen)
        for zombie in self.zombies:
            zombie.draw(screen)

    def is_completed(self):
        return self.state == RoundState.COMPLETED

    # ------------------------------------------------------------------
    # Cleanup
    # ------------------------------------------------------------------

    def stop(self):
        """Detiene hilos de spawn, AI pool y boss (si existe). Idempotente."""
        if self._stopped:
            return
        self._stopped = True
        self._spawner_thread.stop()
        self._executor.shutdown(wait=False)
        for z in self.zombies:
            if isinstance(z, BossZombie):
                z.stop_thread()
