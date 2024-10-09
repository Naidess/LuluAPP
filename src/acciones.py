import random
from minijuego import Juegos
from abc import ABC, abstractmethod

class Accion(ABC):
    """Clase base abstracta que define una acción realizada por Lulu."""
    
    def __init__(self, lulu, mostrar_mensaje_callback):
        """
        Inicializa la acción con una instancia de Lulu y una función de callback para mostrar mensajes.

        Args:
            lulu (Lulu): Instancia de Lulu sobre la cual se realizará la acción.
            mostrar_mensaje_callback (func): Función de callback para mostrar mensajes.
        """
        self.lulu = lulu
        self.mostrar_mensaje_callback = mostrar_mensaje_callback
    
    @abstractmethod
    def realizar(self):
        """Método abstracto para realizar la acción."""
        raise NotImplementedError("Este método debe ser implementado por las subclases.")

    def mostrar_mensaje(self, mensaje):
        """
        Muestra un mensaje utilizando el callback.

        Args:
            mensaje (str): El mensaje que se desea mostrar.
        """
        self.mostrar_mensaje_callback(mensaje)

class Comer(Accion):
    """Clase que representa la acción de comer."""

    def realizar(self):
        """Realiza la acción de comer."""
        self.lulu.estado.hambre -= random.randint(30, 50)
        self.lulu.estado.felicidad += random.randint(20, 50)
        self.lulu.estado.energia += random.randint(0, 10)
        self.lulu.estado.suciedad += random.randint(0, 10)
        if self.lulu.estado.hambre == 0:
            self.lulu.estado.salud += random.randint(5, 15)
        elif self.lulu.estado.hambre == 100:
            self.lulu.estado.salud -= random.randint(5, 15)
        self.lulu.estado.limitar_valores()
        self.mostrar_mensaje("Lulu ha comido y se siente mejor.")

class Jugar(Accion):
    """Clase que representa la acción de Lulu de jugar."""

    def __init__(self, lulu, mostrar_mensaje_callback, root):
        super().__init__(lulu, mostrar_mensaje_callback)
        self.root = root
        self.juegos = Juegos(root)

    def realizar(self):
        """Realiza la acción de jugar."""
        self.mostrar_mensaje("\nLulu quiere jugar.")
        if self.root:  # Si hay una ventana raíz (Tkinter)
            self.juegos.seleccionar_juego_interfaz(self.actualizar_estado)
        else:
            self.juegos.seleccionar_juego(self.actualizar_estado)

    def actualizar_estado(self, resultado):
        """Actualiza el estado de Lulu basado en el resultado del juego."""
        if resultado:
            self.lulu.estado.aburrido -= random.randint(40, 50)
            self.lulu.estado.felicidad += random.randint(50, 100)
            self.mostrar_mensaje("Lulu se divirtió mucho")
        else:
            self.lulu.estado.aburrido -= random.randint(30, 50)
            self.mostrar_mensaje("Lulu se divirtió un poco.")
        self.lulu.estado.energia -= random.randint(0, 10)
        self.lulu.estado.suciedad += random.randint(0, 10)
        self.lulu.estado.limitar_valores()

class Dormir(Accion):
    """Clase que representa la acción de Lulu de dormir."""

    def realizar(self):
        """Realiza la acción de dormir."""
        self.lulu.estado.energia = 100
        self.lulu.estado.felicidad += random.randint(0, 5)
        self.lulu.estado.suciedad += random.randint(0, 30)
        self.mostrar_mensaje("Lulu está durmiendo y recuperando su energía.")
        self.lulu.estado.limitar_valores()

class Curar(Accion):
    """Clase que representa la acción de Lulu de curarse."""
    
    def realizar(self):
        """Realiza la acción de curarse."""
        self.lulu.estado.salud = 100
        self.lulu.estado.energia -= random.randint(0, 10)
        self.lulu.estado.suciedad += random.randint(0, 5)
        self.lulu.estado.limitar_valores()
        self.mostrar_mensaje("Lulu ha tomado medicina y se ha recuperado. ¡Qué bien!")

class Ducharse(Accion):
    """Clase que representa la acción de Lulu de ducharse."""

    def realizar(self):
        """Realiza la acción de ducharse."""
        self.lulu.estado.suciedad = 0
        self.lulu.estado.energia -= random.randint(0, 10)
        self.lulu.estado.felicidad += random.randint(0, 10)
        self.lulu.estado.salud += random.randint(0, 5)
        self.lulu.estado.limitar_valores()
        self.mostrar_mensaje("Lulu ha tomado una ducha.")
