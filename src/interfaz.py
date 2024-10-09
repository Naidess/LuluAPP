import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from acciones import Comer, Jugar, Curar, Ducharse
from modelo import Lulu
from estado import Estado
from gestor_de_estados import GestorDeEstados
from minijuego import Juegos
from recomendacion import obtener_recomendaciones

SAVE_PATH = "../saved_states/guardado.json"

# Obtener la ruta absoluta al directorio actual del script
current_dir = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(current_dir, "../assets/images")

# Diccionario de imágenes basadas en el estado de Lulu
IMAGES = {
    'despierto': ["despierto-1-00.gif", "despierto-1-01.gif"],
    'muerto': ["muerto.gif"],
    'quejarse-sucio': ["quejarse-sucio-1-00.gif", "quejarse-sucio-1-01.gif"],
    'quejarse': ["quejarse-1-00.gif", "quejarse-1-01.gif"],
    'dormido-enfermo-sucio': ["dormido-enfermo-sucio-1-00.gif", "dormido-enfermo-sucio-1-01.gif"],
    'despierto_enfermo_sucio': ["despierto-enfermo-sucio-1-00.gif", "despierto-enfermo-sucio-1-01.gif"],
    'dormido-enfermo': ["dormido-enfermo-1-00.gif", "dormido-enfermo-1-01.gif"],
    'despierto_enfermo': ["despierto-enfermo-1-00.gif", "despierto-enfermo-1-01.gif"],
    'dormido-sucio': ["dormido-sucio-1-00.gif", "dormido-sucio-1-01.gif"],
    'despierto_sucio': ["despierto-sucio-1-00.gif", "despierto-sucio-1-01.gif"],
    'dormido': ["dormido-1-00.gif", "dormido-1-01.gif"],
}

class LuluApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lulu")
        self.root.geometry("600x450")
        self.root.configure(bg="#ffffff")  # Fondo blanco
        self.gestor_estados = GestorDeEstados()
        self.estado = Estado()
        self.estado_inicial = self.gestor_estados.cargar_estado(Estado, SAVE_PATH)
        self.mi_lulu = Lulu(nombre="Lulu", estado=self.estado_inicial, root=root)
        
        # Inicializar juegos para la interfaz gráfica
        self.juegos = Juegos(self.root)

        # Añadir un Frame para la imagen de Lulu
        self.lulu_img_label = tk.Label(self.root, bg="#ffffff")
        self.lulu_img_label.pack(expand=True, fill=tk.BOTH, pady=10)  # Expandir y llenar el espacio disponible

        self.load_images()  # Cargar las imágenes iniciales
        self.current_image_index = 0  # Índice para alternar entre las dos imágenes
        self.update_image()  # Iniciar la actualización de la imagen

        # Añadir un Frame para mostrar mensajes
        self.mensaje_label = tk.Label(self.root, text="", wraplength=300, justify="center", bg="#ffffff", font=("Arial", 12, "italic"))
        self.mensaje_label.pack(pady=10)

        # Añadir un Frame para los botones de acciones
        self.create_buttons()
        
        # Crear un Frame para los botones de estadísticas y tips
        self.top_left_frame = tk.Frame(self.root, bg="#ffffff")
        self.top_left_frame.place(relx=0.0, rely=0.0, anchor="nw", x=10, y=10)

        # Añadir un botón para mostrar estadísticas
        self.boton_mostrar_estadistica = ttk.Button(self.top_left_frame, text="Mostrar Estadísticas", command=self.mostrar_estadisticas, width=20)
        self.boton_mostrar_estadistica.pack(side=tk.LEFT, padx=5)

        # Botón para mostrar recomendaciones
        self.boton_recomendaciones = ttk.Button(self.top_left_frame, text="Tips", command=self.mostrar_recomendaciones)
        self.boton_recomendaciones.pack(side=tk.LEFT, padx=5)

        # Añadir un Frame para mostrar estadísticas y recomendaciones
        self.estadisticas_recomendaciones_frame = tk.Frame(self.root, bg="#ffffff", bd=2, relief="solid")
        self.estadisticas_recomendaciones_label = tk.Label(self.estadisticas_recomendaciones_frame, text="", justify="left", anchor="nw", bg="#ffffff", font=("Arial", 12, "italic"))
        self.estadisticas_recomendaciones_label.pack(padx=10, pady=10)

        self.root.after(30000, self.guardar_estado_auto)  # 30 segundos

        # Manejar el cierre de la aplicación
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def load_images(self):
        self.images = {}
        for key, filenames in IMAGES.items():
            self.images[key] = []
            for filename in filenames:
                image_path = os.path.join(IMAGE_DIR, filename)
                if os.path.exists(image_path):
                    image = Image.open(image_path)
                    image = image.resize((360, 240), Image.LANCZOS)
                    self.images[key].append(ImageTk.PhotoImage(image))
                else:
                    print(f"Error: La imagen no se encuentra en la ruta: {image_path}")

    def update_image(self):
        key = self.get_image_key(self.estado)
        if key in self.images:
            if len(self.images[key]) > 1:
                self.lulu_img_label.config(image=self.images[key][self.current_image_index])
                self.current_image_index = (self.current_image_index + 1) % 2
            else:
                self.lulu_img_label.config(image=self.images[key][0])
        self.root.after(400, self.update_image)

    def get_image_key(self, estado):
        if estado.estas_muerto():
            return 'muerto'
        elif estado.estas_dormido() and estado.estas_enfermo():
            if estado.estas_sucio():
                return 'dormido-enfermo-sucio'
            return 'dormido-enfermo'
        elif estado.estas_dormido() and estado.estas_sucio():
            return 'dormido-sucio'
        elif estado.estas_dormido():
            return 'dormido'
        elif estado.tienes_quejas() and estado.estas_sucio():
            return 'quejarse-sucio'
        elif estado.tienes_quejas():
            return 'quejarse'
        elif estado.estas_sucio():
            return 'despierto-sucio'
        elif estado.estas_enfermo():
            return 'despierto-enfermo'
        else:
            return 'despierto'

    def create_buttons(self):
        # Frame para los botones de acciones
        frame_botones = tk.Frame(self.root, bg="#ffffff")
        frame_botones.pack(pady=10)
        # Crear botones para cada acción
        self.acciones = {
            "Comer": Comer(self.mi_lulu, self.mostrar_mensaje),
            "Jugar": lambda: self.realizar_accion(Jugar(self.mi_lulu, self.mostrar_mensaje, self.root)),
            "Curar": Curar(self.mi_lulu, self.mostrar_mensaje),
            "Ducharse": Ducharse(self.mi_lulu, self.mostrar_mensaje),
        }
        for nombre, accion in self.acciones.items():
            button = ttk.Button(frame_botones, text=nombre, command=lambda a=accion: self.realizar_accion(a), width=10)
            button.pack(side=tk.LEFT, padx=10, pady=10)

    def realizar_accion(self, accion):
        if callable(accion):
            accion()
        else:
            accion.realizar()

    def mostrar_estadisticas(self):
        stats_text = f"Energia: {self.mi_lulu.estado.energia}\nFelicidad: {self.mi_lulu.estado.felicidad}\nHambre: {self.mi_lulu.estado.hambre}\nSuciedad: {self.mi_lulu.estado.suciedad}\nSalud: {self.mi_lulu.estado.salud}"
        self.estadisticas_recomendaciones_label.config(text=stats_text)
        self.estadisticas_recomendaciones_frame.place(x=10, y=40)  # Mostrar el frame en la posición deseada
        self.root.after(2000, self.ocultar_estadisticas_recomendaciones)  # Ocultar estadísticas y recomendaciones después de 2 segundos

    def ocultar_estadisticas_recomendaciones(self):
        self.estadisticas_recomendaciones_frame.place_forget()  # Ocultar el frame de estadísticas y recomendaciones
        self.boton_mostrar_estadistica.pack(side=tk.LEFT, padx=5)  # Mostrar el botón de estadísticas nuevamente
        self.boton_recomendaciones.pack(side=tk.LEFT, padx=5)  # Mostrar el botón de recomendaciones nuevamente

    def mostrar_recomendaciones(self):
        try:
            recomendaciones = obtener_recomendaciones()
            self.estadisticas_recomendaciones_label.config(text='\n'.join(recomendaciones))
            self.estadisticas_recomendaciones_frame.place(x=10, y=40)  # Mostrar el frame en la posición deseada
            self.root.after(2000, self.ocultar_estadisticas_recomendaciones)  # Ocultar estadísticas y recomendaciones después de 2 segundos
        except Exception as e:
            self.estadisticas_recomendaciones_label.config(text=f"Error: {e}")
            self.estadisticas_recomendaciones_frame.place(x=10, y=40)
            self.root.after(2000, self.ocultar_estadisticas_recomendaciones)

    def mostrar_mensaje(self, mensaje):
        self.mensaje_label.config(text=mensaje)
        self.root.after(1000, self.borrar_mensaje)  # Borrar el mensaje después de 1 segundo

    def borrar_mensaje(self):
        self.mensaje_label.config(text="")

    def guardar_estado_auto(self):
        print("Guardando estado automáticamente...")
        self.gestor_estados.guardar_estado(self.mi_lulu.estado, SAVE_PATH)
        self.root.after(30000, self.guardar_estado_auto)  # Programa el próximo guardado

    def on_closing(self):
        self.gestor_estados.guardar_estado(self.mi_lulu.estado, SAVE_PATH)
        self.estado.detener_actualizacion_automatica()
        self.root.destroy()  # Cerrar la ventana

if __name__ == "__main__":
    root = tk.Tk()
    app = LuluApp(root)
    root.mainloop()