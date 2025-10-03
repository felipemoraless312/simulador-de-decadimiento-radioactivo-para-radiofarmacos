import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import subprocess  # Necesario para ejecutar archivos Python


class SimuladorGUI:
    def __init__(self, root, radiofarmacos, escala_tiempo_dict, simulador):
        self.root = root
        self.radiofarmacos = radiofarmacos
        self.escala_tiempo_dict = escala_tiempo_dict
        self.simulador = simulador
        
        # Configuración de la ventana principal
        self.root.title("Simulador de Decaimiento Radiactivo")
        self.root.geometry("1024x600")
        self.root.configure(fg_color="#1B2631")
        
        # Inicializar interfaz
        self._crear_interfaz()
        self._configurar_graficas()
        
    def _crear_interfaz(self):
        """Crea todos los elementos de la interfaz de usuario"""
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        # División en dos columnas
        self.left_frame = ctk.CTkFrame(self.main_frame, fg_color="#2C3E50", corner_radius=10)
        self.left_frame.pack(side="left", padx=5, pady=5, fill="both", expand=True)
        
        self.right_frame = ctk.CTkFrame(self.main_frame, fg_color="#2C3E50", corner_radius=10)
        self.right_frame.pack(side="right", padx=5, pady=5, fill="both", expand=True)
        
        # Introducción en columna izquierda
        intro_texto = """
        ☢ SIMULADOR DE 
           DECAIMIENTO RADIACTIVO ☢
        Visualiza el comportamiento 
        de radiofármacos en tiempo 
        real.
        Características:
        • Simulación de vidas medias
        • Gráfica de decaimiento
        • Animación de partículas
        • Información detallada
        """
        ctk.CTkLabel(
            self.left_frame, 
            text=intro_texto, 
            font=("Arial Bold", 14),
            text_color="white",
            fg_color="transparent",
            justify="left"
        ).pack(padx=20, pady=20)
        
        # Botón de detalles de radiofármaco
        ctk.CTkButton(
            self.left_frame, 
            text="Ver Detalles", 
            command=self.mostrar_detalles_radiofarmaco,
            fg_color="#E74C3C",
            hover_color="#C0392B"
        ).pack(pady=10)
        
        # Controles en columna derecha
        ctk.CTkLabel(
            self.right_frame, 
            text="Parámetros de Simulación", 
            font=("Arial Bold", 16)
        ).pack(pady=(10,20))
        
        # Radiofármaco
        ctk.CTkLabel(self.right_frame, text="Radiofármaco:").pack(anchor="w", padx=20)
        self.combo_radiofarmaco = ctk.CTkComboBox(
            self.right_frame, 
            values=list(self.radiofarmacos.keys()),
            width=250,
            fg_color="#34495E",
            text_color="white"
        )
        self.combo_radiofarmaco.pack(pady=(0,10), padx=20)
        self.combo_radiofarmaco.set("Fluor-18")
        
        # Escala de Tiempo
        ctk.CTkLabel(self.right_frame, text="Escala de Tiempo:").pack(anchor="w", padx=20)
        self.combo_escala = ctk.CTkComboBox(
            self.right_frame, 
            values=list(self.escala_tiempo_dict.keys()),
            width=250,
            fg_color="#34495E",
            text_color="white"
        )
        self.combo_escala.pack(pady=(0,10), padx=20)
        self.combo_escala.set("5 horas")
        
        # Actividad Inicial
        ctk.CTkLabel(self.right_frame, text="Actividad Inicial (MBq):").pack(anchor="w", padx=20)
        self.entry_actividad = ctk.CTkEntry(
            self.right_frame, 
            placeholder_text="Ingrese actividad inicial",
            width=250,
            fg_color="#34495E",
            text_color="white"
        )
        self.entry_actividad.pack(pady=(0,10), padx=20)
        
        # Actividad Deseada
        ctk.CTkLabel(self.right_frame, text="Actividad Deseada (MBq):").pack(anchor="w", padx=20)
        self.entry_actividad_deseada = ctk.CTkEntry(
            self.right_frame, 
            placeholder_text="Ingrese actividad deseada",
            width=250,
            fg_color="#34495E",
            text_color="white"
        )
        self.entry_actividad_deseada.pack(pady=(0,10), padx=20)
        
        # Botones
        botones_frame = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        botones_frame.pack(pady=10)
        
        ctk.CTkButton(
            botones_frame, 
            text="Iniciar", 
            command=self.iniciar_simulacion,
            fg_color="#2ECC71",
            hover_color="#27AE60",
            width=100
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            botones_frame, 
            text="Reiniciar", 
            command=self.reiniciar,
            fg_color="#F39C12",
            hover_color="#D35400",
            width=100
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            botones_frame, 
            text="Cerrar", 
            command=self.cerrar_app,
            fg_color="#E74C3C",
            hover_color="#C0392B",
            width=100
        ).pack(side="left", padx=5)

                # Nuevo botón de simulación parcial
        ctk.CTkButton(
            botones_frame, 
            text="Simulación parcial", 
            command=self.abrir_simulacion_parcial,  # Asumiendo que tienes una función llamada simulacion_parcial
            fg_color="#9B59B6",  # Morado
            hover_color="#8E44AD",  # Morado más oscuro para hover
            width=100
            ).pack(side="left", padx=5)


    def abrir_simulacion_parcial(self):
        # Aquí ejecutas el archivo Python "simulacion_parcial.py" usando subprocess
        try:
            subprocess.run(["python", "interfaz/sumulacion_parcial.py"], check=True)  # Ejecuta el archivo .py
        except subprocess.CalledProcessError as e:
            print(f"Error al ejecutar el archivo: {e}")



        
    def _configurar_graficas(self):
        """Configura los elementos gráficos (gráfica y animación)"""
        # Configuración de las gráficas
        self.fig, self.ax = plt.subplots(facecolor="#212F3D", figsize=(8, 6))
        self.fig.subplots_adjust(hspace=0.3)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_frame)
        self.canvas.get_tk_widget().pack(pady=10, expand=True, fill="both")
        
        # Lienzo de animación
        self.canvas_animation = ctk.CTkCanvas(
            self.right_frame, 
            width=300, 
            height=150, 
            bg="black", 
            highlightthickness=0
        )
        self.canvas_animation.pack(pady=10)
    
    def mostrar_detalles_radiofarmaco(self):
        """Muestra una ventana con detalles del radiofármaco seleccionado"""
        radiofarmaco = self.combo_radiofarmaco.get()
        detalles = self.radiofarmacos[radiofarmaco]
        
        # Crear ventana de detalles
        detalles_window = ctk.CTkToplevel(self.root)
        detalles_window.title(f"Detalles de {radiofarmaco}")
        detalles_window.geometry("350x400")
        detalles_window.configure(fg_color="#2C3E50")
        
        # Contenido de la ventana
        contenido = ctk.CTkFrame(detalles_window, fg_color="transparent")
        contenido.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Título
        ctk.CTkLabel(
            contenido, 
            text=radiofarmaco, 
            font=("Arial Bold", 18),
            text_color=detalles["color"]
        ).pack(pady=(0,10))
        
        # Detalles
        detalles_texto = f"""
        Vida Media: {detalles['vida_media']} horas
        
        Aplicación: {detalles['aplicacion']}
        
        Descripción: {detalles['descripcion']}
        
        Color de Representación:
        """
        
        ctk.CTkLabel(
            contenido, 
            text=detalles_texto,
            font=("Arial", 12),
            justify="left"
        ).pack()
        
        # Cuadro de color
        color_frame = ctk.CTkFrame(
            contenido, 
            width=100, 
            height=50, 
            fg_color=detalles["color"]
        )
        color_frame.pack(pady=10)
        
        # Botón de cerrar
        ctk.CTkButton(
            contenido, 
            text="Cerrar", 
            command=detalles_window.destroy,
            fg_color="#34495E",
            hover_color="#2C3E50"
        ).pack(pady=10)
    
    def iniciar_simulacion(self):
        """Inicia la simulación con los parámetros ingresados"""
        radiofarmaco = self.combo_radiofarmaco.get()
        vida_media = self.radiofarmacos[radiofarmaco]["vida_media"]
        color = self.radiofarmacos[radiofarmaco]["color"]
        
        actividad_inicial = float(self.entry_actividad.get())
        actividad_deseada = float(self.entry_actividad_deseada.get())
        escala_tiempo = self.escala_tiempo_dict[self.combo_escala.get()]
        
        # Iniciar simulación en el modelo
        self.simulador.iniciar_simulacion(
            actividad_inicial, 
            vida_media, 
            actividad_deseada, 
            escala_tiempo, 
            color
        )
        
        # Iniciar actualización en la interfaz
        self.actualizar_grafica()
    
    def actualizar_grafica(self):
        """Actualiza la gráfica y la animación con los nuevos datos"""
        # Obtener datos actualizados
        actividad_actual, _ = self.simulador.actualizar_calculos()
        
        # Limpiar gráfica
        self.ax.clear()
        
        # Configuración de la gráfica (decaimiento)
        self.ax.set_facecolor("#212F3D")
        self.ax.plot(
            self.simulador.tiempos, 
            self.simulador.actividades, 
            marker='o', 
            color=self.simulador.color, 
            label="Decaimiento", 
            linewidth=3
        )
        self.ax.set_title("Decaimiento Radiactivo", color='white', fontsize=10)
        self.ax.set_xlabel("Tiempo (horas)", color='white')
        self.ax.set_ylabel("Actividad (MBq)", color='white')
        self.ax.tick_params(colors='white')
        self.ax.grid(color='gray', linestyle='--', linewidth=0.5)
        
        self.canvas.draw()
        
        # Actualizar animación
        self.update_animation(int(actividad_actual))
        
        # Continuar actualizando si no se ha alcanzado la actividad deseada
        if actividad_actual > self.simulador.actividad_deseada:
            self.root.after(100, self.actualizar_grafica)
    
    def update_animation(self, n_particles):
        """Actualiza la animación visual de partículas"""
        self.canvas_animation.delete("all")
        
        # Generar partículas
        particulas = self.simulador.generar_particulas_random(n_particles)
        
        # Dibujar partículas
        for x, y, simbolo in particulas:
            self.canvas_animation.create_text(
                x, y, 
                text=simbolo, 
                fill=self.simulador.color, 
                font=("Arial", 20)
            )
        
        self.canvas_animation.update()
    
    def reiniciar(self):
        """Reinicia la simulación y limpia la interfaz"""
        self.entry_actividad.delete(0, "end")
        self.entry_actividad_deseada.delete(0, "end")
        
        self.ax.clear()
        self.ax.set_facecolor("#212F3D")
        self.canvas.draw()
        
        self.canvas_animation.delete("all")
        
        # Reiniciar datos de simulación
        self.simulador.reiniciar()
    
    def cerrar_app(self):
        """Cierra la aplicación"""
        self.root.quit()
        self.root.destroy()