"""
Funciones matemáticas para cálculos de decaimiento radiactivo
Versión mejorada con funciones adicionales
"""

import math

def calcular_actividad_restante(actividad_inicial, tiempo, vida_media):
    """
    Calcula la actividad restante usando la ley de decaimiento exponencial.
    
    Fórmula: A(t) = A₀ * e^(-λt)
    donde λ = ln(2) / t½
    
    Args:
        actividad_inicial (float): Actividad inicial en MBq
        tiempo (float): Tiempo transcurrido en horas
        vida_media (float): Vida media del radiofármaco en horas
        
    Returns:
        float: Actividad restante en MBq
    """
    if vida_media <= 0:
        raise ValueError("La vida media debe ser mayor que cero")
    
    constante_decaimiento = math.log(2) / vida_media
    actividad_restante = actividad_inicial * math.exp(-constante_decaimiento * tiempo)
    
    return actividad_restante

def calcular_tiempo_para_actividad(actividad_inicial, actividad_final, vida_media):
    """
    Calcula el tiempo necesario para alcanzar una actividad específica.
    
    Fórmula: t = -ln(Af / A₀) / λ
    donde λ = ln(2) / t½
    
    Args:
        actividad_inicial (float): Actividad inicial en MBq
        actividad_final (float): Actividad deseada en MBq
        vida_media (float): Vida media del radiofármaco en horas
        
    Returns:
        float: Tiempo necesario en horas
    """
    if actividad_final >= actividad_inicial:
        return 0
    
    if actividad_final <= 0:
        raise ValueError("La actividad final debe ser mayor que cero")
    
    constante_decaimiento = math.log(2) / vida_media
    tiempo = -math.log(actividad_final / actividad_inicial) / constante_decaimiento
    
    return tiempo

def calcular_porcentaje_restante(actividad_actual, actividad_inicial):
    """
    Calcula el porcentaje de actividad restante.
    
    Args:
        actividad_actual (float): Actividad actual en MBq
        actividad_inicial (float): Actividad inicial en MBq
        
    Returns:
        float: Porcentaje restante (0-100)
    """
    if actividad_inicial == 0:
        return 0
    return (actividad_actual / actividad_inicial) * 100

def calcular_constante_decaimiento(vida_media):
    """
    Calcula la constante de decaimiento (λ).
    
    Fórmula: λ = ln(2) / t½
    
    Args:
        vida_media (float): Vida media del radiofármaco en horas
        
    Returns:
        float: Constante de decaimiento en h⁻¹
    """
    if vida_media <= 0:
        raise ValueError("La vida media debe ser mayor que cero")
    
    return math.log(2) / vida_media

def calcular_gamma(actividad_actual, actividad_inicial):
    """
    Calcula el factor gamma (γ) de intensidad relativa.
    
    Gamma representa la fracción de actividad restante, variando de 1.0 (100%)
    cuando la actividad es máxima, hasta 0.0 cuando la actividad es mínima.
    
    Fórmula: γ = A(t) / A₀
    
    Args:
        actividad_actual (float): Actividad actual en MBq
        actividad_inicial (float): Actividad inicial en MBq
        
    Returns:
        float: Factor gamma entre 0 y 1
    """
    if actividad_inicial == 0:
        return 0
    
    gamma = actividad_actual / actividad_inicial
    return max(0.0, min(1.0, gamma))

def calcular_numero_vidas_medias(tiempo, vida_media):
    """
    Calcula cuántas vidas medias han transcurrido.
    
    Args:
        tiempo (float): Tiempo transcurrido en horas
        vida_media (float): Vida media del radiofármaco en horas
        
    Returns:
        float: Número de vidas medias transcurridas
    """
    if vida_media <= 0:
        raise ValueError("La vida media debe ser mayor que cero")
    
    return tiempo / vida_media

def calcular_actividad_en_vidas_medias(actividad_inicial, num_vidas_medias):
    """
    Calcula la actividad después de un número específico de vidas medias.
    
    Fórmula: A = A₀ * (1/2)^n
    donde n es el número de vidas medias
    
    Args:
        actividad_inicial (float): Actividad inicial en MBq
        num_vidas_medias (float): Número de vidas medias transcurridas
        
    Returns:
        float: Actividad restante en MBq
    """
    return actividad_inicial * math.pow(0.5, num_vidas_medias)

def obtener_formula_sustituida(modo, actividad_inicial, actividad_final, 
                               tiempo_simulacion, vida_media):
    """
    Genera la fórmula con valores sustituidos según el modo de simulación.
    
    Args:
        modo (str): "tiempo" o "actividad"
        actividad_inicial (float): Actividad inicial en MBq
        actividad_final (float): Actividad final en MBq
        tiempo_simulacion (float): Tiempo de simulación en horas
        vida_media (float): Vida media en horas
        
    Returns:
        dict: Diccionario con fórmula general, sustitución, resultado y lambda
    """
    lambda_val = calcular_constante_decaimiento(vida_media)
    
    if modo == "tiempo":
        At = calcular_actividad_restante(actividad_inicial, tiempo_simulacion, vida_media)
        return {
            "formula": "A(t) = A₀ · e^(-λt)",
            "sustitucion": f"A({tiempo_simulacion:.2f}) = {actividad_inicial:.2f} · e^(-{lambda_val:.6f} × {tiempo_simulacion:.2f})",
            "resultado": f"A({tiempo_simulacion:.2f}) = {At:.4f} MBq",
            "lambda": lambda_val
        }
    else:  # modo actividad
        t = calcular_tiempo_para_actividad(actividad_inicial, actividad_final, vida_media)
        return {
            "formula": "t = -ln(Af / A₀) / λ",
            "sustitucion": f"t = -ln({actividad_final:.2f} / {actividad_inicial:.2f}) / {lambda_val:.6f}",
            "resultado": f"t = {t:.4f} horas",
            "lambda": lambda_val
        }
