import math
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import time
import random

class SimulacionParcialGUI:
    def __init__(self, root, radiofarmacos):
        self.root = root
        self.radiofarmacos = radiofarmacos
        
        # Variables de simulación
        self.tiempos = []
        self.actividades = []
        self.start_time = 0
        self.tiempo_simulacion_real = 0
        self.tiempo_simulacion = 0
        self.actividad_inicial = 0
        self.vida_media = 0
        self.color = "#3498DB"
        
        # Configuración de la ventana principal
        self.root.title("Simulador de Decaimiento Parcial")
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
        self.left_frame = ctk.CTkFrame(self.main_frame, fg_color="#2C3E50", corner_radius=10, width=300)
        self.left_frame.pack(side="left", padx=5, pady=5, fill="both", expand=True)        
        self.right_frame = ctk.CTkFrame(self.main_frame, fg_color="#2C3E50", corner_radius=10)
        self.right_frame.pack(side="right", padx=5, pady=5, fill="both", expand=True)
        
        # Introducción en columna izquierda
        intro_texto = """
        ☢ SIMULADOR DE 
           DECAIMIENTO PARCIAL ☢
        
        Visualiza el comportamiento 
        del radiofármaco en tiempo real
        con control preciso del tiempo
        de simulación.
        
        Características:
        • Control de tiempo real vs simulado
        • Gráfica de decaimiento en tiempo real
        • Datos de vida media precisos
        • Personalización completa
        """
        ctk.CTkLabel(
            self.left_frame, 
            text=intro_texto, 
            font=("Arial Bold", 14),
            text_color="white",
            fg_color="transparent",
            justify="left"
        ).pack(padx=20, pady=20)
        
        # Controles en columna izquierda
        ctk.CTkLabel(
            self.left_frame, 
            text="Parámetros de Simulación", 
            font=("Arial Bold", 16)
        ).pack(pady=(10,20))
        
        # Radiofármaco
        ctk.CTkLabel(self.left_frame, text="Radiofármaco:").pack(anchor="w", padx=20)
        self.combo_radiofarmaco = ctk.CTkComboBox(
            self.left_frame, 
            values=list(self.radiofarmacos.keys()),
            width=250,
            fg_color="#34495E",
            text_color="white"
        )
        self.combo_radiofarmaco.pack(pady=(0,10), padx=20)
        self.combo_radiofarmaco.set("Fluor-18")
        
        # Actividad Inicial
        ctk.CTkLabel(self.left_frame, text="Actividad Inicial (MBq):").pack(anchor="w", padx=20)
        self.entry_actividad = ctk.CTkEntry(
            self.left_frame, 
            placeholder_text="Ingrese actividad inicial",
            width=250,
            fg_color="#34495E",
            text_color="white"
        )
        self.entry_actividad.pack(pady=(0,10), padx=20)
        self.entry_actividad.insert(0, "100")
        
        # Tiempo total a simular
        ctk.CTkLabel(self.left_frame, text="Tiempo total a simular (horas):").pack(anchor="w", padx=20)
        self.entry_tiempo_simulacion = ctk.CTkEntry(
            self.left_frame, 
            placeholder_text="Tiempo de simulación",
            width=250,
            fg_color="#34495E",
            text_color="white"
        )
        self.entry_tiempo_simulacion.pack(pady=(0,10), padx=20)
        self.entry_tiempo_simulacion.insert(0, "5")
        
        # Tiempo real de simulación
        ctk.CTkLabel(self.left_frame, text="Tiempo real (minutos):").pack(anchor="w", padx=20)
        self.entry_tiempo_real = ctk.CTkEntry(
            self.left_frame, 
            placeholder_text="Tiempo en minutos",
            width=250,
            fg_color="#34495E",
            text_color="white"
        )
        self.entry_tiempo_real.pack(pady=(0,10), padx=20)
        self.entry_tiempo_real.insert(0, "1")
        
        # Información de tiempo
        self.tiempo_label = ctk.CTkLabel(
            self.left_frame, 
            text="Tiempo transcurrido: 0.00 h", 
            font=("Arial", 12)
        )
        self.tiempo_label.pack(pady=(10,0), padx=20)
        
        self.actividad_label = ctk.CTkLabel(
            self.left_frame, 
            text="Actividad actual: 0.00 MBq", 
            font=("Arial", 12)
        )
        self.actividad_label.pack(pady=(5,10), padx=20)
        
        # Botones
        botones_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
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
                




        
    def _configurar_graficas(self):
        """Configura los elementos gráficos"""
        # Título en el panel derecho
        ctk.CTkLabel(
            self.right_frame, 
            text="Simulación de Decaimiento Radiactivo", 
            font=("Arial Bold", 18)
        ).pack(pady=10)
        
        # Configuración de la gráfica
        self.fig, self.ax = plt.subplots(facecolor="#212F3D", figsize=(10, 6))
        self.ax.set_facecolor("#212F3D")
        self.ax.set_xlabel("Tiempo (horas)", color='white')
        self.ax.set_ylabel("Actividad (MBq)", color='white')
        self.ax.tick_params(colors='white')
        self.ax.grid(color='gray', linestyle='--', linewidth=0.5)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_frame)
        self.canvas.get_tk_widget().pack(pady=10, padx=10, expand=True, fill="both")
        
        # Información adicional
        info_frame = ctk.CTkFrame(self.right_frame, fg_color="#34495E", corner_radius=5)
        info_frame.pack(fill="x", padx=10, pady=10)
        
        # Información sobre la vida media del elemento seleccionado
        self.vida_media_label = ctk.CTkLabel(
            info_frame,
            text="Vida media: - horas",
            font=("Arial", 12)
        )
        self.vida_media_label.pack(side="left", padx=20, pady=10)
        
        # Fecha y hora de simulación
        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.fecha_label = ctk.CTkLabel(
            info_frame,
            text=f"Fecha: {fecha_actual}",
            font=("Arial", 12)
        )
        self.fecha_label.pack(side="right", padx=20, pady=10)
    
    def calcular_actividad_restante(self, actividad_inicial, tiempo, vida_media):
        """Calcula la actividad restante en función del tiempo y la vida media"""
        lambda_ = math.log(2) / vida_media
        return actividad_inicial * math.exp(-lambda_ * tiempo)
    
    def actualizar_grafica(self):
        """Actualiza la gráfica con los nuevos datos de la simulación"""
        tiempo_real = (time.time() - self.start_time) / 60  # Convertir segundos a minutos
        tiempo_escalado = (tiempo_real / self.tiempo_simulacion_real) * self.tiempo_simulacion
        
        actividad_actual = self.calcular_actividad_restante(
            self.actividad_inicial, 
            tiempo_escalado, 
            self.vida_media
        )
        
        self.tiempos.append(tiempo_escalado)
        self.actividades.append(actividad_actual)
        
        # Actualizar gráfica
        self.ax.clear()
        self.ax.set_facecolor("#212F3D")
        self.ax.plot(self.tiempos, self.actividades, marker='o', color=self.color, linewidth=3)
        self.ax.set_xlabel("Tiempo (horas)", color='white')
        self.ax.set_ylabel("Actividad (MBq)", color='white')
        self.ax.tick_params(colors='white')
        self.ax.grid(color='gray', linestyle='--', linewidth=0.5)
        self.canvas.draw()
        
        # Actualizar etiquetas de información
        self.tiempo_label.configure(text=f"Tiempo transcurrido: {tiempo_escalado:.2f} h")
        self.actividad_label.configure(text=f"Actividad actual: {actividad_actual:.2f} MBq")
        
        # Continuar actualizando si no se ha alcanzado el tiempo de simulación
        if tiempo_escalado < self.tiempo_simulacion:
            self.root.after(100, self.actualizar_grafica)
    
    def iniciar_simulacion(self):
        """Inicia la simulación con los parámetros ingresados"""
        # Obtener parámetros
        radiofarmaco = self.combo_radiofarmaco.get()
        self.vida_media = self.radiofarmacos[radiofarmaco]["vida_media"]
        self.color = self.radiofarmacos[radiofarmaco]["color"]
        
        self.actividad_inicial = float(self.entry_actividad.get())
        self.tiempo_simulacion = float(self.entry_tiempo_simulacion.get())
        self.tiempo_simulacion_real = float(self.entry_tiempo_real.get())
        
        # Actualizar información de vida media
        self.vida_media_label.configure(text=f"Vida media: {self.vida_media} horas")
        
        # Inicializar datos
        self.start_time = time.time()
        self.tiempos = [0]
        self.actividades = [self.actividad_inicial]
        
        # Iniciar actualización
        self.actualizar_grafica()
    
    def reiniciar(self):
        """Reinicia la simulación y limpia la interfaz"""
        # Limpiar entradas
        self.entry_actividad.delete(0, "end")
        self.entry_actividad.insert(0, "100")
        
        self.entry_tiempo_simulacion.delete(0, "end")
        self.entry_tiempo_simulacion.insert(0, "5")
        
        self.entry_tiempo_real.delete(0, "end")
        self.entry_tiempo_real.insert(0, "1")
        
        # Reiniciar etiquetas
        self.tiempo_label.configure(text="Tiempo transcurrido: 0.00 h")
        self.actividad_label.configure(text="Actividad actual: 0.00 MBq")
        self.vida_media_label.configure(text="Vida media: - horas")
        
        # Limpiar gráfica
        self.ax.clear()
        self.ax.set_facecolor("#212F3D")
        self.ax.set_xlabel("Tiempo (horas)", color='white')
        self.ax.set_ylabel("Actividad (MBq)", color='white')
        self.ax.tick_params(colors='white')
        self.ax.grid(color='gray', linestyle='--', linewidth=0.5)
        self.canvas.draw()
        
        # Reiniciar variables
        self.tiempos = []
        self.actividades = []
    
    def cerrar_app(self):
        """Cierra la aplicación"""
        self.root.quit()
        self.root.destroy()

# Para pruebas independientes del archivo
if __name__ == "__main__":
    # Diccionario con los radiofármacos y sus datos
    radiofarmacos = {
        "Fluor-18": {"vida_media": 1.83, "color": "#8E44AD", "aplicacion": "PET", "descripcion": "Usado en FDG para estudios metabólicos"},
        "Tecnecio-99m": {"vida_media": 6.01, "color": "#3498DB", "aplicacion": "SPECT", "descripcion": "Ampliamente usado en medicina nuclear"},
        "Yodo-131": {"vida_media": 192.5, "color": "#2ECC71", "aplicacion": "Terapia", "descripcion": "Usado en tratamiento de tiroides"},
        "Carbono-11": {"vida_media": 0.33, "color": "#E74C3C", "aplicacion": "PET", "descripcion": "Para estudios neurológicos"},
        "Nitrógeno-13": {"vida_media": 0.17, "color": "#F39C12", "aplicacion": "PET", "descripcion": "Estudios de perfusión miocárdica"}
    }
    
    # Configuración
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    root = ctk.CTk()
    app = SimulacionParcialGUI(root, radiofarmacos)
    root.mainloop()