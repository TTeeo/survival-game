# Documentación de Round

## Qué es esta clase

`Round` representa una ola o ronda del juego. Su responsabilidad principal es controlar todo lo que ocurre durante esa etapa: aparición de enemigos, movimiento, colisiones, eliminación de zombies y cambio de estado cuando la ronda termina.

## Propósito

Cada ronda tiene su propia configuración de dificultad. La clase `Round` se encarga de:
- definir cuántos zombies deben aparecer,
- decidir con qué frecuencia aparecen,
- gestionar los zombies vivos,
- actualizar su inteligencia artificial,
- detectar cuándo una ronda ha sido completada,
- y detener los hilos relacionados cuando termina.

## Estados de una ronda

La clase usa un estado interno para saber en qué momento está la ronda:

- `SPAWNING`: todavía se están generando los zombies.
- `ACTIVE`: la ronda ya está en marcha y los zombies están activos.
- `COMPLETED`: todos los zombies fueron eliminados y la ronda terminó.

## Cómo funciona

Cuando se crea una ronda:
1. Se le asigna un número.
2. Se carga su configuración según la ronda actual.
3. Se crean los obstáculos del mapa.
4. Se inicializa una cola de spawn y un pool de hilos para la IA de los zombies.
5. Se inicia el hilo productor encargado de generar pedidos de aparición.
6. Si la ronda es de jefe, también se agrega un jefe al inicio de la misma.

## Métodos principales

### `__init__`
Inicializa la ronda, carga la configuración, prepara los obstáculos y pone en marcha los subprocesos necesarios.

### `load_config()`
Busca la configuración correspondiente a la ronda actual y guarda valores como:
- cantidad total de zombies,
- tiempo entre apariciones,
- tipos de zombie que pueden aparecer.

### `_spawn_boss()`
Agrega un jefe al inicio de las rondas especiales.

### `_drain_spawn_queue()`
Consume los pedidos generados por el hilo de spawn y crea los zombies reales en el hilo principal.

### `_compute_ai_parallel()`
Ejecuta el cálculo del movimiento de los zombies en paralelo usando un pool de hilos. Esto permite que la IA sea más eficiente.

### `update(player)`
Es el método más importante. En cada frame:
- consume los nuevos zombies pendientes de generar,
- calcula el movimiento de todos los zombies,
- aplica esos movimientos,
- comprueba si alguno murió,
- suma puntos por los enemigos eliminados,
- y cambia el estado de la ronda si ya no quedan zombies vivos.

### `draw(screen)`
Dibuja los obstáculos y los zombies en la pantalla.

### `is_completed()`
Devuelve si la ronda ha finalizado.

### `stop()`
Detiene todos los hilos asociados a la ronda para evitar fugas o comportamientos inconsistentes.

## Relación con el juego

`Round` es una pieza central del diseño del juego. No maneja directamente el movimiento del jugador ni el HUD, pero sí organiza la parte de combate y supervivencia de cada ola.

## Resumen simple

Piensa en `Round` como el “director” de una ola del juego. Controla cuándo aparecen los enemigos, cómo se mueven, cuándo terminan y cuándo la ronda se considera completada.
