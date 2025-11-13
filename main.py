"""
Simulador de Decaimiento Radiactivo
====================================
Aplicación para visualizar el decaimiento de radiofármacos en tiempo real.

    @Autor: [Felipe Morales]
        Web: [https://github.com/felipemoraless312/simulador-de-decadimiento-radioactivo-para-radiofarmacos]
        Fecha: [28-10-2025]
"""

import customtkinter as ctk
from config.constantes import RADIOFARMACOS, ESCALAS_TIEMPO
from modelos.simulacion import SimuladorDecaimiento
from interfaz.gui_principal import SimuladorGUI

if __name__ == "__main__":
    
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    root = ctk.CTk()
    simulador = SimuladorDecaimiento()
    app = SimuladorGUI(root, RADIOFARMACOS, ESCALAS_TIEMPO, simulador)
    root.mainloop()
