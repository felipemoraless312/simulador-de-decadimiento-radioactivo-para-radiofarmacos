"""Lógica de simulación de decaimiento radiactivo"""

import time
import random
from utilidades.calculos import calcular_actividad_restante

class SimuladorDecaimiento:
    """Maneja la lógica de simulación de decaimiento radiactivo"""
    
    def __init__(self):
        self.actividad_inicial = 0
        self.vida_media = 0
        self.actividad_deseada = 0
        self.start_time = 0
        self.escala_tiempo = 0
        self.color = "#FFFFFF"
        self.tiempos = []
        self.actividades = []
        self.en_ejecucion = False
        
    def iniciar_simulacion(self, actividad_inicial, vida_media, 
                          actividad_deseada, escala_tiempo, color):
        """
        Inicia una nueva simulación.
        
        Args:
            actividad_inicial (float): Actividad inicial en MBq
            vida_media (float): Vida media en horas
            actividad_deseada (float): Actividad objetivo en MBq
            escala_tiempo (int): Horas simuladas por minuto real
            color (str): Color para visualización
        """
        self.actividad_inicial = actividad_inicial
        self.vida_media = vida_media
        self.actividad_deseada = actividad_deseada
        self.escala_tiempo = escala_tiempo
        self.color = color
        self.start_time = time.time()
        self.tiempos = [0]
        self.actividades = [actividad_inicial]
        self.en_ejecucion = True
        
    def actualizar_calculos(self):
        """
        Actualiza los cálculos basados en el tiempo transcurrido.
        
        Returns:
            tuple: (actividad_actual, tiempo_escalado)
        """
        tiempo_real_minutos = (time.time() - self.start_time) / 60
        tiempo_escalado = tiempo_real_minutos * self.escala_tiempo
        
        actividad_actual = calcular_actividad_restante(
            self.actividad_inicial,
            tiempo_escalado,
            self.vida_media
        )
        
        self.tiempos.append(tiempo_escalado)
        self.actividades.append(actividad_actual)
        
        return actividad_actual, tiempo_escalado
    
    def reiniciar(self):
        """Reinicia todos los datos de la simulación"""
        self.tiempos = []
        self.actividades = []
        self.start_time = 0
        self.en_ejecucion = False
        
    def generar_particulas_random(self, n_particles):
        """
        Genera posiciones aleatorias para animación de partículas.
        
        Args:
            n_particles (int): Número de partículas a generar
            
        Returns:
            list: Lista de tuplas (x, y, símbolo)
        """
        simbolos = ['☢', '⚛', '☢', '⚛']
        particulas = []
        
        for _ in range(max(1, n_particles // 2)):
            x = random.randint(10, 290)
            y = random.randint(10, 140)
            simbolo = random.choice(simbolos)
            particulas.append((x, y, simbolo))
            
        return particulas
    
    def obtener_estadisticas(self):
        """
        Obtiene estadísticas de la simulación actual.
        
        Returns:
            dict: Diccionario con estadísticas
        """
        if not self.actividades:
            return None
            
        return {
            "actividad_inicial": self.actividad_inicial,
            "actividad_actual": self.actividades[-1],
            "actividad_minima": min(self.actividades),
            "tiempo_transcurrido": self.tiempos[-1] if self.tiempos else 0,
            "porcentaje_restante": (self.actividades[-1] / self.actividad_inicial) * 100
        }
