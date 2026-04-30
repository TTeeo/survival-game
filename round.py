import random
import pygame

from settings import ROUND_CONFIG
from entities.zombie import Zombie


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
        self.spawned_zombies = 0
        self.last_spawn_time = 0

        self.load_config()

    def load_config(self):
        config = ROUND_CONFIG.get(self.number, ROUND_CONFIG[max(ROUND_CONFIG)])

        self.total_zombies = config["total_zombies"]
        self.spawn_delay = config["spawn_delay"]
        self.zombie_weights = config["zombie_weights"]

    def can_spawn(self):
        if self.state != RoundState.SPAWNING:
            return False

        now = pygame.time.get_ticks()

        return (
            self.spawned_zombies < self.total_zombies
            and now - self.last_spawn_time >= self.spawn_delay
        )

    def choose_zombie_type(self):
        zombie_types = list(self.zombie_weights.keys())
        weights = list(self.zombie_weights.values())

        return random.choices(zombie_types, weights=weights, k=1)[0]

    def spawn(self):
        zombie_type = self.choose_zombie_type()

        zombie = self.zombie_spawner.spawn(zombie_type)

        self.zombies.append(zombie)
        self.spawned_zombies += 1
        self.last_spawn_time = pygame.time.get_ticks()

        if self.spawned_zombies >= self.total_zombies:
            self.state = RoundState.ACTIVE

    def update(self, player):
        if self.can_spawn():
            self.spawn()

        for zombie in self.zombies:
            zombie.update(player, self.zombies)

        self.zombies = [zombie for zombie in self.zombies if zombie.health > 0]

        if self.state == RoundState.ACTIVE and len(self.zombies) == 0:
            self.state = RoundState.COMPLETED

    def draw(self, screen):
        for zombie in self.zombies:
            zombie.draw(screen)

    def is_completed(self):
        return self.state == RoundState.COMPLETED
