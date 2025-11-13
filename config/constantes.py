"""Constantes y configuración global del simulador"""

# Radiofármacos disponibles
RADIOFARMACOS = {
    "Fluor-18": {
        "vida_media": 1.83,
        "color": "#8E44AD",
        "aplicacion": "PET (Tomografía por Emisión de Positrones)",
        "descripcion": "Usado en diagnóstico de cáncer"
    },
    "Tecnecio-99m": {
        "vida_media": 6.01,
        "color": "#3498DB",
        "aplicacion": "Gammagrafía",
        "descripcion": "Diagnóstico de enfermedades cardíacas"
    },
    "Yodo-131": {
        "vida_media": 192.5,
        "color": "#2ECC71",
        "aplicacion": "Tratamiento de tiroides",
        "descripcion": "Terapia de cáncer de tiroides"
    },
    "Carbono-11": {
        "vida_media": 0.33,
        "color": "#E74C3C",
        "aplicacion": "Investigación metabólica",
        "descripcion": "Estudios de metabolismo cerebral"
    },
    "Nitrógeno-13": {
        "vida_media": 0.17,
        "color": "#F39C12",
        "aplicacion": "Medicina nuclear",
        "descripcion": "Estudios cardiovasculares"
    }
}

# Escalas de tiempo disponibles
ESCALAS_TIEMPO = {
    "5 horas": 5,
    "10 horas": 10,
    "15 horas": 15,
    "20 horas": 20
}

# Colores de la interfaz
COLORES = {
    "fondo_principal": "#1B2631",
    "fondo_frame": "#2C3E50",
    "fondo_grafica": "#212F3D",
    "fondo_input": "#34495E",
    "boton_iniciar": "#2ECC71",
    "boton_iniciar_hover": "#27AE60",
    "boton_reiniciar": "#F39C12",
    "boton_reiniciar_hover": "#D35400",
    "boton_cerrar": "#E74C3C",
    "boton_cerrar_hover": "#C0392B",
    "boton_parcial": "#9B59B6",
    "boton_parcial_hover": "#8E44AD"
}

# Configuración de ventanas
VENTANA_PRINCIPAL = {
    "ancho": 1024,
    "alto": 600,
    "titulo": "Simulador de Decaimiento Radiactivo"
}

VENTANA_PARCIAL = {
    "ancho": 1024,
    "alto": 600,
    "titulo": "Simulador de Decaimiento Parcial"
}
