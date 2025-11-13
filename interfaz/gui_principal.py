"""
Interfaz gráfica profesional para simulación de decaimiento radiactivo
Versión mejorada con control de actividad final, gamma y visualización avanzada
"""

import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import time
import math
import os
from tkinter import filedialog

# Importaciones de los módulos del proyecto
from config.constantes import COLORES
from utilidades.calculos import calcular_actividad_restante, calcular_tiempo_para_actividad

class SimuladorGUI:
    """Interfaz profesional para simulación con control avanzado"""
    
    def __init__(self, root, radiofarmacos, escalas_tiempo, simulador):
        self.root = root
        self.radiofarmacos = radiofarmacos
        self.escalas_tiempo = escalas_tiempo
        self.simulador = simulador
        
        # Variables de simulación
        self.tiempos = []
        self.actividades = []
        self.gammas = []
        self.start_time = 0
        self.tiempo_simulacion_real = 0
        self.tiempo_simulacion = 0
        self.actividad_inicial = 0
        self.actividad_final = 0
        self.vida_media = 0
        self.color = "#3498DB"
        self.simulacion_activa = False
        self.simulacion_pausada = False
        self.modo_simulacion = "tiempo"  # "tiempo" o "actividad"
        
        # Variables para punto seleccionado
        self.punto_seleccionado = None
        self.punto_marcado = None
        
        # Configurar ventana
        self._configurar_ventana()
        
        # Crear interfaz
        self._crear_interfaz()
        self._configurar_graficas()
        
    def _configurar_ventana(self):
        """Configura las propiedades de la ventana"""
        self.root.title("Simulador Profesional de Decaimiento Radiactivo")
        self.root.geometry("1400x800")
        self.root.configure(fg_color=COLORES["fondo_principal"])
        
    def _crear_interfaz(self):
        """Crea todos los elementos de la interfaz"""
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Crear paneles
        self._crear_panel_izquierdo()
        self._crear_panel_derecho()
        
    def _crear_panel_izquierdo(self):
        """Crea el panel izquierdo con controles"""
        # Frame principal izquierdo
        self.left_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=COLORES["fondo_frame"],
            corner_radius=10,
            width=400
        )
        self.left_frame.pack(side="left", fill="y", padx=(0, 5), pady=5)
        self.left_frame.pack_propagate(False)  # Importante: prevenir que se encoja
        
        # Crear un frame scrollable para el contenido
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self.left_frame,
            fg_color="transparent",
            width=380
        )
        self.scrollable_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Header
        self._crear_header()
        
        # Modo de simulación
        self._crear_selector_modo()
        
        # Controles de parámetros
        self._crear_controles()
        
        # Panel de fórmula
        self._crear_panel_formula()
        
        # Información en tiempo real
        self._crear_etiquetas_info()
        
        # Panel Gamma
        self._crear_panel_gamma()
        
        # Panel de botones - ¡ESTE ES EL QUE FALTABA!
        self._crear_panel_botones()
        
    def _crear_header(self):
        """Crea el encabezado del panel izquierdo"""
        header_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#1A1A2E", corner_radius=10)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            header_frame,
            text="SIMULADOR PROFESIONAL",
            font=("Arial Black", 16),
            text_color="#00D9FF"
        ).pack(pady=(10, 5))
        
        ctk.CTkLabel(
            header_frame,
            text="Decaimiento Radiactivo en Tiempo Real",
            font=("Arial", 11),
            text_color="#AAAAAA"
        ).pack(pady=(0, 5))
        
        ctk.CTkLabel(
            header_frame,
            text="Por: Felipe Morales",
            font=("Arial", 9),
            text_color="#888888"
        ).pack(pady=(0, 10))
        
    def _crear_selector_modo(self):
        """Crea el selector de modo de simulación"""
        modo_frame = ctk.CTkFrame(self.scrollable_frame, fg_color=COLORES["fondo_input"], corner_radius=10)
        modo_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            modo_frame,
            text="Modo de Simulación",
            font=("Arial Bold", 14),
            text_color="white"
        ).pack(pady=(10, 5))
        
        # Botones de modo
        botones_frame = ctk.CTkFrame(modo_frame, fg_color="transparent")
        botones_frame.pack(fill="x", padx=10, pady=(5, 10))
        
        self.btn_modo_tiempo = ctk.CTkButton(
            botones_frame,
            text="Por Tiempo",
            command=lambda: self._cambiar_modo("tiempo"),
            fg_color=COLORES["boton_iniciar"],
            hover_color=COLORES["boton_iniciar_hover"],
            height=35,
            font=("Arial Bold", 12)
        )
        self.btn_modo_tiempo.pack(side="left", fill="x", expand=True, padx=5)
        
        self.btn_modo_actividad = ctk.CTkButton(
            botones_frame,
            text="Por Actividad Final",
            command=lambda: self._cambiar_modo("actividad"),
            fg_color="#555555",
            hover_color="#666666",
            height=35,
            font=("Arial Bold", 12)
        )
        self.btn_modo_actividad.pack(side="left", fill="x", expand=True, padx=5)
        
    def _cambiar_modo(self, modo):
        """Cambia el modo de simulación"""
        if self.simulacion_activa:
            return
            
        self.modo_simulacion = modo
        
        if modo == "tiempo":
            self.btn_modo_tiempo.configure(fg_color=COLORES["boton_iniciar"])
            self.btn_modo_actividad.configure(fg_color="#555555")
            self.entry_tiempo_simulacion.configure(state="normal")
            self.entry_actividad_final.configure(state="disabled")
        else:
            self.btn_modo_tiempo.configure(fg_color="#555555")
            self.btn_modo_actividad.configure(fg_color=COLORES["boton_iniciar"])
            self.entry_tiempo_simulacion.configure(state="disabled")
            self.entry_actividad_final.configure(state="normal")
        
        self._actualizar_formula()
        
    def _crear_controles(self):
        """Crea los controles de parámetros"""
        control_frame = ctk.CTkFrame(self.scrollable_frame, fg_color=COLORES["fondo_input"], corner_radius=10)
        control_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            control_frame,
            text="Parámetros de Simulación",
            font=("Arial Bold", 14)
        ).pack(pady=(10, 15))
        
        # Radiofármaco
        ctk.CTkLabel(control_frame, text="Radiofármaco:", font=("Arial Bold", 11)).pack(anchor="w", padx=20)
        self.combo_radiofarmaco = ctk.CTkComboBox(
            control_frame,
            values=list(self.radiofarmacos.keys()),
            width=340,
            fg_color=COLORES["fondo_frame"],
            text_color="white",
            command=self._actualizar_formula,
            font=("Arial", 11)
        )
        self.combo_radiofarmaco.pack(fill="x", pady=(0, 10), padx=20)
        self.combo_radiofarmaco.set("Fluor-18")
        
        # Actividad Inicial
        ctk.CTkLabel(control_frame, text="Actividad Inicial (MBq):", font=("Arial Bold", 11)).pack(anchor="w", padx=20)
        self.entry_actividad = ctk.CTkEntry(
            control_frame,
            placeholder_text="Ej: 100",
            fg_color=COLORES["fondo_frame"],
            text_color="white",
            font=("Arial", 11)
        )
        self.entry_actividad.pack(fill="x", pady=(0, 10), padx=20)
        self.entry_actividad.insert(0, "100")
        self.entry_actividad.bind("<KeyRelease>", lambda e: self._actualizar_formula())
        
        # Actividad Final
        ctk.CTkLabel(
            control_frame, 
            text="Actividad Final (MBq):", 
            font=("Arial Bold", 11),
            text_color="#FFD700"
        ).pack(anchor="w", padx=20)
        self.entry_actividad_final = ctk.CTkEntry(
            control_frame,
            placeholder_text="Ej: 50",
            fg_color=COLORES["fondo_frame"],
            text_color="white",
            font=("Arial", 11),
            state="disabled"
        )
        self.entry_actividad_final.pack(fill="x", pady=(0, 10), padx=20)
        self.entry_actividad_final.insert(0, "50")
        self.entry_actividad_final.bind("<KeyRelease>", lambda e: self._actualizar_formula())
        
        # Tiempo total a simular
        ctk.CTkLabel(
            control_frame, 
            text="Tiempo total a simular (horas):",
            font=("Arial Bold", 11),
            text_color="#FFD700"
        ).pack(anchor="w", padx=20)
        self.entry_tiempo_simulacion = ctk.CTkEntry(
            control_frame,
            placeholder_text="Ej: 5",
            fg_color=COLORES["fondo_frame"],
            text_color="white",
            font=("Arial", 11)
        )
        self.entry_tiempo_simulacion.pack(fill="x", pady=(0, 10), padx=20)
        self.entry_tiempo_simulacion.insert(0, "5")
        self.entry_tiempo_simulacion.bind("<KeyRelease>", lambda e: self._actualizar_formula())
        
        # Tiempo real de simulación
        ctk.CTkLabel(control_frame, text="Duración real (minutos):", font=("Arial Bold", 11)).pack(anchor="w", padx=20)
        self.entry_tiempo_real = ctk.CTkEntry(
            control_frame,
            placeholder_text="Ej: 1",
            fg_color=COLORES["fondo_frame"],
            text_color="white",
            font=("Arial", 11)
        )
        self.entry_tiempo_real.pack(fill="x", pady=(0, 15), padx=20)
        self.entry_tiempo_real.insert(0, "1")
        
    def _crear_panel_formula(self):
        """Crea el panel con la fórmula sustituida"""
        formula_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#1A1A2E", corner_radius=10)
        formula_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            formula_frame,
            text="Fórmula de Decaimiento",
            font=("Arial Bold", 14),
            text_color="#00D9FF"
        ).pack(pady=(10, 10))
        
        # Frame para fórmula general
        self.formula_general_frame = ctk.CTkFrame(formula_frame, fg_color=COLORES["fondo_frame"], corner_radius=5)
        self.formula_general_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(
            self.formula_general_frame,
            text="Fórmula General:",
            font=("Arial Bold", 10),
            text_color="#AAAAAA"
        ).pack(pady=(5, 2))
        
        self.label_formula_general = ctk.CTkLabel(
            self.formula_general_frame,
            text="A(t) = A₀ · e^(-λt)",
            font=("Courier", 13, "bold"),
            text_color="white"
        )
        self.label_formula_general.pack(pady=(0, 5))
        
        # Frame para lambda
        self.lambda_frame = ctk.CTkFrame(formula_frame, fg_color=COLORES["fondo_frame"], corner_radius=5)
        self.lambda_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(
            self.lambda_frame,
            text="Constante de decaimiento (λ):",
            font=("Arial Bold", 10),
            text_color="#AAAAAA"
        ).pack(pady=(5, 2))
        
        self.label_lambda = ctk.CTkLabel(
            self.lambda_frame,
            text="λ = ln(2) / t½ = 0.0000 h⁻¹",
            font=("Courier", 11),
            text_color="#00FF88"
        )
        self.label_lambda.pack(pady=(0, 5))
        
        # Frame para sustitución
        self.sustitucion_frame = ctk.CTkFrame(formula_frame, fg_color=COLORES["fondo_frame"], corner_radius=5)
        self.sustitucion_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(
            self.sustitucion_frame,
            text="Sustitución:",
            font=("Arial Bold", 10),
            text_color="#AAAAAA"
        ).pack(pady=(5, 2))
        
        self.label_sustitucion = ctk.CTkLabel(
            self.sustitucion_frame,
            text="Ingrese valores...",
            font=("Courier", 10),
            text_color="#FFD700",
            wraplength=340
        )
        self.label_sustitucion.pack(pady=(0, 5), padx=5)
        
        # Frame para resultado
        self.resultado_frame = ctk.CTkFrame(formula_frame, fg_color="#00D9FF", corner_radius=5)
        self.resultado_frame.pack(fill="x", padx=10, pady=(5, 10))
        
        ctk.CTkLabel(
            self.resultado_frame,
            text="Resultado:",
            font=("Arial Bold", 10),
            text_color="#000000"
        ).pack(pady=(5, 2))
        
        self.label_resultado = ctk.CTkLabel(
            self.resultado_frame,
            text="---",
            font=("Courier", 12, "bold"),
            text_color="#000000"
        )
        self.label_resultado.pack(pady=(0, 5))
        
    def _actualizar_formula(self, event=None):
        """Actualiza la visualización de la fórmula con valores sustituidos"""
        try:
            radiofarmaco = self.combo_radiofarmaco.get()
            vida_media = self.radiofarmacos[radiofarmaco]["vida_media"]
            A0 = float(self.entry_actividad.get() or 0)
            
            # Calcular lambda
            lambda_val = math.log(2) / vida_media
            self.label_lambda.configure(
                text=f"λ = ln(2) / {vida_media} = {lambda_val:.6f} h⁻¹"
            )
            
            if self.modo_simulacion == "tiempo":
                t = float(self.entry_tiempo_simulacion.get() or 0)
                At = calcular_actividad_restante(A0, t, vida_media)
                
                self.label_formula_general.configure(text="A(t) = A₀ · e^(-λt)")
                self.label_sustitucion.configure(
                    text=f"A({t}) = {A0} · e^(-{lambda_val:.4f} × {t})"
                )
                self.label_resultado.configure(
                    text=f"A({t}) = {At:.4f} MBq"
                )
                
            else:  # modo actividad
                Af = float(self.entry_actividad_final.get() or 0)
                if Af >= A0 or Af <= 0:
                    self.label_sustitucion.configure(text="Actividad final debe ser menor que inicial")
                    return
                    
                t = calcular_tiempo_para_actividad(A0, Af, vida_media)
                
                # Actualizar automáticamente el campo de tiempo
                self.entry_tiempo_simulacion.delete(0, "end")
                self.entry_tiempo_simulacion.insert(0, f"{t:.4f}")
                
                self.label_formula_general.configure(text="t = -ln(Af / A₀) / λ")
                self.label_sustitucion.configure(
                    text=f"t = -ln({Af} / {A0}) / {lambda_val:.4f}"
                )
                self.label_resultado.configure(
                    text=f"t = {t:.4f} horas"
                )
                
        except (ValueError, ZeroDivisionError):
            pass
        
    def _crear_etiquetas_info(self):
        """Crea las etiquetas de información en tiempo real"""
        info_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#1A1A2E", corner_radius=10)
        info_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            info_frame,
            text="Información en Tiempo Real",
            font=("Arial Bold", 14),
            text_color="#00D9FF"
        ).pack(pady=(10, 10))
        
        # Tiempo
        tiempo_card = ctk.CTkFrame(info_frame, fg_color=COLORES["fondo_frame"], corner_radius=5)
        tiempo_card.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(tiempo_card, text="Tiempo Transcurrido", font=("Arial Bold", 10), text_color="#AAAAAA").pack(pady=(5, 2))
        self.tiempo_label = ctk.CTkLabel(
            tiempo_card,
            text="0.0000 h",
            font=("Arial Bold", 16),
            text_color="#00FF88"
        )
        self.tiempo_label.pack(pady=(0, 5))
        
        # Actividad
        actividad_card = ctk.CTkFrame(info_frame, fg_color=COLORES["fondo_frame"], corner_radius=5)
        actividad_card.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(actividad_card, text="Actividad Actual", font=("Arial Bold", 10), text_color="#AAAAAA").pack(pady=(5, 2))
        self.actividad_label = ctk.CTkLabel(
            actividad_card,
            text="0.0000 MBq",
            font=("Arial Bold", 16),
            text_color="#FFD700"
        )
        self.actividad_label.pack(pady=(0, 5))
        
        # Porcentaje
        porcentaje_card = ctk.CTkFrame(info_frame, fg_color=COLORES["fondo_frame"], corner_radius=5)
        porcentaje_card.pack(fill="x", padx=10, pady=(5, 10))
        
        ctk.CTkLabel(porcentaje_card, text="Porcentaje Restante", font=("Arial Bold", 10), text_color="#AAAAAA").pack(pady=(5, 2))
        self.porcentaje_label = ctk.CTkLabel(
            porcentaje_card,
            text="100.00%",
            font=("Arial Bold", 16),
            text_color="#00D9FF"
        )
        self.porcentaje_label.pack(pady=(0, 5))
        
    def _crear_panel_gamma(self):
        """Crea el panel de visualización de Gamma"""
        gamma_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#1A1A2E", corner_radius=10)
        gamma_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            gamma_frame,
            text="Factor Gamma (γ)",
            font=("Arial Bold", 14),
            text_color="#00D9FF"
        ).pack(pady=(10, 5))
        
        ctk.CTkLabel(
            gamma_frame,
            text="Intensidad Relativa de Radiación",
            font=("Arial", 9),
            text_color="#AAAAAA"
        ).pack(pady=(0, 10))
        
        # Valor de gamma
        self.gamma_valor_label = ctk.CTkLabel(
            gamma_frame,
            text="1.0000",
            font=("Arial Black", 48),
            text_color="#00FF88"
        )
        self.gamma_valor_label.pack(pady=10)
        
        # Barra de progreso visual
        self.gamma_progress = ctk.CTkProgressBar(
            gamma_frame,
            height=20,
            corner_radius=10,
            progress_color="#00FF88"
        )
        self.gamma_progress.pack(fill="x", pady=10, padx=10)
        self.gamma_progress.set(1.0)
        
        # Descripción
        self.gamma_desc_label = ctk.CTkLabel(
            gamma_frame,
            text="γ = Actividad Actual / Actividad Inicial\nRango: 1.0 (máxima) → 0.0 (mínima)",
            font=("Arial", 9),
            text_color="#AAAAAA"
        )
        self.gamma_desc_label.pack(pady=(5, 10))
        
    def _crear_panel_botones(self):
        """Crea el panel completo de botones de control"""
        botones_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#1A1A2E", corner_radius=10)
        botones_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            botones_frame,
            text="Control de Simulación",
            font=("Arial Bold", 14),
            text_color="#00D9FF"
        ).pack(pady=(10, 5))
        
        # Frame para botones principales
        botones_principales_frame = ctk.CTkFrame(botones_frame, fg_color="transparent")
        botones_principales_frame.pack(fill="x", padx=10, pady=5)
        
        # Botón Iniciar
        self.btn_iniciar = ctk.CTkButton(
            botones_principales_frame,
            text="INICIAR SIMULACIÓN",
            command=self.iniciar_simulacion,
            fg_color=COLORES["boton_iniciar"],
            hover_color=COLORES["boton_iniciar_hover"],
            height=45,
            font=("Arial Bold", 14),
            corner_radius=10
        )
        self.btn_iniciar.pack(fill="x", pady=5)
        
        # Botón Pausar/Reanudar
        self.btn_pausar = ctk.CTkButton(
            botones_principales_frame,
            text="⏸️",
            command=self.pausar_simulacion,
            fg_color="#F39C12",
            hover_color="#D35400",
            height=40,
            font=("Arial Bold", 13),
            corner_radius=10,
            state="disabled"
        )
        self.btn_pausar.pack(fill="x", pady=5)
        
        # Botón Detener
        self.btn_detener = ctk.CTkButton(
            botones_principales_frame,
            text="⏹️",
            command=self.detener_simulacion,
            fg_color="#E74C3C",
            hover_color="#C0392B",
            height=40,
            font=("Arial Bold", 13),
            corner_radius=10,
            state="disabled"
        )
        self.btn_detener.pack(fill="x", pady=5)
        
        # Frame para botones secundarios (2 columnas)
        botones_secundarios_frame = ctk.CTkFrame(botones_frame, fg_color="transparent")
        botones_secundarios_frame.pack(fill="x", padx=10, pady=5)
        
        # Columna izquierda - Botones de gestión
        col_izq = ctk.CTkFrame(botones_secundarios_frame, fg_color="transparent")
        col_izq.pack(side="left", fill="both", expand=True, padx=2)
        
        # Botón Reiniciar
        ctk.CTkButton(
            col_izq,
            text="REINICIAR",
            command=self.reiniciar,
            fg_color=COLORES["boton_reiniciar"],
            hover_color=COLORES["boton_reiniciar_hover"],
            height=35,
            font=("Arial Bold", 12),
            corner_radius=8
        ).pack(fill="x", pady=2)
        
        # Botón Limpiar Gráfica
        ctk.CTkButton(
            col_izq,
            text="LIMPIAR",
            command=self.limpiar_grafica,
            fg_color="#95A5A6",
            hover_color="#7F8C8D",
            height=35,
            font=("Arial Bold", 12),
            corner_radius=8
        ).pack(fill="x", pady=2)
        
        # Columna derecha - Botones de exportación
        col_der = ctk.CTkFrame(botones_secundarios_frame, fg_color="transparent")
        col_der.pack(side="right", fill="both", expand=True, padx=2)
        
        # Botón Guardar Imagen
        ctk.CTkButton(
            col_der,
            text="GUARDAR IMAGEN",
            command=self.guardar_imagen,
            fg_color="#3498DB",
            hover_color="#2980B9",
            height=35,
            font=("Arial Bold", 12),
            corner_radius=8
        ).pack(fill="x", pady=2)
        
        # Botón Guardar PDF
        ctk.CTkButton(
            col_der,
            text="GUARDAR PDF",
            command=self.guardar_pdf,
            fg_color="#9B59B6",
            hover_color="#8E44AD",
            height=35,
            font=("Arial Bold", 12),
            corner_radius=8
        ).pack(fill="x", pady=2)
        
        # Botón Cerrar
        ctk.CTkButton(
            botones_frame,
            text="CERRAR APLICACIÓN",
            command=self.cerrar_app,
            fg_color=COLORES["boton_cerrar"],
            hover_color=COLORES["boton_cerrar_hover"],
            height=40,
            font=("Arial Bold", 13),
            corner_radius=10
        ).pack(fill="x", pady=(10, 15), padx=10)
        
    def _crear_panel_derecho(self):
        """Crea el panel derecho con gráficas"""
        self.right_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=COLORES["fondo_frame"],
            corner_radius=10
        )
        self.right_frame.pack(side="right", fill="both", expand=True, padx=(5, 0), pady=5)
        
    def _configurar_graficas(self):
        """Configura los elementos gráficos"""
        # Título
        title_frame = ctk.CTkFrame(self.right_frame, fg_color="#1A1A2E", corner_radius=10)
        title_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            title_frame,
            text="Curva de Decaimiento Radiactivo",
            font=("Arial Bold", 20),
            text_color="#00D9FF"
        ).pack(pady=15)
        
        # Configuración de la gráfica
        self.fig, self.ax = plt.subplots(
            facecolor=COLORES["fondo_grafica"],
            figsize=(10, 6)
        )
        self.ax.set_facecolor(COLORES["fondo_grafica"])
        self.ax.set_xlabel("Tiempo (horas)", color='white', fontsize=12, fontweight='bold')
        self.ax.set_ylabel("Actividad (MBq)", color='white', fontsize=12, fontweight='bold')
        self.ax.set_title("Decaimiento en Tiempo Real", color='white', fontsize=14, fontweight='bold')
        self.ax.tick_params(colors='white', labelsize=10)
        self.ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.3)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        
        # Conectar evento de clic
        self.canvas.mpl_connect('button_press_event', self._on_click_grafica)
        
        # Panel de información del punto seleccionado
        self.punto_info_frame = ctk.CTkFrame(
            self.right_frame,
            fg_color="#1A1A2E",
            corner_radius=10,
            height=120
        )
        self.punto_info_frame.pack(fill="x", padx=10, pady=(0, 10))
        self.punto_info_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            self.punto_info_frame,
            text="Información del Punto Seleccionado",
            font=("Arial Bold", 13),
            text_color="#00D9FF"
        ).pack(pady=(10, 5))
        
        self.punto_info_label = ctk.CTkLabel(
            self.punto_info_frame,
            text="Haga clic en la gráfica para ver detalles de un punto específico",
            font=("Arial", 11),
            text_color="#AAAAAA",
            wraplength=900
        )
        self.punto_info_label.pack(pady=5, padx=20)
        
        # Frame de información adicional
        info_bottom_frame = ctk.CTkFrame(
            self.right_frame,
            fg_color=COLORES["fondo_input"],
            corner_radius=10
        )
        info_bottom_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Grid para información
        info_grid = ctk.CTkFrame(info_bottom_frame, fg_color="transparent")
        info_grid.pack(fill="x", padx=20, pady=10)
        
        # Columna 1: Vida media
        col1 = ctk.CTkFrame(info_grid, fg_color="transparent")
        col1.pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(col1, text="Vida Media:", font=("Arial Bold", 11), text_color="#AAAAAA").pack(anchor="w")
        self.vida_media_label = ctk.CTkLabel(
            col1,
            text="- horas",
            font=("Arial Bold", 13),
            text_color="white"
        )
        self.vida_media_label.pack(anchor="w")
        
        # Columna 2: Fecha
        col2 = ctk.CTkFrame(info_grid, fg_color="transparent")
        col2.pack(side="left", fill="x", expand=True)
        
        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        ctk.CTkLabel(col2, text="Fecha de Simulación:", font=("Arial Bold", 11), text_color="#AAAAAA").pack(anchor="w")
        self.fecha_label = ctk.CTkLabel(
            col2,
            text=fecha_actual,
            font=("Arial Bold", 13),
            text_color="white"
        )
        self.fecha_label.pack(anchor="w")
        
        # Columna 3: Aplicación
        col3 = ctk.CTkFrame(info_grid, fg_color="transparent")
        col3.pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(col3, text="Aplicación:", font=("Arial Bold", 11), text_color="#AAAAAA").pack(anchor="w")
        self.aplicacion_label = ctk.CTkLabel(
            col3,
            text="-",
            font=("Arial Bold", 13),
            text_color="white"
        )
        self.aplicacion_label.pack(anchor="w")
    
    def _on_click_grafica(self, event):
        """Maneja el clic en la gráfica para mostrar información del punto"""
        if event.inaxes != self.ax or len(self.tiempos) == 0:
            return
        
        # Encontrar el punto más cercano al clic
        click_x = event.xdata
        distancias = [abs(t - click_x) for t in self.tiempos]
        idx_cercano = distancias.index(min(distancias))
        
        # Obtener datos del punto
        tiempo_punto = self.tiempos[idx_cercano]
        actividad_punto = self.actividades[idx_cercano]
        gamma_punto = self.gammas[idx_cercano] if idx_cercano < len(self.gammas) else 1.0
        porcentaje_punto = (actividad_punto / self.actividad_inicial) * 100
        decaimiento_punto = 100 - porcentaje_punto
        
        # Actualizar el panel de información
        info_texto = (
            f"Tiempo: {tiempo_punto:.4f} horas  |  "
            f"Actividad: {actividad_punto:.4f} MBq  |  "
            f"Restante: {porcentaje_punto:.2f}%  |  "
            f"% Decaído: {decaimiento_punto:.2f}%  |  "
            f"Gamma (γ): {gamma_punto:.4f}"
        )
        
        self.punto_info_label.configure(
            text=info_texto,
            text_color="white"
        )
        
        # Marcar el punto en la gráfica
        if self.punto_marcado is not None:
            self.punto_marcado.remove()
        
        self.punto_marcado = self.ax.plot(
            tiempo_punto, 
            actividad_punto, 
            'o', 
            color='#FFD700', 
            markersize=12, 
            markeredgecolor='white',
            markeredgewidth=2,
            zorder=5
        )[0]
        
        self.canvas.draw()
        
    def _calcular_gamma(self, actividad_actual):
        """Calcula el valor de gamma (0 a 1)"""
        if self.actividad_inicial == 0:
            return 0
        gamma = actividad_actual / self.actividad_inicial
        return max(0.0, min(1.0, gamma))
        
    def _actualizar_color_gamma(self, gamma):
        """Actualiza el color del valor de gamma según su intensidad"""
        # Interpolar entre rojo (baja actividad) y verde (alta actividad)
        r = int(255 * (1 - gamma))
        g = int(255 * gamma)
        b = 80
        color = f"#{r:02x}{g:02x}{b:02x}"
        return color
        
    def _actualizar_estado_botones(self):
        """Actualiza el estado de los botones según la simulación"""
        if self.simulacion_activa and not self.simulacion_pausada:
            self.btn_iniciar.configure(state="disabled")
            self.btn_pausar.configure(state="normal", text="⏸️ PAUSAR")
            self.btn_detener.configure(state="normal")
        elif self.simulacion_pausada:
            self.btn_iniciar.configure(state="disabled")
            self.btn_pausar.configure(state="normal", text="▶️ REANUDAR")
            self.btn_detener.configure(state="normal")
        else:
            self.btn_iniciar.configure(state="normal")
            self.btn_pausar.configure(state="disabled", text="⏸️ PAUSAR")
            self.btn_detener.configure(state="disabled")
        
    def pausar_simulacion(self):
        """Pausa o reanuda la simulación"""
        if self.simulacion_activa and not self.simulacion_pausada:
            self.simulacion_pausada = True
        else:
            self.simulacion_pausada = False
            if self.simulacion_activa:
                self.actualizar_grafica()
        
        self._actualizar_estado_botones()

    def detener_simulacion(self):
        """Detiene completamente la simulación"""
        self.simulacion_activa = False
        self.simulacion_pausada = False
        self._actualizar_estado_botones()

    def limpiar_grafica(self):
        """Limpia la gráfica manteniendo los parámetros"""
        self.simulacion_activa = False
        self.simulacion_pausada = False
        
        # Limpiar datos de la gráfica
        self.tiempos = []
        self.actividades = []
        self.gammas = []
        self.punto_marcado = None
        
        # Limpiar gráfica
        self.ax.clear()
        self.ax.set_facecolor(COLORES["fondo_grafica"])
        self.ax.set_xlabel("Tiempo (horas)", color='white', fontsize=12, fontweight='bold')
        self.ax.set_ylabel("Actividad (MBq)", color='white', fontsize=12, fontweight='bold')
        self.ax.set_title("Decaimiento en Tiempo Real", color='white', fontsize=14, fontweight='bold')
        self.ax.tick_params(colors='white', labelsize=10)
        self.ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.3)
        self.canvas.draw()
        
        # Reiniciar etiquetas de información
        self.tiempo_label.configure(text="0.0000 h")
        self.actividad_label.configure(text="0.0000 MBq")
        self.porcentaje_label.configure(text="100.00%")
        self.gamma_valor_label.configure(text="1.0000", text_color="#00FF88")
        self.gamma_progress.set(1.0)
        
        # Reiniciar punto info
        self.punto_info_label.configure(
            text="Haga clic en la gráfica para ver detalles de un punto específico",
            text_color="#AAAAAA"
        )
        
        self._actualizar_estado_botones()

    def guardar_imagen(self):
        """Guarda la gráfica como imagen PNG"""
        if not self.tiempos:
            self._mostrar_error("No hay datos para guardar. Ejecute una simulación primero.")
            return
            
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")],
                title="Guardar gráfica como imagen"
            )
            
            if file_path:
                # Guardar la figura actual
                self.fig.savefig(file_path, dpi=300, bbox_inches='tight', facecolor=COLORES["fondo_grafica"])
                
                self._mostrar_mensaje("Éxito", f"Gráfica guardada correctamente en:\n{file_path}")
                
        except Exception as e:
            self._mostrar_error(f"Error al guardar imagen: {str(e)}")

    def guardar_pdf(self):
        """Guarda la gráfica como PDF"""
        if not self.tiempos:
            self._mostrar_error("No hay datos para guardar. Ejecute una simulación primero.")
            return
            
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
                title="Guardar gráfica como PDF"
            )
            
            if file_path:
                # Guardar la figura actual como PDF
                self.fig.savefig(file_path, bbox_inches='tight', facecolor=COLORES["fondo_grafica"])
                
                self._mostrar_mensaje("Éxito", f"Gráfica guardada correctamente en:\n{file_path}")
                
        except Exception as e:
            self._mostrar_error(f"Error al guardar PDF: {str(e)}")

    def actualizar_grafica(self):
        """Actualiza la gráfica con los nuevos datos"""
        if not self.simulacion_activa or self.simulacion_pausada:
            return
            
        # Calcular tiempo transcurrido
        tiempo_real_segundos = time.time() - self.start_time
        tiempo_real_minutos = tiempo_real_segundos / 60
        tiempo_escalado = (tiempo_real_minutos / self.tiempo_simulacion_real) * self.tiempo_simulacion
        
        # Calcular actividad actual
        actividad_actual = calcular_actividad_restante(
            self.actividad_inicial,
            tiempo_escalado,
            self.vida_media
        )
        
        # Calcular gamma
        gamma_actual = self._calcular_gamma(actividad_actual)
        
        # Agregar datos
        self.tiempos.append(tiempo_escalado)
        self.actividades.append(actividad_actual)
        self.gammas.append(gamma_actual)
        
        # Actualizar gráfica
        self.ax.clear()
        self.ax.set_facecolor(COLORES["fondo_grafica"])
        self.ax.plot(
            self.tiempos,
            self.actividades,
            marker='o',
            color=self.color,
            linewidth=3,
            markersize=5,
            markeredgecolor='white',
            markeredgewidth=0.5,
            label=f"Decaimiento de {self.combo_radiofarmaco.get()}",
            alpha=0.9
        )
        
        # Agregar línea de actividad final si es modo actividad
        if self.modo_simulacion == "actividad" and self.actividad_final > 0:
            self.ax.axhline(
                y=self.actividad_final,
                color='#FF4444',
                linestyle='--',
                linewidth=2,
                label=f'Objetivo: {self.actividad_final} MBq',
                alpha=0.7
            )
        
        self.ax.set_xlabel("Tiempo (horas)", color='white', fontsize=12, fontweight='bold')
        self.ax.set_ylabel("Actividad (MBq)", color='white', fontsize=12, fontweight='bold')
        self.ax.set_title("Decaimiento en Tiempo Real", color='white', fontsize=14, fontweight='bold')
        self.ax.tick_params(colors='white', labelsize=10)
        self.ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.3)
        self.ax.legend(
            facecolor=COLORES["fondo_grafica"], 
            edgecolor='white', 
            labelcolor='white',
            fontsize=10,
            loc='upper right'
        )
        
        # Añadir anotación de gamma en la gráfica
        if len(self.tiempos) > 1:
            self.ax.text(
                0.02, 0.98, 
                f'γ = {gamma_actual:.4f}',
                transform=self.ax.transAxes,
                fontsize=12,
                verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor=self._actualizar_color_gamma(gamma_actual), alpha=0.8),
                color='white',
                fontweight='bold'
            )
        
        self.canvas.draw()
        
        # Actualizar etiquetas de información en tiempo real
        porcentaje_restante = (actividad_actual / self.actividad_inicial) * 100
        
        self.tiempo_label.configure(text=f"{tiempo_escalado:.4f} h")
        self.actividad_label.configure(text=f"{actividad_actual:.4f} MBq")
        self.porcentaje_label.configure(text=f"{porcentaje_restante:.2f}%")
        
        # Actualizar gamma
        color_gamma = self._actualizar_color_gamma(gamma_actual)
        self.gamma_valor_label.configure(text=f"{gamma_actual:.4f}", text_color=color_gamma)
        self.gamma_progress.set(gamma_actual)
        
        # Continuar si no se alcanzó el tiempo límite
        if tiempo_escalado < self.tiempo_simulacion and self.simulacion_activa and not self.simulacion_pausada:
            self.root.after(100, self.actualizar_grafica)
        elif tiempo_escalado >= self.tiempo_simulacion:
            self.simulacion_activa = False
            self.simulacion_pausada = False
            self._actualizar_estado_botones()
            self._mostrar_mensaje(
                "Simulación Completada", 
                f"La simulación de {self.tiempo_simulacion:.2f} horas ha finalizado.\n\n"
                f"Actividad final: {actividad_actual:.4f} MBq\n"
                f"Gamma final: {gamma_actual:.4f}\n"
                f"Decaimiento total: {100 - porcentaje_restante:.2f}%"
            )
            
    def iniciar_simulacion(self):
        """Inicia la simulación con los parámetros ingresados"""
        try:
            # Obtener parámetros
            radiofarmaco = self.combo_radiofarmaco.get()
            self.vida_media = self.radiofarmacos[radiofarmaco]["vida_media"]
            self.color = self.radiofarmacos[radiofarmaco]["color"]
            aplicacion = self.radiofarmacos[radiofarmaco]["aplicacion"]
            
            self.actividad_inicial = float(self.entry_actividad.get())
            self.tiempo_simulacion = float(self.entry_tiempo_simulacion.get())
            self.tiempo_simulacion_real = float(self.entry_tiempo_real.get())
            
            if self.modo_simulacion == "actividad":
                self.actividad_final = float(self.entry_actividad_final.get())
                if self.actividad_final >= self.actividad_inicial:
                    self._mostrar_error("La actividad final debe ser menor que la actividad inicial")
                    return
            else:
                self.actividad_final = 0
            
            # Validar datos
            if self.actividad_inicial <= 0:
                self._mostrar_error("La actividad inicial debe ser mayor que cero")
                return
                
            if self.tiempo_simulacion <= 0 or self.tiempo_simulacion_real <= 0:
                self._mostrar_error("Los tiempos deben ser mayores que cero")
                return
            
            # Actualizar información
            self.vida_media_label.configure(text=f"{self.vida_media} horas")
            self.aplicacion_label.configure(text=aplicacion)
            fecha_inicio = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            self.fecha_label.configure(text=fecha_inicio)
            
            # Inicializar datos
            self.start_time = time.time()
            self.tiempos = [0]
            self.actividades = [self.actividad_inicial]
            self.gammas = [1.0]
            self.simulacion_activa = True
            self.simulacion_pausada = False
            
            # Actualizar estado de botones
            self._actualizar_estado_botones()
            
            # Resetear información del punto
            self.punto_info_label.configure(
                text="Haga clic en la gráfica para ver detalles de un punto específico",
                text_color="#AAAAAA"
            )
            
            # Inicializar valores de información
            self.tiempo_label.configure(text="0.0000 h")
            self.actividad_label.configure(text=f"{self.actividad_inicial:.4f} MBq")
            self.porcentaje_label.configure(text="100.00%")
            self.gamma_valor_label.configure(text="1.0000", text_color="#00FF88")
            self.gamma_progress.set(1.0)
            
            # Iniciar actualización
            self.actualizar_grafica()
            
        except ValueError:
            self._mostrar_error("Por favor ingrese valores numéricos válidos")
        except Exception as e:
            self._mostrar_error(f"Error al iniciar simulación: {str(e)}")
            
    def reiniciar(self):
        """Reinicia la simulación y limpia la interfaz"""
        self.simulacion_activa = False
        self.simulacion_pausada = False
        
        # Limpiar entradas
        self.entry_actividad.delete(0, "end")
        self.entry_actividad.insert(0, "100")
        
        self.entry_actividad_final.delete(0, "end")
        self.entry_actividad_final.insert(0, "50")
        
        self.entry_tiempo_simulacion.delete(0, "end")
        self.entry_tiempo_simulacion.insert(0, "5")
        
        self.entry_tiempo_real.delete(0, "end")
        self.entry_tiempo_real.insert(0, "1")
        
        # Reiniciar etiquetas
        self.tiempo_label.configure(text="0.0000 h")
        self.actividad_label.configure(text="0.0000 MBq")
        self.porcentaje_label.configure(text="100.00%")
        self.vida_media_label.configure(text="- horas")
        self.aplicacion_label.configure(text="-")
        
        # Reiniciar gamma
        self.gamma_valor_label.configure(text="1.0000", text_color="#00FF88")
        self.gamma_progress.set(1.0)
        
        # Reiniciar punto info
        self.punto_info_label.configure(
            text="Haga clic en la gráfica para ver detalles de un punto específico",
            text_color="#AAAAAA"
        )
        
        # Limpiar gráfica
        self.ax.clear()
        self.ax.set_facecolor(COLORES["fondo_grafica"])
        self.ax.set_xlabel("Tiempo (horas)", color='white', fontsize=12, fontweight='bold')
        self.ax.set_ylabel("Actividad (MBq)", color='white', fontsize=12, fontweight='bold')
        self.ax.set_title("Decaimiento en Tiempo Real", color='white', fontsize=14, fontweight='bold')
        self.ax.tick_params(colors='white', labelsize=10)
        self.ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.3)
        self.canvas.draw()
        
        # Reiniciar variables
        self.tiempos = []
        self.actividades = []
        self.gammas = []
        self.punto_marcado = None
        
        # Actualizar estado de botones
        self._actualizar_estado_botones()
        
        # Actualizar fórmula
        self._actualizar_formula()
        
    def cerrar_app(self):
        """Cierra la aplicación"""
        self.root.quit()
        self.root.destroy()
        
    def _mostrar_error(self, mensaje):
        """Muestra un mensaje de error profesional"""
        ventana = ctk.CTkToplevel(self.root)
        ventana.title("Error")
        ventana.geometry("400x200")
        ventana.configure(fg_color=COLORES["fondo_frame"])
        
        # Centrar ventana
        ventana.transient(self.root)
        ventana.grab_set()
        
        error_frame = ctk.CTkFrame(ventana, fg_color="#C0392B", corner_radius=10)
        error_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        ctk.CTkLabel(
            error_frame,
            text="⚠️ Error",
            font=("Arial Black", 18),
            text_color="white"
        ).pack(pady=(20, 10))
        
        ctk.CTkLabel(
            error_frame,
            text=mensaje,
            font=("Arial", 12),
            wraplength=340,
            text_color="white"
        ).pack(pady=10, padx=20)
        
        ctk.CTkButton(
            error_frame,
            text="Aceptar",
            command=ventana.destroy,
            fg_color="#E74C3C",
            hover_color="#922B21",
            height=35,
            font=("Arial Bold", 12)
        ).pack(pady=(10, 20))
        
    def _mostrar_mensaje(self, titulo, mensaje):
        """Muestra un mensaje informativo profesional"""
        ventana = ctk.CTkToplevel(self.root)
        ventana.title(titulo)
        ventana.geometry("450x250")
        ventana.configure(fg_color=COLORES["fondo_frame"])
        
        # Centrar ventana
        ventana.transient(self.root)
        ventana.grab_set()
        
        info_frame = ctk.CTkFrame(ventana, fg_color="#27AE60", corner_radius=10)
        info_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        ctk.CTkLabel(
            info_frame,
            text=f"✓ {titulo}",
            font=("Arial Black", 18),
            text_color="white"
        ).pack(pady=(20, 10))
        
        ctk.CTkLabel(
            info_frame,
            text=mensaje,
            font=("Arial", 12),
            wraplength=390,
            text_color="white",
            justify="left"
        ).pack(pady=10, padx=20)
        
        ctk.CTkButton(
            info_frame,
            text="Aceptar",
            command=ventana.destroy,
            fg_color="#2ECC71",
            hover_color="#229954",
            height=35,
            font=("Arial Bold", 12)
        ).pack(pady=(10, 20))


# Ejecución independiente para pruebas
if __name__ == "__main__":
    from config.constantes import RADIOFARMACOS, ESCALAS_TIEMPO
    from modelos.simulacion import SimuladorDecaimiento
    
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    root = ctk.CTk()
    simulador = SimuladorDecaimiento()
    app = SimuladorGUI(root, RADIOFARMACOS, ESCALAS_TIEMPO, simulador)
    root.mainloop()