import random
import threading
import queue

from settings import SPAWN_POINTS
from factories.zombie_factory import ZombieFactory


class SpawnerThread(threading.Thread):
    """
    Hilo productor (Producer): genera pedidos de spawn a intervalos regulares.
    Se comunica con el hilo principal via queue.Queue thread-safe.
    Usa threading.Event para poder detenerse limpiamente antes de terminar.
    """

    def __init__(self, total_zombies, spawn_delay_ms, zombie_weights, spawn_queue):
        super().__init__(daemon=True, name="SpawnerThread")
        self.total_zombies = total_zombies
        self.spawn_delay = spawn_delay_ms / 1000.0
        self.zombie_weights = zombie_weights
        self.spawn_queue = spawn_queue
        self._stop_event = threading.Event()

    def run(self):
        spawned = 0
        while spawned < self.total_zombies:
            # wait(timeout) bloquea spawn_delay segundos O hasta que stop() sea llamado.
            # Retorna True si el evento fue seteado (stop), False si fue timeout.
            stopped = self._stop_event.wait(timeout=self.spawn_delay)
            if stopped:
                break
            zombie_type = self._choose_type()
            self.spawn_queue.put(zombie_type)
            spawned += 1

    def _choose_type(self):
        types = list(self.zombie_weights.keys())
        weights = list(self.zombie_weights.values())
        return random.choices(types, weights=weights, k=1)[0]

    def stop(self):
        """Señala al hilo que debe terminar en la próxima iteración."""
        self._stop_event.set()


class ZombieSpawner:
    def __init__(self, assets):
        self.assets = assets

    def spawn(self, zombie_type):
        x, y = random.choice(SPAWN_POINTS)
        return ZombieFactory.create(zombie_type, x, y, self.assets)
