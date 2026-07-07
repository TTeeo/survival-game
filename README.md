# **🧟 Zombie Game**

## **📝 Descripción**

Juego de supervivencia desarrollado en Python utilizando *pygame*.

El jugador enfrenta oleadas de zombies que aumentan progresivamente en dificultad.
El objetivo es sobrevivir la mayor cantidad de rondas posibles eliminando enemigos y evitando recibir daño.

## **📋 Requisitos**

Python 3.9 o superior

> Este proyecto utiliza pygame 2.6.1 (instalado automáticamente desde `requirements.txt`)

## **💻 Restricciones y compatibilidad**

- **Hardware:** sin restricciones — corre en cualquier equipo de escritorio moderno.
- **Sistema operativo:** multiplataforma. Funciona en Windows, Linux y macOS (desarrollado y probado con Python 3.12 en macOS y Windows).
- **Navegador:** no aplica — es una aplicación de escritorio, no requiere navegador ni conexión a internet.
- **Pantalla:** resolución lógica de 900×600 escalable a pantalla completa (tecla `F`).

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
| `F` | Alternar pantalla completa |
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


## **🧵 Concurrencia**

La concurrencia es el eje del proyecto: durante toda la partida conviven el hilo principal (bucle del juego a 60 FPS), un hilo productor de apariciones, un pool de hilos para la IA y, en rondas de jefe, un hilo dedicado a su máquina de estados.

| Mecanismo | Primitivas | Archivo |
|-----------|------------|---------|
| Generación de enemigos (productor-consumidor) | `threading.Thread`, `queue.Queue`, `threading.Event` | `spawners/zombie_spawner.py` |
| IA de zombies en paralelo (fork-join) | `concurrent.futures.ThreadPoolExecutor` | `managers/round.py` |
| Máquina de estados del jefe | `threading.Thread`, `threading.Lock` | `entities/boss.py` |
| Protección de la vida del jugador | `threading.Lock` | `entities/player.py` |

### Hilo generador de enemigos (Producer-Consumer)
Cada ronda lanza un `SpawnerThread` que produce pedidos de aparición a intervalos regulares, independientes del frame rate, y los deposita en una `queue.Queue` (estructura sincronizada, sin necesidad de locks explícitos). El hilo principal consume la cola una vez por frame con `get_nowait()` y construye ahí los zombies, porque las operaciones gráficas de pygame no son seguras fuera del hilo principal: el productor decide *cuándo y qué* aparece; el consumidor lo *materializa*. La espera entre apariciones se hace con `Event.wait(timeout)`, que además permite cancelar la ronda al instante.

### IA en paralelo (fork-join)
El movimiento de cada zombie se calcula sumando cuatro fuerzas (atracción al jugador, separación entre zombies, evasión de obstáculos y ruido aleatorio). Ese cómputo se reparte en un `ThreadPoolExecutor` en dos fases: una **fase paralela de solo lectura** donde cada worker calcula el vector de movimiento sin modificar estado, una **barrera** donde el hilo principal espera todos los resultados, y una **fase secuencial** donde aplica los movimientos y ataques. Al no haber escrituras durante la fase de lectura, no hay condiciones de carrera.

### Hilo del jefe (exclusión mutua)
El jefe tiene un hilo propio que corre su máquina de estados a 20 Hz (persecución → advertencia → embestida). Ese hilo **escribe** el par (dirección, multiplicador de velocidad) y los workers del pool lo **leen**; ambos accesos están protegidos por un `threading.Lock` que garantiza la consistencia del par como unidad atómica.

### Vida del jugador
`take_damage()` ejecuta bajo `Lock` la secuencia *check-then-act* del escudo (verificar si hay escudo activo, consumirlo o descontar vida), garantizando su atomicidad ante ataques concurrentes.

### Ciclo de vida de los hilos
Todos los hilos son *daemon* y cada ronda expone un `stop()` idempotente que detiene el productor, el pool y el hilo del jefe. Se invoca al completar la ronda, al morir el jugador, al reiniciar y al cerrar el juego.


## **🧩 Estructura del proyecto**

El proyecto está organizado separando responsabilidades principales:

- `main.py`: punto de entrada del programa.
- `game/`: contiene la lógica principal del juego y sus estados.
- `entities/`: contiene las entidades del juego, como jugador, zombies, armas, balas y modificadores.
- `managers/`: contiene clases encargadas de coordinar partes del sistema, como las rondas y los assets.
- `factories/`: contiene la creación de objetos como armas y zombies.
- `spawners/`: contiene la lógica de aparición de enemigos.
- `settings.py`: configuración general del juego (pantalla, armas, zombies, rondas, jefe, obstáculos).
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