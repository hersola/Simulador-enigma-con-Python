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
        self.posIni = StringVar(value="A")
        self.textoEncriptado = StringVar(value="")
        self.posicion = ""
        self.contenidoVentana()

    def contenidoVentana(self):
        ttk.Label(self,text="Texto a codificar:").place(x=10,y=10)
        ttk.Label(self,text="Configuración:",font=("",20)).place(x=375,y=20)
        ttk.Label(self,text="Un rotor + reflector",foreground="Blue",font=("",15)).place(x=400,y=55)
        ttk.Label(self,text="Posición inicio:",foreground="black",font=("",12)).place(x=400,y=82)
        ttk.Label(self,text="Posición actual:",foreground="black",font=("",12)).place(x=400,y=105)
        ttk.Label(self,text="Texto codificado:").place(x=10,y=205)
        self.entrada = Text(self, width = 40, height = 10).place(x=10,y=35)
        self.salida = Text(self, width = 40,height = 10).place(x=10,y=230)
        self.botonComprueba = Button(self, text="Comprobar",width = 10, height=2).place(x=10, y=405)
        self.botonCodifica = Button(self,text="Codificar",width = 10, height=2).place(x=100, y=405)
        self.botonLimpiar = Button(self,text="Limpiar",width = 10, height=2).place(x=190, y=405)

    def start(self):
        self.mainloop()
    
    def stop(self):
        self.destroy()
        
if __name__ == "__main__":
    app = mainApp()
    app.start()
    app.stop()
