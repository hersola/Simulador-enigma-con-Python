from tkinter import *
from tkinter import ttk

class mainApp(Tk):
    size = "640x480"
    titulo = "Simulación máquina Enigma - KeepCoding"

    def __init__(self):
        Tk.__init__(self,)
        self.geometry(self.size)
        self.title(self.titulo)
        self.resizable(0,0)
        self.textoPlano = StringVar(value="")
        self.textoEncriptado = StringVar(value="")
        self.posicion = ""
        self.contenidoVentana()

    def contenidoVentana(self):
        self.labelEntrada = ttk.Label(self,text="Texto a codificar:").place(x=10,y=10)
        self.entrada = ttk.Entry(self,textvariable = self.textoPlano)
        self.entrada.place(x=10, y=30, width=620, height=100)

    def start(self):
        self.mainloop()
    
    def stop(self):
        self.destroy()
        
if __name__ == "__main__":
    app = mainApp()
    app.start()
    app.stop()
