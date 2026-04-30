# **🧟 Zombie Game**

## **📝 Descripción**

Juego de supervivencia desarrollado en Python utilizando *pygame*.

El jugador enfrenta oleadas de zombies que aumentan progresivamente en dificultad.
El objetivo es sobrevivir la mayor cantidad de rondas posibles eliminando enemigos y evitando recibir daño.

## **📋 Requisitos**

Python 3.10 o superior

> Este proyecto utiliza pygame (instalado automáticamente desde `requirements.txt`)

## **⚙️Instalación**

### 1. Clonar repositorio
```

git clone https://github.com/TTeeo/zombie-survival.git
cd zombie-game

```
### 2. Crear entorno virtual
```
python -m venv venv
```

### 3. Activar entorno virtual

En Linux:
```
source venv/bin/activate
```
En Windows:
```
venv\Scripts\activate
```


### 4. Instalar dependencias
```
pip install -r requirements.txt
```

## **▶️ Ejecución**
```
python3 main.py
```

## **🎮 Controles**

- Movimiento: WASD  
- Disparo: Barra espaciadora
- Cambiar arma: Q/E
- Pausa: ESC  


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

La configuración principal del juego se encuentra en `config/settings.py`.

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