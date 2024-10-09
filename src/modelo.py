
class Lulu:
    """Clase para gestionar a la mascota Lulu"""
    def __init__(self, nombre, estado, root=None):
        """
        Inicializa una instancia de Lulu con su nombre y estado.

        Args:
            nombre (str): Nombre de Lulu.
            estado (Estado): Objeto Estado que contiene los atributos de estado de Lulu.
            root (tk.Tk): Ventana principal de la interfaz gráfica (opcional).
        """
        self.nombre = nombre
        self.estado = estado
        self.root = root

    def mostrar(self):
        """Muestra un saludo al usuario."""
        print(f"Hola! Mi nombre es {self.nombre}. Encantada de conocerte 😁")
        print(self._generar_expresion())

    def _generar_expresion(self):
        """
        Genera la expresión facial de Lulu basada en su estado actual.

        Returns:
            str: Cadena que representa la expresión facial de Lulu en emojis.
        """
        hambre = self.estado.hambre
        energia = self.estado.energia
        suciedad = self.estado.suciedad
        felicidad = self.estado.felicidad
        aburrido = self.estado.aburrido
        salud = self.estado.salud
        # Mapeo de estados a emojis
        emojis = {
            (felicidad >= 0 and felicidad <= 10, True): "😭",
            (felicidad > 10 and felicidad <= 40, True): "😞",
            (felicidad > 40 and felicidad <= 60, True): "😑",
            (felicidad > 60 and felicidad <= 80, True): "😀",
            (felicidad > 80 and felicidad <= 100, True): "😁",  
            (aburrido > 60, True): "😒",  
            (hambre > 70, True): "😣",
            (energia <= 50 and energia > 20, True): "🥱",
            (energia <= 20, True): "😪",
            (suciedad >= 80, True): "💩",
            (salud > 20 and salud < 40, True): "😷",
            (salud > 0 and salud <= 20, True): "🤒",
            (salud == 0, True): "☠️"
        }
        # Busca el emoji para los otros estados
        for condiciones, emoji in emojis.items():
            if all(condiciones):
                return f"Lulu: {emoji}"
        #emoji por defecto
        return "Lulu: 😐"
