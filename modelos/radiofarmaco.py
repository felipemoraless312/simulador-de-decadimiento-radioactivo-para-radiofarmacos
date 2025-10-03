# Diccionario con los radiofármacos y sus datos
radiofarmacos = {
    "Fluor-18": {
        "vida_media": 1.83, 
        "color": "#8E44AD",  # Morado
        "aplicacion": "PET (Tomografía por Emisión de Positrones)",
        "descripcion": "Usado en diagnóstico de cáncer"
    },
    "Tecnecio-99m": {
        "vida_media": 6.01, 
        "color": "#3498DB",  # Azul
        "aplicacion": "Gammagrafía",
        "descripcion": "Diagnóstico de enfermedades cardíacas"
    },
    "Yodo-131": {
        "vida_media": 192.5, 
        "color": "#2ECC71",  # Verde
        "aplicacion": "Tratamiento de tiroides",
        "descripcion": "Terapia de cáncer de tiroides"
    },
    "Carbono-11": {
        "vida_media": 0.33, 
        "color": "#E74C3C",  # Rojo
        "aplicacion": "Investigación metabólica",
        "descripcion": "Estudios de metabolismo cerebral"
    },
    "Nitrógeno-13": {
        "vida_media": 0.17, 
        "color": "#F39C12",  # Naranja
        "aplicacion": "Medicina nuclear",
        "descripcion": "Estudios cardiovasculares"
    }
}

# Escala de tiempo definida (horas simuladas por minuto real)
escala_tiempo_dict = {"5 horas": 5, "10 horas": 10, "15 horas": 15, "20 horas": 20}