import queue
from concurrent.futures import ThreadPoolExecutor

from settings import get_round_config
from spawners.zombie_spawner import SpawnerThread


class RoundState:
    SPAWNING = "spawning"
    ACTIVE = "active"
    COMPLETED = "completed"


class Round:
    def __init__(self, number, zombie_spawner):
        self.number = number
        self.zombie_spawner = zombie_spawner

        self.state = RoundState.SPAWNING
        self.zombies = []
        self.spawned_count = 0
        self._stopped = False

        self.load_config()

        # --- Concurrencia ---
        # Queue thread-safe: el SpawnerThread pone tipos de zombie,
        # el hilo principal los consume y crea los objetos.
        self._spawn_queue = queue.Queue()

        # Pool de hilos para calcular la IA de cada zombie en paralelo.
        # max_workers=4 es suficiente para la cantidad de zombies esperados.
        self._executor = ThreadPoolExecutor(
            max_workers=4,
            thread_name_prefix="zombie_ai"
        )

        # Hilo productor: gestiona el timing de spawn fuera del game loop.
        self._spawner_thread = SpawnerThread(
            total_zombies=self.total_zombies,
            spawn_delay_ms=self.spawn_delay,
            zombie_weights=self.zombie_weights,
            spawn_queue=self._spawn_queue,
        )
        self._spawner_thread.start()

    def load_config(self):
        config = get_round_config(self.number)
        self.total_zombies = config["total_zombies"]
        self.spawn_delay = config["spawn_delay"]
        self.zombie_weights = config["zombie_weights"]

    def _drain_spawn_queue(self):
        """
        Patrón Producer-Consumer: consume todos los pedidos pendientes del
        SpawnerThread y crea los objetos Zombie en el hilo principal.
        La creación de sprites de pygame debe ocurrir en el hilo principal.
        """
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

    def _compute_ai_parallel(self, player):
        """
        Fase de lectura paralela: cada zombie calcula su vector de movimiento
        de forma independiente usando el ThreadPoolExecutor.

        Se trabaja sobre un snapshot inmutable de la lista de zombies para
        evitar condiciones de carrera mientras los futures se ejecutan.
        Retorna (snapshot, lista_de_movimientos) sincronizados por índice.
        """
        if not self.zombies:
            return [], []

        snapshot = list(self.zombies)
        futures = [
            self._executor.submit(zombie.compute_movement, player, snapshot)
            for zombie in snapshot
        ]
        movements = [f.result() for f in futures]
        return snapshot, movements

    def update(self, player):
        # 1. Consumir pedidos de spawn del hilo productor
        self._drain_spawn_queue()

        # 2. Fase paralela: calcular vectores de movimiento de cada zombie
        snapshot, movements = self._compute_ai_parallel(player)

        # 3. Fase secuencial (hilo principal): aplicar movimientos y ataques
        for zombie, (move_x, move_y) in zip(snapshot, movements):
            if zombie in self.zombies:
                zombie.apply_movement(move_x, move_y)
                zombie.try_attack(player)

        # 4. Detectar zombies recién eliminados y acumular puntaje
        score_gained = sum(z.score_value for z in self.zombies if z.health <= 0)
        self.zombies = [z for z in self.zombies if z.health > 0]

        if self.state == RoundState.ACTIVE and len(self.zombies) == 0:
            self.state = RoundState.COMPLETED

        return score_gained

    def draw(self, screen):
        for zombie in self.zombies:
            zombie.draw(screen)

    def is_completed(self):
        return self.state == RoundState.COMPLETED

    def stop(self):
        """
        Detiene ordenadamente el hilo de spawn y el pool de AI.
        Idempotente: puede llamarse múltiples veces sin error.
        """
        if self._stopped:
            return
        self._stopped = True
        self._spawner_thread.stop()
        self._executor.shutdown(wait=False)
