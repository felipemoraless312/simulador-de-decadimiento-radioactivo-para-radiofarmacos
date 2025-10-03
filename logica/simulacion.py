import math
import time
import random

def calcular_actividad_restante(actividad_inicial, tiempo, vida_media):
    """
    Calcula la actividad restante de un radiofármaco después de un tiempo determinado.
    
    Args:
        actividad_inicial (float): Actividad inicial en MBq
        tiempo (float): Tiempo transcurrido en horas
        vida_media (float): Vida media del radiofármaco en horas
        
    Returns:
        float: Actividad restante en MBq
    """
    lambda_ = math.log(2) / vida_media
    return actividad_inicial * math.exp(-lambda_ * tiempo)

class SimuladorDecaimiento:
    def __init__(self):
        self.actividad_inicial = 0
        self.vida_media = 0
        self.actividad_deseada = 0
        self.start_time = 0
        self.escala_tiempo = 0
        self.color = "#FFFFFF"
        self.tiempos = []
        self.actividades = []
        
    def iniciar_simulacion(self, actividad_inicial, vida_media, actividad_deseada, escala_tiempo, color):
        """
        Inicia la simulación de decaimiento radiactivo.
        
        Args:
            actividad_inicial (float): Actividad inicial en MBq
            vida_media (float): Vida media del radiofármaco en horas
            actividad_deseada (float): Actividad objetivo en MBq
            escala_tiempo (int): Factor de escala de tiempo (horas simuladas por minuto real)
            color (str): Color para la representación gráfica
        """
        self.actividad_inicial = actividad_inicial
        self.vida_media = vida_media
        self.actividad_deseada = actividad_deseada
        self.escala_tiempo = escala_tiempo
        self.color = color
        self.start_time = time.time()
        self.tiempos = [0]
        self.actividades = [actividad_inicial]
        
    def actualizar_calculos(self):
        """
        Actualiza los cálculos de la simulación basados en el tiempo transcurrido.
        
        Returns:
            float: Actividad actual
            float: Tiempo escalado transcurrido
        """
        tiempo_real = (time.time() - self.start_time) / 60
        tiempo_escalado = tiempo_real * (self.escala_tiempo / 1)
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
        
    def generar_particulas_random(self, n_particles):
        """
        Genera posiciones aleatorias para partículas en animación.
        
        Args:
            n_particles (int): Número de partículas a generar
            
        Returns:
            list: Lista de tuplas (x, y, símbolo) para cada partícula
        """
        # Símbolos de radiación y partículas
        simbolos = ['☢', '⚛', '☢', '⚛']
        particulas = []
        
        for _ in range(n_particles // 2):
            x, y = random.randint(10, 290), random.randint(10, 290)
            simbolo = random.choice(simbolos)
            particulas.append((x, y, simbolo))
            
        return particulas