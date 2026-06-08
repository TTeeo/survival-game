# **🧟 Zombie Game**

## **📝 Descripción**

Juego de supervivencia desarrollado en Python utilizando *pygame*.

El jugador enfrenta oleadas de zombies que aumentan progresivamente en dificultad.
El objetivo es sobrevivir la mayor cantidad de rondas posibles eliminando enemigos y evitando recibir daño.

## **📋 Requisitos**

Python 3.9 o superior

> Este proyecto utiliza pygame 2.6.1 (instalado automáticamente desde `requirements.txt`)

## **⚙️ Instalación**

### 1. Clonar repositorio
```
git clone https://github.com/TTeeo/zombie-survival.git
cd zombie-survival
```

### 2. Crear entorno virtual
```
python -m venv venv
```

### 3. Activar entorno virtual

En Windows:
```
venv\Scripts\activate
```

En Linux / macOS:
```
source venv/bin/activate
```

### 4. Instalar dependencias
```
pip install -r requirements.txt
```

## **▶️ Ejecución**

En Windows:
```
python main.py
```

En Linux / macOS:
```
python3 main.py
```

## **🎮 Cómo jugar**

### Objetivo

Sobrevivir la mayor cantidad de rondas posibles eliminando zombies antes de que te maten.
Cada zombie eliminado otorga puntos. El juego no tiene fin: las rondas escalan indefinidamente en dificultad.

---

### Controles

| Tecla | Acción |
|-------|--------|
| `W` | Mover hacia arriba |
| `A` | Mover hacia la izquierda |
| `S` | Mover hacia abajo |
| `D` | Mover hacia la derecha |
| `ESPACIO` | Disparar en la dirección que mira el jugador |
| `R` | Reiniciar partida *(solo en pantalla de Game Over)* |

> El jugador siempre dispara en la última dirección en que se movió.
> Mantener `ESPACIO` presionado dispara de forma continua (limitado por el cooldown del arma).

---

### La pantalla de juego

```
┌───────────────────────────────────────────────────────┐
│ Vida: 85        Puntaje: 420          Ronda: 3        │
│ FX: VEL x1.5                                          │
│                                                        │
│   [obstáculo]         [obstáculo]                      │
│                                                        │
│              🧟  👤  🧟                                │
│                                                        │
│   [obstáculo]    [obstáculo central]   [obstáculo]    │
└───────────────────────────────────────────────────────┘
```

**HUD (esquina superior):**
- **Vida** — puntos de vida restantes del jugador (máx. 100).
- **Puntaje** — puntos acumulados en la partida.
- **Ronda** — número de ronda actual.
- **FX** — efectos activos sobre el jugador (aparece en celeste cuando hay alguno).
- **RONDA DE JEFE** — aparece en rojo en la esquina superior derecha cuando la ronda actual es de jefe (múltiplos de 5).

---

### Mecánicas principales

#### Rondas y oleadas
- Cada ronda tiene un número fijo de zombies que van spawneando de a poco desde los bordes del mapa.
- Cuando todos los zombies de la ronda son eliminados, aparece una pantalla de transición durante 5 segundos y comienza la siguiente ronda.
- La dificultad aumenta con cada ronda: más zombies, mayor velocidad de aparición y mayor proporción de tipos difíciles.

#### Obstáculos
- El mapa tiene 5 bloques de obstáculos (esquinas + centro) representados como rectángulos marrones.
- Los zombies intentan rodearlos.
- Las balas impactan contra ellos y desaparecen.
- El jugador no puede atravesarlos.

#### Drops / Power-ups
Cuando un zombie muere tiene un 25 % de probabilidad de dejar un ítem en el suelo. El ítem desaparece después de 9 segundos si no se recoge. Caminar sobre él lo activa automáticamente.

| Ítem | Color | Efecto |
|------|-------|--------|
| **CURA +25** | Verde | Restaura 25 puntos de vida (máximo 100) |
| **VEL x1.5** | Azul | Aumenta la velocidad de movimiento 1.5× durante 8 segundos |
| **ESCUDO** | Amarillo | Absorbe el próximo golpe recibido (dura 10 segundos) |

---

### Tipos de zombie

| Tipo | Tamaño | Velocidad | Vida | Daño | Puntos |
|------|--------|-----------|------|------|--------|
| **Básico** | Normal | Lenta | 50 | 10 | 10 |
| **Rápido** | Normal | Alta | 30 | 8 | 15 |
| **Runner** | Pequeño | Muy alta | 15 | 6 | 20 |
| **Tank** | Grande | Muy lenta | 180 | 25 | 35 |

- Los nuevos tipos se introducen gradualmente a partir de la ronda 2.
- A partir de la ronda 7 la configuración escala dinámicamente sin límite.

---

### Rondas de Jefe (rondas 5, 10, 15…)

En cada ronda múltiplo de 5 aparece un **Zombie Jefe** en el centro del mapa junto a los zombies normales.

**Características del Jefe:**
- Tamaño doble, 500 puntos de vida, 200 puntos al eliminarlo.
- Tiene una máquina de estados con tres fases:

| Estado | Borde | Comportamiento |
|--------|-------|----------------|
| **CHASE** (persecución) | Rojo oscuro | Se acerca lentamente al jugador |
| **TELEGRAPH** (advertencia) | Amarillo | Se detiene un instante — señal de que va a embestir |
| **CHARGE** (embestida) | Rojo vivo | Lanza una carga rápida en línea recta |

> La pantalla de transición avisa **"PRÓXIMA RONDA: JEFE"** antes de una ronda de jefe.

---

### Game Over

Cuando la vida del jugador llega a 0 aparece la pantalla de Game Over mostrando:
- Puntaje final acumulado.
- Ronda en que murió.
- Instrucción para reiniciar con `R`.


## **🧩 Estructura del proyecto**

El proyecto está organizado separando responsabilidades principales:

- `main.py`: punto de entrada del programa.
- `game/`: contiene la lógica principal del juego y sus estados.
- `entities/`: contiene las entidades del juego, como jugador, zombies, armas, balas y modificadores.
- `managers/`: contiene clases encargadas de coordinar partes del sistema, como rondas, colisiones, assets y puntaje.
- `factories/`: contiene la creación de objetos como armas y zombies.
- `spawners/`: contiene la lógica de aparición de enemigos.
- `config/`: contiene la configuración general del juego.
- `assets/`: contiene los recursos visuales del juego.


## **⚙️ Configuración**

La configuración principal del juego se encuentra en `settings.py` (raíz del proyecto).

Este archivo centraliza los valores clave del sistema, organizados en:

### Pantalla
- Tamaño de pantalla  
- FPS  

### Combate
- Configuración de balas (tipo, velocidad, comportamiento)  
- Armas (daño, cooldown, alcance, tipo de bala)  

### Sprites y assets
- Sprites de balas (spritesheet y posiciones)  
- Sprites de armas  
- Sprites de jugador y enemigos  

### Jugador
- Configuración inicial (posición, vida, velocidad, arma inicial)  

### Enemigos
- Tipos de zombies (vida, velocidad, daño)  
- Parámetros de comportamiento (separación entre zombies)  

### Rondas
- Cantidad de enemigos por ronda  
- Frecuencia de aparición  
- Probabilidad de cada tipo de enemigo  

### Spawn
- Puntos de aparición de enemigos  