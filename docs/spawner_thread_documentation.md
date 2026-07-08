# Documentación de SpawnerThread

## Qué es esta clase

`SpawnerThread` es un hilo de Python encargado de generar pedidos de aparición de zombies de forma periódica durante una ronda del juego.

Se utiliza como parte de un patrón productor-consumidor:
- el hilo productor es `SpawnerThread`,
- la cola `queue.Queue` actúa como canal de comunicación,
- y el hilo principal del juego consume esos pedidos para crear los zombies reales en pantalla.

## Propósito

La clase tiene una responsabilidad simple: no crea directamente los zombies, sino que genera eventos de spawn a intervalos regulares.

Esto permite que:
- la aparición de enemigos sea controlada por tiempo,
- la ronda pueda detenerse limpiamente,
- y el juego no dependa de que el hilo principal haga todo el trabajo en cada frame.

## Cómo funciona

Cuando se inicia el hilo:
1. Se inicializa un contador de zombies generados.
2. El hilo entra en un bucle mientras no haya alcanzado la cantidad total esperada.
3. Espera un tiempo determinado (`spawn_delay`).
4. Si no se le ordenó detenerse, elige un tipo de zombie al azar.
5. Lo agrega a la cola `spawn_queue`.
6. Repite el proceso hasta completar la cantidad de zombies de la ronda.

## Variables importantes

- `total_zombies`: cuántos zombies debe generar esta ronda.
- `spawn_delay`: tiempo entre apariciones.
- `zombie_weights`: probabilidades con las que se eligen los distintos tipos de zombie.
- `spawn_queue`: cola donde se almacenan los pedidos de aparición.
- `_stop_event`: evento de parada que permite terminar el hilo de forma controlada.

## Métodos principales

### `__init__`
Inicializa el hilo, guarda los parámetros de configuración y crea un evento de parada.

### `run()`
Es el cuerpo del hilo. Ejecuta el ciclo principal de generación de zombies.

### `_choose_type()`
Selecciona aleatoriamente un tipo de zombie usando los pesos definidos en `zombie_weights`.

### `stop()`
Activa el evento de parada para que el hilo termine en la siguiente iteración.

## Relación con el resto del juego

`SpawnerThread` no crea el zombie visualmente por sí mismo. Solo genera una instrucción de aparición.

Luego, en otra parte del código, el hilo principal consume esa instrucción y llama a `ZombieSpawner.spawn(...)`, que finalmente crea el objeto zombie real.

## Resumen simple

Piensa en `SpawnerThread` como un reloj que dice: “en este momento, tiene que aparecer un zombie”.

No lo pinta ni lo mueve directamente; solo prepara los pedidos para que el juego los procese.
