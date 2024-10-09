import os
import threading
import time
from estado import Estado
from modelo import Lulu
from acciones import Comer, Jugar, Curar, Ducharse
from gestor_de_estados import GestorDeEstados

SAVE_PATH = "../saved_states/guardado.json"

class JuegoLulu:
    """Clase principal que maneja el flujo del juego de Lulu."""
    
    def __init__(self):
        self.gestor_estados = GestorDeEstados()
        self.estado_inicial = None
        self.mi_lulu = None
        self.acciones = []
        self.intervalo = 30

    def limpiar_pantalla(self):
        """Limpia la pantalla de la consola."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def iniciar_guardado_automatico(self):
        """Método para guardar automáticamente el estado de Lulu en un hilo separado."""
        hilo_guardar_estado = threading.Thread(target=self._guardar_automaticamente)
        hilo_guardar_estado.daemon = True  # El hilo se detendrá cuando el programa principal termine
        hilo_guardar_estado.start()

    def _guardar_automaticamente(self):
        """Método para guardar automáticamente el estado de Lulu en un hilo separado."""
        while True:
            self.gestor_estados.guardar_estado(self.estado_inicial, SAVE_PATH)
            time.sleep(self.intervalo)

    def solicitar_nueva_partida(self):
        """
        Solicita al usuario si desea iniciar una nueva partida.

        Returns:
            bool: True si el usuario elige comenzar una nueva partida (respuesta 's'),
                False si el usuario elige salir (respuesta 'n').

        Raises:
            ValueError: Si el usuario ingresa una respuesta que no es 's' ni 'n'.
        """
        while True:
            try:
                opcion = input("¿Deseas iniciar una nueva partida? (s/n): ").strip().lower()
                if opcion == "s":
                    print("¡Nueva partida creada!")
                    return True
                elif opcion == "n":
                    print("Saliendo...")
                    return False
                else:
                    raise ValueError("Respuesta inválida. Por favor, ingresa 's' para sí o 'n' para no.")
            except ValueError as e:
                print(e)

    def nueva_partida(self):
        """
        Inicia una nueva partida reiniciando el estado de Lulu y las acciones disponibles.
        """
        # Eliminar la partida anterior si existe
        if os.path.exists(SAVE_PATH):
            os.remove(SAVE_PATH)
        self.estado_inicial = Estado()
        self.mi_lulu = Lulu(nombre="Lulu", estado=self.estado_inicial)
        self._inicializar_acciones()
        # Crea el nuevo archivo de guardado
        self.gestor_estados.guardar_estado(self.estado_inicial, SAVE_PATH)

    def _inicializar_acciones(self):
        self.acciones = [
            Comer(self.mi_lulu), 
            Jugar(self.mi_lulu), 
            Curar(self.mi_lulu), 
            Ducharse(self.mi_lulu)
        ]

    def mostrar_menu_acciones(self):
        """Muestra las opciones de acciones disponibles."""
        self.limpiar_pantalla()
        self.mi_lulu.mostrar()
        self.estado_inicial.mostrar_estadisticas()
        self._verificar_salud()
        print("\nAcciones:")
        for i, accion in enumerate(self.acciones, start=1):
            print(f"{i}. {accion.__class__.__name__}")
        print(f"{len(self.acciones) + 1}. Actualizar")
        print("0. Salir")

    def ejecutar_accion(self, opcion):
        """Ejecuta la acción seleccionada por el usuario."""
        if opcion == "0":
            print("¡Hasta la próxima!")
            return False
        elif opcion.isdigit() and 1 <= int(opcion) <= len(self.acciones):
            self.acciones[int(opcion) - 1].realizar()
        elif opcion == str(len(self.acciones) + 1):
            pass # Actualizar Estadistica
        else:
            print("¡Opción inválida!")
        input("Presiona Enter para continuar...")
        return True
    
    def _verificar_salud(self):
        """Verifica la salud de Lulu y maneja el reinicio del juego si es necesario."""
        if self.mi_lulu.estado.salud == 0:
            print("No cuidaste suficiente de Lulu... RIP")
            # Llama a la función para obtener la opción del usuario
            if self.solicitar_nueva_partida():
                self.nueva_partida()
            else:
                self.estado_inicial.detener_actualizacion_automatica()
                exit()

    def jugar(self):
        """
        Función principal que maneja la interacción con el usuario y controla el flujo del juego.
        """
        self.estado_inicial = self.gestor_estados.cargar_estado(Estado, SAVE_PATH)
        self.mi_lulu = Lulu(nombre="Lulu", estado=self.estado_inicial)
        self._inicializar_acciones()
        self.iniciar_guardado_automatico()
        self.estado_inicial.iniciar_actualizacion_automatica()  # Inicia la actualización automática
        opcion = -1
        while opcion != 0:
            self.mostrar_menu_acciones()
            opcion = input(f"Selecciona una acción (0-{len(self.acciones)+1}): ")
            if not self.ejecutar_accion(opcion):
                break
        # Cancela el temporizador del estado al salir del juego
        self.estado_inicial.detener_actualizacion_automatica()

if __name__ == "__main__":
    juego = JuegoLulu()
    juego.jugar()
