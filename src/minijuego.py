import os
import tkinter as tk
from tkinter import ttk, PhotoImage, Toplevel
import random

class Juego:
    """Clase base abstracta para definir un juego."""
    def __init__(self, callback=None, root=None):
        self.callback = callback
        self.root = root
        self.window = None

    def jugar(self):
        """Método abstracto para jugar un juego."""
        self.window = Toplevel(self.root)
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)  # Capturar cierre de ventana

    def on_closing(self):
        self.callback(False)  # Llamar al callback con False al cerrar la ventana

    def cerrar_juego(self, resultado):
        if self.window:
            self.window.destroy()
            self.callback(resultado)  # Llamar al callback al cerrar el juego
    
    def ocultar_widgets(self, widgets):
        for widget in widgets:
            widget.pack_forget()

    def _cerrar_ventana_despues_de_mostrar_resultado(self, mensaje, label):
        label.config(text=mensaje)
        self.root.after(2000, lambda: self.cerrar_juego("¡Lulu ganó!" in mensaje))

class AdivinaElNumero(Juego):
    """Implementación del juego Adivina el Número."""
    
    def __init__(self, callback=None, root=None):
        super().__init__(callback, root)
        self.numero_random = random.randint(1, 100)
        self.intentos = 0

    def jugar(self):
        if self.root:
            self.jugar_interfaz()
        else:
            self.jugar_terminal()

    def jugar_terminal(self):
        print("\n*** Adivina el Número ***\n")
        self.intentos = self._obtener_intentos_terminal()
        print("Tengo un número entre 1 y 100")
        for contador in range(1, self.intentos + 1):
            numero = self._obtener_numero_terminal()
            if numero > self.numero_random:
                print(f"Mi número es menor que {numero}.")
            elif numero < self.numero_random:
                print(f"Mi número es mayor que {numero}.")
            else:
                print(f"¡Acertaste! Y en tan solo {contador} intento(s).")
                if self.callback:
                    self.callback(True)
                return
        print("No te quedan intentos. \n\033[91mHas perdido!!\033[0m")
        print(f"El número era {self.numero_random}.")
        if self.callback:
            self.callback(False)

    def _obtener_intentos_terminal(self):
        while True:
            try:
                intentos = int(input("Cantidad máxima de intentos: "))
                if intentos > 0:
                    return intentos
                else:
                    print("El número debe ser mayor a 0.")
            except ValueError:
                print("Por favor, ingresa un número válido.")

    def _obtener_numero_terminal(self):
        while True:
            try:
                numero = int(input("Intenta adivinar mi número: "))
                if 1 <= numero <= 100:
                    return numero
                else:
                    print("Por favor, ingresa un número entre 1 y 100.")
            except ValueError:
                print("Por favor, ingresa un número válido.")

    def jugar_interfaz(self):
        self.window = tk.Toplevel(self.root)
        self.window.title("Adivina el Número")
        self.window.geometry(("350x150"))
        self.window.configure(bg="#ffffff")

        self.label = tk.Label(self.window, text="Tengo un número entre 1 y 100. ¿Cuántos intentos quieres?", bg="#ffffff")
        self.label.pack(pady=10)

        self.intentos_entry = tk.Entry(self.window)
        self.intentos_entry.pack(pady=5)

        self.boton_intentos = tk.Button(self.window, text="Aceptar", command=self.establecer_intentos_interfaz)
        self.boton_intentos.pack(pady=5)

    def establecer_intentos_interfaz(self):
        try:
            self.intentos = int(self.intentos_entry.get())
            if self.intentos > 0:
                self.label.config(text="Intenta adivinar mi número:", bg="#ffffff")
                self.intentos_entry.delete(0, tk.END)
                self.boton_intentos.config(text="Adivinar", command=self.adivinar_numero_interfaz)
            else:
                self.label.config(text="El número debe ser mayor a 0.", bg="#ffffff")
        except ValueError:
            self.label.config(text="Por favor, ingresa un número válido.", bg="#ffffff")

    def adivinar_numero_interfaz(self):
        try:
            numero = int(self.intentos_entry.get())
            if 1 <= numero <= 100:
                if numero > self.numero_random:
                    self.label.config(text=f"Mi número es menor que {numero}.", bg="#ffffff")
                elif numero < self.numero_random:
                    self.label.config(text=f"Mi número es mayor que {numero}.", bg="#ffffff")
                else:
                    self.ocultar_widgets([self.intentos_entry, self.boton_intentos])
                    self._cerrar_ventana_despues_de_mostrar_resultado("¡Acertaste!", self.label)
                    if self.callback:
                        self.callback(True)
                    return
                self.intentos -= 1
                if self.intentos == 0:
                    self.ocultar_widgets([self.intentos_entry, self.boton_intentos])
                    self._cerrar_ventana_despues_de_mostrar_resultado(f"No te quedan intentos. ¡Has perdido! El número era {self.numero_random}.", self.label)
                    if self.callback:
                        self.callback(False)
            else:
                self.label.config(text="Por favor, ingresa un número entre 1 y 100.", bg="#ffffff")
        except ValueError:
            self.label.config(text="Por favor, ingresa un número válido.", bg="#ffffff")

class PiedraPapelTijeras(Juego):
    """Implementación del juego Piedra, Papel, Tijeras."""

    def __init__(self, callback=None, root=None):
        super().__init__(callback, root)
        self.opciones = ["Piedra", "Papel", "Tijeras"]
        self.opcion_lulu = ""
        self.opcion_usuario = ""
        self.resultado_label = None

        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.IMAGE_DIR = os.path.join(current_dir, "../assets/images")
        self.imagenes = {
            "Piedra": PhotoImage(file=os.path.join(self.IMAGE_DIR, "piedra.gif")).subsample(6, 6),
            "Papel": PhotoImage(file=os.path.join(self.IMAGE_DIR, "papel.gif")).subsample(6, 6),
            "Tijeras": PhotoImage(file=os.path.join(self.IMAGE_DIR, "tijera.gif")).subsample(6, 6)
        }
        self.animacion_imgs = [self.imagenes["Piedra"], self.imagenes["Papel"], self.imagenes["Tijeras"]]
        self.animacion_index = 0
        self.animacion_intervalo = 800
        self.animacion_running = True  # Controlar si la animación está en curso

    def jugar(self):
        if self.root:
            self.jugar_interfaz()
        else:
            self.jugar_terminal()

    def jugar_terminal(self):
        opciones = ["Piedra", "Papel", "Tijeras"]
        print("\n¡Vamos a jugar a Piedra, Papel o Tijeras!")
        print("Opciones: Piedra, Papel, Tijeras")
        while True:
            lulu_opcion = random.choice(opciones)
            usuario_opcion = self._obtener_opcion_usuario_terminal(opciones)
            print(f"Lulu eligió: {lulu_opcion}")
            if usuario_opcion == lulu_opcion:
                print("¡Es un empate! Juguemos de nuevo.")
            elif self._usuario_gana(usuario_opcion, lulu_opcion):
                print("¡Ganaste!")
                if self.callback:
                    self.callback(True)
                return
            else:
                print("¡Lulu ganó!")
                if self.callback:
                    self.callback(False)
                return

    def _obtener_opcion_usuario_terminal(self, opciones):
        while True:
            usuario_opcion = input("Elige tu opción: ").capitalize()
            if usuario_opcion in opciones:
                return usuario_opcion
            else:
                print("Por favor elige Piedra, Papel o Tijeras.")

    def jugar_interfaz(self):
        self.window = tk.Toplevel(self.root)
        self.window.title("Piedra, Papel, Tijeras")
        self.window.geometry("520x550")
        self.window.configure(bg="#ffffff")

        self.label = tk.Label(self.window, text="Vamos a jugar a Piedra, Papel o Tijeras.", bg="#ffffff")
        self.label.pack(pady=10)

        self.lulu_img_label = tk.Label(self.window, text="Lulu:", bg="#ffffff")
        self.lulu_img_label.pack()

        self.lulu_img = tk.Label(self.window, image=self.imagenes["Piedra"], bg="#ffffff")
        self.lulu_img.pack()

        self.usuario_img_label = tk.Label(self.window, text="Usuario:", bg="#ffffff")
        self.usuario_img_label.pack()

        self.usuario_img = tk.Label(self.window, image=self.imagenes["Piedra"], bg="#ffffff")
        self.usuario_img.pack()

        self.resultado_label = tk.Label(self.window, text="", bg="#ffffff")
        self.resultado_label.pack(pady=10)

        # Crear un frame para los botones
        self.boton_frame = tk.Frame(self.window, bg="#ffffff")
        self.boton_frame.pack(side=tk.BOTTOM, pady=20)

        self.boton_piedra = tk.Button(self.boton_frame, image=self.imagenes["Piedra"], command=lambda: self.elegir_opcion("Piedra"))
        self.boton_piedra.configure(borderwidth=0, highlightthickness=0)
        self.boton_piedra.pack(side=tk.LEFT, padx=10)

        self.boton_papel = tk.Button(self.boton_frame, image=self.imagenes["Papel"], command=lambda: self.elegir_opcion("Papel"))
        self.boton_papel.configure(borderwidth=0, highlightthickness=0)
        self.boton_papel.pack(side=tk.LEFT, padx=10)

        self.boton_tijeras = tk.Button(self.boton_frame, image=self.imagenes["Tijeras"], command=lambda: self.elegir_opcion("Tijeras"))
        self.boton_tijeras.configure(borderwidth=0, highlightthickness=0)
        self.boton_tijeras.pack(side=tk.LEFT, padx=10)

        self._animar_imagenes()

    def _animar_imagenes(self):
        """Función para animar las imágenes de Lulu y Usuario."""
        if self.animacion_running:  # Verificar si la animación está en curso
            self.animacion_index = (self.animacion_index + 1) % len(self.animacion_imgs)
            self.lulu_img.config(image=self.animacion_imgs[self.animacion_index])
            self.usuario_img.config(image=self.animacion_imgs[self.animacion_index])
            self.window.after(self.animacion_intervalo, self._animar_imagenes)

    def elegir_opcion(self, eleccion_usuario):
        self.animacion_running = False  # Detener la animación
        self.opcion_usuario = eleccion_usuario
        self.opcion_lulu = random.choice(self.opciones)

        # Actualizar imágenes según las selecciones
        self.lulu_img.config(image=self.imagenes[self.opcion_lulu])
        self.usuario_img.config(image=self.imagenes[self.opcion_usuario])

        # Ocultar botones después de jugar
        self.boton_frame.pack_forget()

        # Mostrar resultado
        resultado = self._obtener_resultado(self.opcion_usuario, self.opcion_lulu)

        # Cerrar ventana después de mostrar resultado
        self._cerrar_ventana_despues_de_mostrar_resultado(resultado, self.resultado_label)

    def _obtener_resultado(self, usuario_opcion, lulu_opcion):
        if usuario_opcion == lulu_opcion:
            return "¡Es un empate!"
        elif (usuario_opcion == "Piedra" and lulu_opcion == "Tijeras") or \
            (usuario_opcion == "Papel" and lulu_opcion == "Piedra") or \
            (usuario_opcion == "Tijeras" and lulu_opcion == "Papel"):
            return "¡Ganaste!"
        else:
            return "¡Lulu ganó!"

class Juegos:
    """Clase para manejar varios juegos disponibles."""

    def __init__(self, root=None):
        self.root = root
        self.juegos = {
            "Adivina el Número": AdivinaElNumero,
            "Piedra, Papel, Tijeras": PiedraPapelTijeras
        }
    
    def seleccionar_juego(self, callback=None):
        if self.root:
            self.seleccionar_juego_interfaz(callback)
        else:
            self.seleccionar_juego_terminal(callback)

    def seleccionar_juego_terminal(self, callback):
        print("\nJuegos disponibles:")
        for clave, juego in self.juegos.items():
            print(f"{clave}. {juego.__name__}")
        opcion = input("Selecciona un juego: ")
        juego_clase = self.juegos.get(opcion)
        if juego_clase:
            juego = juego_clase(callback)
            return juego.jugar()
        else:
            print("¡Opción inválida!")
            return False

    def seleccionar_juego_interfaz(self, callback):
        self.window = tk.Toplevel(self.root)
        self.window.title("Selecciona un Juego")
        self.window.geometry("300x150")
        self.window.configure(bg="#ffffff")

        self.label = tk.Label(self.window, text="Selecciona un juego:", bg="#ffffff")
        self.label.pack(pady=10)

        self.juego_var = tk.StringVar(value="Adivina el Número")
        self.juegos_menu = ttk.Combobox(self.window, textvariable=self.juego_var, values=list(self.juegos.keys()), state="readonly")
        self.juegos_menu.pack(pady=5)

        self.boton_seleccionar = tk.Button(self.window, text="Seleccionar", command=lambda: self.iniciar_juego(callback))
        self.boton_seleccionar.pack(pady=5)

    def iniciar_juego(self, callback):
        juego_clase = self.juegos.get(self.juego_var.get())
        if juego_clase:
            juego = juego_clase(callback, self.root)
            juego.jugar()
            self.window.destroy()

# para prueba
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    juegos = Juegos(root)
    juegos.seleccionar_juego()
    root.mainloop()
