import customtkinter as ctk
from modelos.radiofarmaco import radiofarmacos, escala_tiempo_dict
from logica.simulacion import SimuladorDecaimiento
from interfaz.gui import SimuladorGUI

def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")    
    root = ctk.CTk()

    simulador = SimuladorDecaimiento()
    
    # Crear la interfaz gráfica
    app = SimuladorGUI(root, radiofarmacos, escala_tiempo_dict, simulador)
    
    # Iniciar bucle principal
    root.mainloop()

if __name__ == "__main__":
    main()
