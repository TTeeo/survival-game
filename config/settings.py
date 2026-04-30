# =========================
# PANTALLA
# =========================
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

FPS = 60



# =========================
# BULLETS
# =========================

BULLET_ROCKET = "rocket_bullet"
BULLET_SHOTGUN = "shotgun_bullet"
BULLET_PISTOL = "pistol_bullet"
BULLET_REVOLVER = "revolver_bullet"
BULLET_THOMPSON = "thompson_bullet"
BULLET_RIFLE = "rifle_bullet"

BULLET_SHEET = {
  "asset": "bullets",
  "path": "assets/bullets/bullets_sprites.png",
  "size": 16,
}

BULLETS = {
  BULLET_ROCKET: {
    "asset": BULLET_SHEET["asset"],
    "sprite": {"row": 0, "col": 0},
    "size": BULLET_SHEET["size"],
  },

  BULLET_SHOTGUN: {
    "asset": BULLET_SHEET["asset"],
    "sprite": {"row": 0, "col": 1},
    "size": BULLET_SHEET["size"],
  },

  BULLET_PISTOL: {
    "asset": BULLET_SHEET["asset"],
    "sprite": {"row": 0, "col": 2},
    "size": BULLET_SHEET["size"],
  },

  BULLET_REVOLVER: {
    "asset": BULLET_SHEET["asset"],
    "sprite": {"row": 0, "col": 2},
    "size": BULLET_SHEET["size"],
  },

  BULLET_THOMPSON: {
    "asset": BULLET_SHEET["asset"],
    "sprite": {"row": 0, "col": 3},
    "size": BULLET_SHEET["size"],
  },

  BULLET_RIFLE: {
    "asset": BULLET_SHEET["asset"],
    "sprite": {"row": 0, "col": 4},
    "size": BULLET_SHEET["size"],
  },
}

# =========================
# WEAPONS
# =========================


WEAPON_RIFLE = "rifle"
WEAPON_PISTOL = "pistol"
WEAPON_REVOLVER = "revolver"
WEAPON_SHOTGUN = "shotgun"
WEAPON_THOMPSON = "thompson"
WEAPON_ROCKET_LAUNCHER = "rocket_launcher"

WEAPONS = {
  WEAPON_RIFLE: {
    "damage": 50,
    "cooldown": 300,
    "bullet_speed": 12,
    "projectiles": 1,
    "spread": 0.0,
    "range": 800,
    "sprite": {"row": 0, "col": 0},
    "bullet_type": BULLET_RIFLE,
  },

  WEAPON_PISTOL: {
    "damage": 10,
    "cooldown": 800,
    "bullet_speed": 10,
    "projectiles": 1,
    "spread": 0.0,
    "range": 600,
    "sprite": {"row": 0, "col": 1},
    "bullet_type": BULLET_PISTOL,
  },

  WEAPON_REVOLVER: {
    "damage": 80,
    "cooldown": 1200,
    "bullet_speed": 11,
    "projectiles": 1,
    "spread": 0.02,
    "range": 700,
    "sprite": {"row": 0, "col": 2},
    "bullet_type": BULLET_REVOLVER,
  },

  WEAPON_SHOTGUN: {
    "damage": 30,
    "cooldown": 1500,
    "bullet_speed": 8,
    "projectiles": 5,
    "spread": 0.3,
    "range": 400,
    "sprite": {"row": 0, "col": 3},
    "bullet_type": BULLET_SHOTGUN,
  },

  WEAPON_THOMPSON: {
    "damage": 20,
    "cooldown": 200,
    "bullet_speed": 13,
    "projectiles": 1,
    "spread": 0.1,
    "range": 700,
    "sprite": {"row": 1, "col": 1},
    "bullet_type": BULLET_THOMPSON,
  },

  WEAPON_ROCKET_LAUNCHER: {
    "damage": 200,
    "cooldown": 2000,
    "bullet_speed": 6,
    "projectiles": 1,
    "spread": 0.0,
    "range": 900,
    "explosion_radius": 100,
    "sprite": {"row": 1, "col": 2},
    "bullet_type": BULLET_ROCKET,
  },
}

WEAPON_SHEET = {
  "asset": "weapons",
  "path": "assets/weapons/Weapons sprites (32x32).png",
  "size": 32
}


# =========================
# PLAYER
# =========================
PLAYER_CONFIG = {
  "sprite": {
    "asset": "player",
    "path": "assets/player/Player_idle.png",
    "size": 32,
  },

  "stats": {
    "health": 100,
    "speed": 3,
  },

  "init": {
    "pos": (400, 300),
    "weapon": WEAPON_PISTOL,
  }
}

DIR_UP = "up"
DIR_DOWN = "down"
DIR_LEFT = "left"
DIR_RIGHT = "right"


# =========================
# ZOMBIES
# =========================
ZOMBIE_BASIC = "basic"
ZOMBIE_FAST = "fast"

ZOMBIE_SEPARATION_DISTANCE = 35
ZOMBIE_SEPARATION_FORCE = 1
ZOMBIE_SPRITE_SIZE = 32


ZOMBIES = {
  ZOMBIE_BASIC: {
    "sprite": {
      "asset": "zombie_basic",
      "path": "assets/zombie/zombie_basic/Zombie_Idle.png",
    },

    "stats": {
      "speed": 1,
      "health": 50,
      "damage": 10,
    },
  },

  ZOMBIE_FAST: {
    "sprite": {
      "asset": "zombie_fast",
      "path": "assets/zombie/zombie_2/Zombie 2_Idle.png",
    },

    "stats": {
      "speed": 2,
      "health": 30,
      "damage": 8,
    },
  },
}


# =========================
# RONDAS
# =========================
ROUND_DELAY = 10000

ROUND_CONFIG = {
    1: {
        "total_zombies": 3,
        "spawn_delay": 1200,
        "zombie_weights": {
            ZOMBIE_BASIC: 1.0,
            ZOMBIE_FAST: 0.0,
        },
    },
    2: {
        "total_zombies": 6,
        "spawn_delay": 1000,
        "zombie_weights": {
            ZOMBIE_BASIC: 0.8,
            ZOMBIE_FAST: 0.2,
        },
    },
    3: {
        "total_zombies": 10,
        "spawn_delay": 800,
        "zombie_weights": {
            ZOMBIE_BASIC: 0.7,
            ZOMBIE_FAST: 0.3,
        },
    },
    4: {
        "total_zombies": 15,
        "spawn_delay": 650,
        "zombie_weights": {
            ZOMBIE_BASIC: 0.6,
            ZOMBIE_FAST: 0.4,
        },
    },
}


# =========================
# SPAWN
# =========================
SPAWN_OFFSET = 50

SPAWN_POINTS = [
    (-SPAWN_OFFSET, SCREEN_HEIGHT // 2),
    (SCREEN_WIDTH + SPAWN_OFFSET, SCREEN_HEIGHT // 2),
    (SCREEN_WIDTH // 2, -SPAWN_OFFSET),
    (SCREEN_WIDTH // 2, SCREEN_HEIGHT + SPAWN_OFFSET),
]

