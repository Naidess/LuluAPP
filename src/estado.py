import random
import threading
import time

from felicidad import calcular_felicidad_promedio

class Estado:
    """Clase para gestionar los estados de Lulu."""
    LIMITE_SUPERIOR = 100
    LIMITE_INFERIOR = 0
    INTERVALO_ACTUALIZACION = 20  # segundos

    def __init__(self):
        """Inicializa los atributos del estado con valores aleatorios."""
        self.hambre = random.randint(30, 70)
        self.energia = random.randint(30, 70)
        self.aburrido = random.randint(30, 70)
        self.salud = random.randint(30, 70)
        self.felicidad = random.randint(30, 70)
        self.suciedad = random.randint(30, 70)
        self.thread = None
        self.activo = True  # Bandera para controlar la activación del hilo
        self.iniciar_actualizacion_automatica()

    def iniciar_actualizacion_automatica(self):
        """Inicia la actualización automática de los estados."""
        self.thread = threading.Thread(target=self._actualizar_estados, daemon=True)
        self.thread.start()  # Iniciar el hilo

    def detener_actualizacion_automatica(self):
        """Detiene la actualización automática de los estados."""
        self.activo = False  # Marcar que ya no se requiere la ejecución del hilo
        if self.thread is not None:
            self.thread.join()  # Esperar a que el hilo termine completamente

    def detener_todos_los_hilos(self):
        """Detiene todos los hilos activos."""
        self.detener_actualizacion_automatica()  # Detener el hilo de actualización automática

    def estas_dormido(self):
        """Verifica si Lulu está dormida."""
        return self.energia < 20

    def estas_enfermo(self):
        """Verifica si Lulu está enferma."""
        return self.salud < 40
    
    def estas_sucio(self):
        """Verifica si Lulu está sucia."""
        return self.suciedad > 80
    
    def estas_feliz(self):
        """Verifica si Lulu está feliz."""
        return calcular_felicidad_promedio(self) > 70

    def estas_muerto(self):
        """Verifica si Lulu está muerta."""
        return self.salud == 0
    
    def tienes_quejas(self):
        """Verifica si Lulu tiene quejas."""
        return self.hambre > 75 or self.aburrido > 60

    def _actualizar_estados(self):
        """Actualiza los estados de Lulu con valores aleatorios."""
        while self.activo:
            try:
                self.hambre = min(self.hambre + random.randint(1, 5), self.LIMITE_SUPERIOR)
                self.aburrido = min(self.aburrido + random.randint(1, 4), self.LIMITE_SUPERIOR)
                self.energia = max(self.energia - random.randint(1, 3), self.LIMITE_INFERIOR)
                self.suciedad = min(self.suciedad + random.randint(1, 3), self.LIMITE_SUPERIOR)
                # Ajustes a la salud basados en condiciones actuales
                if self.hambre > 70 or self.energia < 30:
                    self.salud = max(self.salud - random.randint(1, 3), self.LIMITE_INFERIOR)
                # Ajustes a la felicidad basados en condiciones actuales
                if self.hambre > 30 or self.aburrido > 30:
                    self.felicidad = max(self.felicidad - random.randint(1, 5), self.LIMITE_INFERIOR)
                self.limitar_valores()
            except Exception as e:
                print(f"Error al actualizar estados: {e}")
            # Esperar el intervalo de actualización
            time.sleep(self.INTERVALO_ACTUALIZACION)
        
    def limitar_valores(self):
        """Limita los valores de los atributos dentro de un rango definido."""
        atributos = ['hambre', 'aburrido', 'energia', 'felicidad', 'salud', 'suciedad']
        for atributo in atributos:
            valor = getattr(self, atributo)
            valor_limitado = max(self.LIMITE_INFERIOR, min(self.LIMITE_SUPERIOR, valor))
            setattr(self, atributo, valor_limitado)

    def mostrar_estadisticas(self):
        """Muestra las estadísticas actuales de Lulu."""
        guiones = 22
        print("+" + "-"*guiones + "+")
        print("| Estadísticas de Lulu |")
        print("+" + "-"*guiones + "+")
        print("| Hambre:       {:<6} |".format(self.hambre))
        print("| Aburrimiento: {:<6} |".format(self.aburrido))
        print("| Energía:      {:<6} |".format(self.energia))
        print("| Suciedad:     {:<6} |".format(self.suciedad))
        print("| Felicidad:    {:<6} |".format(self.felicidad))
        print("| Salud:        {:<6} |".format(self.salud))  
        print("+" + "-"*guiones + "+")
