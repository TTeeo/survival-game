# Glosario

## Jugador / Player
Entidad controlada por el usuario. Puede moverse por el mapa, utilizar armas, disparar proyectiles y recolectar recompensas. Su objetivo es sobrevivir la mayor cantidad de rondas posibles.

---

## Zombie / Zombie
Entidad hostil del juego que interactúa con el jugador. Puede perseguirlo y atacarlo mediante uno o más tipos de ataque (por ejemplo, cuerpo a cuerpo o a distancia). Al morir otorga puntaje, contribuye al combo y puede generar recompensas.

---

## Arma / Weapon
Elemento utilizado por el jugador para atacar enemigos. Define las características del disparo, como daño, velocidad del proyectil, cantidad de proyectiles por disparo, dispersión, alcance y tiempo entre disparos. Al ser utilizada, genera uno o más proyectiles.

---

## Ataque de Zombie / ZombieAttack
Comportamiento mediante el cual un zombie inflige daño al jugador. Cada ataque define propiedades como daño y alcance. Puede haber distintos tipos de ataque, como cuerpo a cuerpo (MeleeAttack) o a distancia (RangedAttack).

---

## Munición / Ammo
Cantidad de disparos disponibles para el jugador. Se consume al utilizar armas y puede recuperarse mediante recompensas. Algunas armas pueden no consumir munición.

---

## Proyectil / Projectile
Entidad generada por un arma que se desplaza por el mapa. Contiene información como posición, dirección, velocidad, daño y distancia recorrida. Al impactar o finalizar su ciclo de vida, puede aplicar efectos adicionales.

---

## Efecto de Proyectil / ProjectileEffect
Comportamiento asociado a un proyectil que se ejecuta al impactar o al finalizar su ciclo de vida. Permite extender el comportamiento del proyectil, por ejemplo generando daño en área.

---

## Ronda / Round
Fase del juego que determina la cantidad, tipo y frecuencia de aparición de enemigos. La dificultad aumenta progresivamente, incrementando la cantidad de enemigos, reduciendo los tiempos de aparición e introduciendo enemigos más complejos.

---

## Combo / Combo
Sistema que registra eliminaciones consecutivas de enemigos. Aumenta al eliminar enemigos en un intervalo de tiempo y se reinicia si el jugador deja de eliminar enemigos durante un período determinado. Puede influir en el puntaje y en la generación de recompensas.

---

## Recompensa / Reward
Objeto generado al eliminar enemigos que el jugador puede recolectar. Al ser consumido, aplica un efecto directo sobre el jugador, como recuperar vida, obtener munición o adquirir un arma.

---

## Puntaje / Score
Valor acumulado que refleja el desempeño del jugador. Aumenta al eliminar enemigos y puede verse potenciado por el sistema de combo.

---

## Vida / Health
Valor que representa la resistencia de una entidad. Al llegar a cero, la entidad es eliminada.

---

## Daño / Damage
Cantidad de vida que se reduce al recibir un ataque o impacto de proyectil.

---

## Mapa / Map
Espacio donde se desarrolla la partida. Contiene al jugador, enemigos, proyectiles y recompensas.