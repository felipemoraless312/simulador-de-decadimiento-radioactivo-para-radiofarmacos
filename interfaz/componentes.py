"""Componentes comunes reutilizables para la interfaz"""

import customtkinter as ctk

class FrameParametros(ctk.CTkFrame):
    """Frame reutilizable para parámetros de entrada"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.campos = {}
        
    def agregar_campo(self, etiqueta, tipo="entry", valores=None, valor_default=""):
        """
        Agrega un campo de entrada al frame.
        
        Args:
            etiqueta (str): Etiqueta del campo
            tipo (str): 'entry' o 'combobox'
            valores (list): Valores para combobox
            valor_default (str): Valor por defecto
        """
        ctk.CTkLabel(self, text=etiqueta).pack(anchor="w", padx=20, pady=(10,0))
        
        if tipo == "entry":
            campo = ctk.CTkEntry(
                self,
                width=250,
                fg_color="#34495E",
                text_color="white"
            )
            campo.insert(0, valor_default)
        elif tipo == "combobox":
            campo = ctk.CTkComboBox(
                self,
                values=valores or [],
                width=250,
                fg_color="#34495E",
                text_color="white"
            )
            if valor_default:
                campo.set(valor_default)
                
        campo.pack(pady=(0,10), padx=20)
        self.campos[etiqueta] = campo
        
        return campo
    
    def obtener_valor(self, etiqueta):
        """Obtiene el valor de un campo"""
        return self.campos[etiqueta].get()
    
    def limpiar_campo(self, etiqueta, valor_default=""):
        """Limpia un campo y establece un valor por defecto"""
        campo = self.campos[etiqueta]
        if isinstance(campo, ctk.CTkEntry):
            campo.delete(0, "end")
            campo.insert(0, valor_default)


class PanelGrafica(ctk.CTkFrame):
    """Panel reutilizable para mostrar gráficas"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.fig = None
        self.ax = None
        self.canvas = None
        
    def configurar_grafica(self, figura, ejes, canvas):
        """Configura la gráfica en el panel"""
        self.fig = figura
        self.ax = ejes
        self.canvas = canvas