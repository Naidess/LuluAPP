import json
import os

class GestorDeEstados:
    """Clase para gestionar los estados de Lulu."""

    def __init__(self, carpeta="saved_states"):
        """
        Inicializa el gestor de estados con la ruta de la carpeta de guardado.

        Args:
            carpeta (str): Ruta de la carpeta donde se guardarán los estados. Por defecto, "saved_states".
        """
        self.carpeta = carpeta
        self._crear_carpeta_si_no_existe()

    def _crear_carpeta_si_no_existe(self):
        """Crea la carpeta de guardado si no existe."""
        ruta_carpeta = os.path.join(os.getcwd(), self.carpeta)
        if not os.path.exists(ruta_carpeta):
            os.makedirs(ruta_carpeta)

    def guardar_estado(self, estado, archivo="guardado.json"):
        """
        Guarda el estado actual en un archivo JSON.

        Args:
            estado (Estado): Objeto Estado que se va a guardar.
            archivo (str, optional): Nombre del archivo donde se guardará el estado. Por defecto, "guardado.json".
        """
        try:
            ruta_completa = os.path.join(os.getcwd(), self.carpeta, archivo)
            datos = {
                "hambre": estado.hambre,
                "energia": estado.energia,
                "aburrido": estado.aburrido,
                "salud": estado.salud,
                "felicidad": estado.felicidad,
                "suciedad": estado.suciedad
            }
            with open(ruta_completa, "w") as f:
                json.dump(datos, f)
            print("Guardado con éxito.")
        except FileNotFoundError:
            print(f"No se encontró la carpeta {self.carpeta}.")
        except Exception as e:
            print(f"Error al guardar progreso: {e}")

    def cargar_estado(self, estado_class, archivo="guardado.json"):
        """
        Carga el estado desde un archivo JSON.

        Args:
            estado_class (class): Clase del estado que se va a cargar.
            archivo (str, optional): Nombre del archivo desde donde se cargará el estado. Por defecto, "guardado.json".

        Returns:
            Estado: Objeto Estado cargado desde el archivo JSON.
        """
        try:
            ruta_completa = os.path.join(os.getcwd(), self.carpeta, archivo)
            if os.path.exists(ruta_completa):
                with open(ruta_completa, "r") as f:
                    datos = json.load(f)
                    estado = estado_class()
                    estado.hambre = datos.get("hambre", estado.hambre)
                    estado.energia = datos.get("energia", estado.energia)
                    estado.aburrido = datos.get("aburrido", estado.aburrido)
                    estado.salud = datos.get("salud", estado.salud)
                    estado.felicidad = datos.get("felicidad", estado.felicidad)
                    estado.suciedad = datos.get("suciedad", estado.suciedad)
                    print("Cargado con éxito.")
                    return estado
            else:
                print(f"No se encontró el archivo de guardado {archivo}. Se creará uno nuevo.")
                return estado_class()
        except FileNotFoundError:
            print(f"No se encontró el archivo de guardado {archivo}. Se creará uno nuevo.")
            return estado_class()
        except Exception as e:
            print(f"Error al cargar estado: {e}")
            return estado_class()
