import random
import string

class Enigma: #Pendiente de definir
    pass

class Engranaje:
    
    ################################################################
    # Agrupación de rotores + reflector que simulan el conexionado #
    # interno y el avance de los rotores conforme a la             #
    # configuración del engranaje y de sus rotores.                #
    # Su configuración es una lista de N rotores + un reflector y  #
    # la posición innicial de los mismos.                          #
    # Tiene un método configEngranaje() para configurarlo  y otro  #
    # codifica() que sirve tanto para encriptar un texto como para #
    # desencriptarlo.                                              #
    # También tiene un método privado __refrescarConfigAct() que   #
    # refresca posición de los rotores tras el avance de estos.    #
    ################################################################  
    
    def __init__(self, cuantosRotores = 3): # Se autoconfigura con tres rotores + reflector aleatorios.
        self.rotores = []
        self.numRotores = cuantosRotores +1 # Incluye el reflector
        for contador in range(0,self.numRotores): # Bucle para crear tres rotores.
            self.rotores.append(Rotor())
        self.rotores.append(Rotor(1)) # Se añade el rotor.
        self.configIni = ""
        self.configAct = ""
        self.configArr = ""
        for contador in range(0,self.numRotores):
            self.configIni += self.rotores[contador].posIni
            self.configAct += self.rotores[contador].posAct
            self.configArr += self.rotores[contador].posArrastre

    def configEngranaje(self, rotores=[], inicio = ""):
        if (len(rotores) == len(inicio)) and rotores != []:
            inicio = inicio[:-1] + rotores[-1].conexiones[0][0] # Posición del reflector fija.
            self.rotores = []
            self.numRotores = len(rotores)            
            self.configIni = ""
            self.configAct = ""
            self.configArr = ""
            contador = 0
            for item in rotores:
                self.rotores.append(item)
                self.configArr = self.configArr + item.posArrastre
                if self.rotores[contador].posIni != inicio[contador]:
                    self.rotores[contador].posIni = inicio[contador]
                    self.rotores[contador].posAct = inicio[contador]
                contador += 1
            self.__refrescarConfigAct()    
            self.configIni = self.configAct
        else:
            return [self.numRotores,self.configIni,self.configAct,self.rotores]

    def codifica(self, clave):
        claveOriginal = clave
        # Este bucle codifica en cadena todos los rotores del engranaje
        # incluido el reflector, en sentido primer rotor >> reflector.
        # Lleva la codificación desde el teclado hasta la vuelta del reflector.
        for item in range(self.numRotores):
            if item == 0:
                self.rotores[item].avanza()
                self.__refrescarConfigAct()
            posClave = self.rotores[item].conexiones[0].index(clave)
            posRotor = self.rotores[item].conexiones[0].index(self.configAct[item])
            claveAux = self.rotores[item].conexiones[0][(posClave + posRotor) % len(self.rotores[item].conexiones[0])] 
            resultado = self.rotores[item].codifica(claveAux)
            if self.rotores[item].arrastrarRotorSiguiente: # Si la rotación del rotor anterior arrastra al siguiente
                indice = item
                while self.rotores[indice].arrastrarRotorSiguiente:
                    if indice < (len(self.rotores)-2): # Para que el reflector (el último rotor) nunca gire.
                        self.rotores[indice+1].avanza()
                    self.rotores[indice].arrastrarRotorSiguiente = False
                    indice += 1
                self.__refrescarConfigAct()
            clave = resultado
        # Este bucle codifica en cadena todos los rotores del engranaje
        # tras haber pasado por el reflector, en sentido reflector >> primer rotor.
        # Lleva la codificación desde la vuelta del reflector hasta la pantalla de visualización.
        for item in range(self.numRotores-2,-1,-1):
            posClave = self.rotores[item].conexiones[1].index(clave)
            posRotor = self.rotores[item].conexiones[0].index(self.configAct[item])
            claveAux = self.rotores[item].conexiones[1][(posClave - posRotor) % len(self.rotores[item].conexiones[0])]
            resultado = self.rotores[item].decodifica(claveAux)
            clave = resultado
        return resultado

    def __refrescarConfigAct(self):
        # Cuando uno o varios rotores avanzan, es necesario llamar a esta
        # función para que se refresque la posición de los rotores en el engranaje.
        self.configAct = ""
        for item in range(self.numRotores):
            self.configAct += self.rotores[item].posAct

class Rotor:

    ################################################################
    # Esta clase simula cada uno de los discos, bien sean rotores  #
    # o reflectores, que intervienen en la codificación.           # 
    # Dispone de 8 rotores + 1 reflector prefabricados, guardados  #
    # en una estructura de diccionario como atributo privado.      #
    #                                                              #
    # Al crear un objeto, por defecto genera un rotor con          # 
    # conexiones aleatorias. Si recibe un parametro en tipo <> 0   #
    # entonces genera un reflector con conexiones aleatorias       #
    #                                                              #
    # Mediante el método montarConexiones() se puede asignar un    #
    # rotor o reflector prefabricado y definir su posición y su    #
    #                                                              #
    # Mediane el método configRotor() se puede posicionar el rotor #
    # en una posición concreta y asignarle las posiciones de       #
    # arrastre que se quieran aplicar.                             #
    #                                                              #
    ################################################################  

    __rotoresPref = {
        "1":     ["ABCDEFGHIJKLMNÑOPQRSTUVWXYZ", "QXTMRIAZPBDÑJWEYFNGSVKOCUHL"],
        "2":     ["ABCDEFGHIJKLMNÑOPQRSTUVWXYZ", "JCFXSGQTZVORUABWHYDPKMÑLNEI"],
        "3":     ["ABCDEFGHIJKLMNÑOPQRSTUVWXYZ", "LDEKCGIXARÑQSWPNFUBYTJHZOMV"],
        "4":     ["ABCDEFGHIJKLMNÑOPQRSTUVWXYZ", "VLNACXZTJOWBKDSGFIÑRPQYEMHU"],
        "5":     ["ABCDEFGHIJKLMNÑOPQRSTUVWXYZ", "JOHEZÑDXRLTAUSQFBNPVMYCKGWI"],
        "6":     ["ABCDEFGHIJKLMNÑOPQRSTUVWXYZ", "CSLFNRMWKBEDJAPOIÑQXHZVGTYU"],
        "7":     ["ABCDEFGHIJKLMNÑOPQRSTUVWXYZ", "GWQKLSHVDTOÑJNCYAFMPXIZUBRE"],
        "8":     ["ABCDEFGHIJKLMNÑOPQRSTUVWXYZ", "WIZBVHUAQCTGRLJOÑNKDYXFSPME"],
        "R":     ["ABCDEFGHIJKLMNÑOPQRSTUVWXYZ", "ÑOPQRSTUVWXYZNABCDEFGHIJKLM"],
        "I":     ["ABCDEFGHIJKLMNOPQRSTUVWXYZ", "EKMFLGDQVZNTOWYHXUSPAIBRCJ"],
        "II":    ["ABCDEFGHIJKLMNOPQRSTUVWXYZ", "AJDKSIRUXBLHWTMCQGZNPYFVOE"],
        "III":   ["ABCDEFGHIJKLMNOPQRSTUVWXYZ", "BDFHJLCPRTXVZNYEIWGAKMUSQO"],
        "IV" :   ["ABCDEFGHIJKLMNOPQRSTUVWXYZ", "ESOVPZJAYQUIRHXLNFTGKDCMWB"],
        "V"  :   ["ABCDEFGHIJKLMNOPQRSTUVWXYZ", "VZBRGITYUPSDNHLXAWMJQOFECK"],
        "VI" :   ["ABCDEFGHIJKLMNOPQRSTUVWXYZ", "JPGVOUMFYQBENHZRDKASXLICTW"],
        "VII":   ["ABCDEFGHIJKLMNOPQRSTUVWXYZ", "NZJHGRCXMYSWBOUFAIVLPEKQDT"],
        "VIII":  ["ABCDEFGHIJKLMNOPQRSTUVWXYZ", "FKQHTLXOCBJSPDZRAMEWNIUYGV"],
        "RBETA": ["ABCDEFGHIJKLMNOPQRSTUVWXYZ", "LEYJVCNIXWPBQMDRTAKZGFUHOS"],
        "RGAMMA":["ABCDEFGHIJKLMNOPQRSTUVWXYZ", "FSOKANUERHMBTIYCWLQPZXVGJD"],
        "RA" :   ["ABCDEFGHIJKLMNOPQRSTUVWXYZ", "EJMZALYXVBWFCRQUONTSPIKHGD"],
        "RB" :   ["ABCDEFGHIJKLMNOPQRSTUVWXYZ", "YRUHQSLDPXNGOKMIEBFZCWVJAT"], 
        "RC" :   ["ABCDEFGHIJKLMNOPQRSTUVWXYZ", "FVPJIAOYEDRZXWGCTKUQSBNMHL"], 
        "RBEs" : ["ABCDEFGHIJKLMNOPQRSTUVWXYZ", "ENKQAUYWJICOPBLMDXZVFTHRGS"], 
        "RCEs" : ["ABCDEFGHIJKLMNOPQRSTUVWXYZ", "RDOBJNTKVEHMLFCWZAXGYIPSUQ"],  
    }

    arrastrarRotorSiguiente = False

    def __init__(self, tipo = 0, alfabeto="ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"):
        self.posIni="A"
        self.posAct = self.posIni
        self.conexiones = self.__conexiones(tipo,alfabeto)
        if tipo == 0:
            self.tipo = "Rotor Aleatorio"
            self.posArrastre = self.conexiones[0][-1]
        else:
            self.tipo = "Reflector Aleatorio"
            self.posArrastre = ""

    def codifica(self, clave):
        posClave = self.conexiones[0].index(clave)
        posRotor = self.conexiones[0].index(self.posAct)
        claveAux = self.conexiones[0][(posClave + posRotor) % len(self.conexiones[0])]
        posicion = self.conexiones[0].index(claveAux)
        return self.conexiones[1][posicion]
        
    def decodifica(self, clave):
        posClave = self.conexiones[1].index(clave)
        posRotor = self.conexiones[0].index(self.posAct)
        claveAux = self.conexiones[1][(posClave - posRotor) % len(self.conexiones[0])]
        posicion = self.conexiones[1].index(claveAux)
        return self.conexiones[0][posicion]
    
    def avanza(self):
        if self.posAct in self.posArrastre:
            self.arrastrarRotorSiguiente = True 
        posRotor = self.conexiones[0].index(self.posAct)
        claveAux = self.conexiones[0][(posRotor+1) % len(self.conexiones[0])]
        posicion = self.conexiones[0].index(claveAux)
        self.posAct = self.conexiones[0][posicion]
    
    def montarConexiones(self, referencia):
        if referencia in self.__rotoresPref:
            self.tipo = referencia
            self.posIni = self.__rotoresPref[referencia][0][0]
            self.posAct = self.posIni            
            self.conexiones = self.__rotoresPref[referencia]
            self.posArrastre = self.conexiones[0][-1]
        else:
            return [self.tipo,self.conexiones,self.posIni,self.posAct,self.posArrastre]
    
    def configRotor(self, posicion = None, arrastre = None):
        if posicion in self.conexiones[0]:
            self.posAct = posicion[0]
            if arrastre != None:
                for item in arrastre:
                    if item in self.conexiones[0]:
                        self.posArrastre += item
        else:
            return [self.tipo,self.conexiones,self.posIni,self.posAct,self.posArrastre]

    def __conexiones(self, tipo, alfabeto):
        conexiones=[alfabeto,""]
        listaAux = list(alfabeto)
        if tipo == 0: # Consideramos que es un rotor.
            for item in alfabeto:
                indice = random.randrange(len(listaAux))
                conexiones[1] += listaAux[indice]
                listaAux.pop(indice)
        else: # Si tipo !=0 consideramos que es un reflector.
            for indiceAlfabeto in range(0,len(alfabeto)):
                try: # Intentamos asignación aleatoria de un caracter disponible.
                    listaAux.remove(alfabeto[indiceAlfabeto]) # El propio caracter no.
                    indice = random.randrange(len(listaAux))
                    conexiones[1] += listaAux[indice]
                    listaAux.pop(indice) # Si se ha asignado uno ya no estará disponible.
                except: # Caracter ya había sido asignado, hay que buscar su par.
                    try:
                        conexiones[1] += alfabeto[conexiones[1].index(alfabeto[indiceAlfabeto])]
                    except: # Si el alfabeto es impara hay que asociar una letra consigo misma.
                        conexiones[1] += alfabeto[indiceAlfabeto]
                indiceAlfabeto += 1 
        return conexiones

def mainApp ():

    print("################################# Prueba engranaje:")
    # Definimos y configuramos los rotores, el reflector y el engranaje.
    r1 = Rotor()
    r2 = Rotor()
    r3 = Rotor()
    reflector = Rotor(1)
    r1.montarConexiones("I")
    r2.montarConexiones("II")
    r3.montarConexiones("III")
    reflector.montarConexiones("RB")
    engranaje = Engranaje()
    engranaje.configEngranaje([r1,r2,r3,reflector],"AAAA")

    # Codificamos el texto.
    textoplano="HOLAMUNDO"
    print("Texto plano:")
    print(textoplano)
    textoencriptado = ""
    for item in textoplano:
        textoencriptado += engranaje.codifica(item)
    print("Texto enriptado:")
    print(textoencriptado)
    
    # Reconfiguramos la máquina a su posición inicial.
    r1.montarConexiones("I")
    r2.montarConexiones("II")
    r3.montarConexiones("III")
    reflector.montarConexiones("RB")
    engranaje.configEngranaje([r1,r2,r3,reflector],"AAAA")
    
    # Volvemos a codificar el texto encriptado.
    textodesencriptado = ""
    for item in textoencriptado:
        textodesencriptado += engranaje.codifica(item)
    print("Texto desencriptado")
    print(textodesencriptado)

if __name__ == "__main__":

    mainApp()
    