"""Modelo de datos para radiofármacos"""

from dataclasses import dataclass

@dataclass
class Radiofarmaco:
    """Clase que representa un radiofármaco"""
    nombre: str
    vida_media: float
    color: str
    aplicacion: str
    descripcion: str
    
    def __str__(self):
        return f"{self.nombre} (t½ = {self.vida_media}h)"
    
    @classmethod
    def desde_dict(cls, nombre: str, datos: dict):
        """Crea un Radiofármaco desde un diccionario"""
        return cls(
            nombre=nombre,
            vida_media=datos["vida_media"],
            color=datos["color"],
            aplicacion=datos["aplicacion"],
            descripcion=datos["descripcion"]
        )
