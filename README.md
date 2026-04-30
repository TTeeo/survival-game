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

Desde este archivo se centralizan los valores principales del juego, como:

- tamaño de pantalla y FPS
- configuración de balas y sprites
- armas disponibles, daño, cooldown, velocidad, alcance y tipo de bala
- configuración inicial del jugador
- tipos de zombies, vida, velocidad y daño
- separación entre zombies
- configuración de rondas, cantidad de enemigos, velocidad de aparición y probabilidad de cada tipo de zombie
- puntos de aparición de enemigos