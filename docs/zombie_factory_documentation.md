# Documentación de ZombieFactory

## Qué es esta clase

`ZombieFactory` es una clase auxiliar encargada de crear objetos de tipo zombie de forma sencilla y centralizada.

Su función no es controlar el juego ni el comportamiento de los enemigos, sino construirlos a partir de una configuración predefinida.

## Propósito

Esta clase sirve para separar la creación de zombies de la lógica de la ronda o del juego.

En lugar de crear cada zombie manualmente en distintos puntos del código, se delega esa tarea a `ZombieFactory`.

## Cómo funciona

El método `create(...)` recibe:
- `zombie_type`: el tipo de zombie que se quiere crear,
- `x` e `y`: la posición inicial,
- `assets`: el gestor de recursos visuales del juego.

Luego:
1. Busca la configuración del zombie en `ZOMBIES`.
2. Obtiene la imagen correspondiente desde `assets`.
3. Crea un objeto `Zombie` con todos los atributos necesarios.

## Qué devuelve

Devuelve una instancia de la clase `Zombie`, ya configurada con:
- posición,
- velocidad,
- vida,
- daño,
- imagen visual,
- y puntos que otorga al morir.

## Ventaja de usar esta clase

Usar una fábrica hace que el código sea más limpio porque:
- evita repetir la misma lógica de creación en varios lugares,
- centraliza la forma en que se construyen los zombies,
- y facilita modificar la creación si cambia la configuración del juego.

## Resumen simple

`ZombieFactory` es la encargada de “fabricar” zombies según su tipo y su configuración visual y de comportamiento.
