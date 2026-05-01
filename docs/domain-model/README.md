# Zombie Game - Modelo de Dominio

## Descripción general

Este documento describe el **modelo de dominio** del juego *Survival Game*.

El modelo representa las principales entidades conceptuales del sistema y sus relaciones, sin incluir detalles de implementación.

---

## Diagrama

![Modelo de Dominio](./domain-model.png)

🔗 [Abrir versión editable en draw.io](https://drive.google.com/file/d/1CHCw_L1MZKLddJL5wTsXckYvPSBYzeLq/view?usp=sharing)

---

## Conceptos principales

### Game
Representa una instancia del juego en ejecución.  
Contiene al jugador y gestiona la progresión de rondas, incluyendo la generación de enemigos y el estado general de la partida.

---

### Player (Jugador)
Representa al personaje controlado por el usuario.  
Puede moverse por el mapa, utilizar armas, disparar proyectiles y recolectar recompensas.

---

### Weapon (Arma)
Define cómo el jugador realiza disparos.  
Contiene la configuración del ataque, como daño, velocidad del proyectil, cantidad de proyectiles por disparo, dispersión, alcance y tiempo entre disparos.  
Al ser utilizada, genera uno o más proyectiles.

---

### Projectile (Proyectil)
Entidad generada por un arma que se desplaza en el mundo del juego.  
Posee atributos como posición, dirección, velocidad, daño y distancia recorrida.  
Puede tener un efecto asociado.  
Al impactar o finalizar su ciclo de vida, aplica su daño y, opcionalmente, su efecto.

---

### ProjectileEffect (Efecto de Proyectil)
Comportamiento opcional asociado a un proyectil.  
Se ejecuta cuando el proyectil impacta o expira.  
Permite extender el comportamiento del proyectil, por ejemplo aplicando daño en área.

---

### Zombie
Entidad enemiga que aparece durante las rondas.  
Puede moverse, recibir daño y atacar al jugador.  
Posee uno o más ataques que definen su comportamiento ofensivo.  
Al morir, otorga puntaje y puede generar recompensas.

---

### ZombieAttack (Ataque de Zombie)
Define cómo un zombie realiza daño.  
Cada ataque posee propiedades como daño y alcance.  
Permite modelar distintos tipos de ataque (por ejemplo, cuerpo a cuerpo o a distancia) sin modificar la clase `Zombie`.

---

### Round (Ronda)
Representa una oleada de enemigos.  
Define la cantidad, tipo y frecuencia de aparición de zombies.  
La dificultad aumenta progresivamente entre rondas.

---

### Reward (Recompensa)
Objeto generado al eliminar enemigos que puede ser recolectado por el jugador.  
Al ser consumido, aplica directamente un beneficio, como recuperar vida, obtener munición o adquirir un arma.

---

### Ammo (Munición)
Cantidad de disparos disponibles para el jugador.  
Se consume al utilizar armas y puede recuperarse mediante recompensas.

---

### Health (Vida)
Valor que representa la resistencia de una entidad.  
Al llegar a cero, la entidad es eliminada.

---

### Damage (Daño)
Cantidad de vida que se reduce al recibir un ataque o impacto de proyectil.

---

## Decisiones de diseño

- Las armas **no aplican daño directamente**, sino que generan proyectiles.
- El proyectil es el responsable de aplicar daño en el mundo.
- Los efectos son **opcionales** y están asociados únicamente a proyectiles.
- Las recompensas se modelan como objetos consumibles.
- Los ataques de los zombies se desacoplan mediante `ZombieAttack`, permitiendo múltiples comportamientos sin modificar la clase `Zombie`.
- Se separa claramente la configuración del disparo (`Weapon`) de la ejecución en el mundo (`Projectile`).
- El modelo prioriza simplicidad y extensibilidad, evitando abstracciones innecesarias en la primera versión.