# Visión del sistema

## Descripción general

Survival Game es un juego de supervivencia en tiempo real desarrollado en Python utilizando pygame, en el cual el jugador debe resistir oleadas de enemigos que aumentan progresivamente en dificultad.

El jugador controla un personaje que puede moverse por el mapa, utilizar distintas armas y eliminar enemigos para progresar en la partida. Los enemigos representan distintas amenazas dentro del juego, pudiendo existir diferentes tipos con comportamientos y características propias, como zombies u otros enemigos futuros.

## Objetivo del sistema

El objetivo del sistema es brindar una experiencia de supervivencia en tiempo real, en la que el jugador enfrenta oleadas de enemigos con dificultad creciente, buscando sobrevivir la mayor cantidad de rondas posibles.

El juego incorpora un sistema de progresión basado en eliminaciones consecutivas, que otorga beneficios al jugador y potencia su capacidad para afrontar desafíos progresivamente más exigentes.

## Alcance

El sistema incluye:

- Control del jugador (movimiento, disparo y cambio de arma)
- Sistema de combate basado en armas y proyectiles
- Diferentes tipos de armas con propiedades específicas (daño, velocidad, cooldown, alcance, etc.)
- Sistema de modificadores de armas que permiten alterar sus propiedades (por ejemplo: daño, cadencia, cantidad de proyectiles, etc.)
- Diferentes tipos de enemigos con comportamientos y estadísticas propias (por ejemplo: zombies)
- Generación de enemigos por rondas con dificultad progresiva (incremento de cantidad, frecuencia, tipo y estadísticas)
- Sistema de aparición (spawn) de enemigos en puntos definidos del mapa
- Detección de colisiones entre entidades (balas, enemigos y jugador)
- Sistema de daño y eliminación de enemigos
- Sistema de puntaje influenciado por el desempeño del jugador
- Sistema de combo que incentiva eliminar enemigos consecutivamente sin interrupciones
- Sistema de recompensas basado en la eliminación de enemigos, que otorga mejoras o modificadores al jugador
- Gestión del estado del juego (jugando, pausado y finalizado)
- Actualización continua del estado del juego en tiempo real

El sistema no incluye:

- Modo multijugador
- Persistencia de datos (guardado de partidas)
- Integración con servicios externos

## Actores

- **Jugador:** Persona que interactúa con el sistema controlando el personaje principal, tomando decisiones en tiempo real para sobrevivir, combatir enemigos y progresar en las rondas del juego.

Actualmente, el sistema contempla un único actor principal, dado que se trata de un juego de un solo jugador sin interacción con sistemas externos.

## Supuestos

- El juego se ejecuta localmente en un entorno con Python instalado.
- El usuario dispone de un entorno compatible con pygame.
- El usuario utiliza teclado para controlar el personaje.
- El sistema se ejecuta en tiempo real con actualización continua de la pantalla.
- El entorno de ejecución cuenta con los recursos mínimos de hardware para mantener un rendimiento fluido.
- El jugador interactúa con un único personaje durante toda la partida.
- El juego se ejecuta en modo de ventana con resolución predefinida.
- No existe interacción con otros jugadores ni con servicios externos.

## Características principales

- Supervivencia por rondas con dificultad creciente
- Variedad de armas con diferentes comportamientos y propiedades
- Sistema de progresión basado en combo y recompensas
- Presencia de distintos tipos de enemigos con comportamientos diferenciados
- Respuesta en tiempo real a las acciones del jugador
- Progresión basada en el desempeño del jugador durante la partida
- Experiencia orientada a la toma de decisiones en tiempo real

## Restricciones

- El sistema está implementado en Python utilizando pygame.
- El rendimiento depende del hardware donde se ejecute.
- La lógica principal del juego se ejecuta en el hilo principal para mantener la compatibilidad con pygame.
- Las tareas concurrentes o paralelas deben integrarse sin bloquear el bucle principal del juego.
- La concurrencia/paralelismo debe utilizarse en componentes auxiliares, sin afectar la respuesta en tiempo real del jugador.

## Evolución futura

El sistema podrá evolucionar para incorporar nuevas funcionalidades, entre ellas:

- Nuevos tipos de enemigos (por ejemplo: enemigos a distancia, jefes, variantes especiales)
- Modo multijugador con interacción entre jugadores
- Sistemas de ranking o competencia
- Persistencia de datos y progreso del jugador