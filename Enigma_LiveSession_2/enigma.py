import random

# Rotor Live Session 1 - Lo desechamos por ahora
''' 
class Rotor_():

    def __init__(self, abecedario="ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"):
        self.abecedario = abecedario
        self.rotor = []
        self.ix = 0
        otrasLetras = list(self.abecedario)
        for l in self.abecedario:
            n = random.randrange(len(otrasLetras))
            self.rotor.append((l, otrasLetras[n]))
            otrasLetras.pop(n)

        self.rotorC = self.rotor[:]
        

    def codifica(self, letra):
        pLetra = self.abecedario.index(letra)
        return self.rotorC[pLetra][1]
        self.avanza()

        #raise ValueError("{} no pertenece al abecedario".format(letra))



    def posicionInicial(self, letra):
        position = self.abecedario.index(letra)
        self.rotorC = self.rotor[position:] + self.rotor[:position]

    def avanza(self):
        self.rotorC = self.rotorC[1:] + self.rotorC[0]
'''
class Reflector():
    '''
        TODO:
            - Configuración: lista de pares del abecedario
              solo se repite uno si la longitud es impar (Hecho)
              es biunivoca
            - refleja(letra_entrada) -> letra (Lo he cambiado a pines, en lugar de a letras para hacerlo compatible con el nuevo rotor)
    '''    
    __alfabetoPrefijado = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
    
    def __init__(self, conf=["ABCDEFGHIJKLMNÑOPQRSTUVWXYZ", "ZYXWVUTSRQPOÑNMLKJIHGFEDCBA"]):
        '''
            si conf viene vacio, crear uno (abecedario) (Hecho)
            si conf viene lleno, comprobar que cumple las especificaciones (Hecho)
        '''
        self.configuracion = conf
        if not self.__esReflector(self.configuracion):
            self.configuracion = self.__creaReflector()
            print (self.configuracion,self.__esReflector(self.configuracion))
            
    def __creaReflector(self): # Crea las conexiones de un reflector de forma aleatoria.
        conexiones=[self.__alfabetoPrefijado,""]
        listaAux = list(self.__alfabetoPrefijado)
        for indiceAlfabeto in range(0,len(self.__alfabetoPrefijado)):
            try: # Intentamos asignación aleatoria de un caracter disponible.
                listaAux.remove(self.__alfabetoPrefijado[indiceAlfabeto]) # El propio caracter no.
                indice = random.randrange(len(listaAux))
                conexiones[1] += listaAux[indice]
                listaAux.pop(indice) # Si se ha asignado uno ya no estará disponible.
            except: # Caracter ya había sido asignado, hay que buscar su par.
                try:
                    conexiones[1] += self.__alfabetoPrefijado[conexiones[1].index(self.__alfabetoPrefijado[indiceAlfabeto])]
                except: # Si el alfabeto es impara hay que asociar una letra consigo misma.
                    conexiones[1] += self.__alfabetoPrefijado[indiceAlfabeto]
            indiceAlfabeto += 1 
        return conexiones
    
    def __esReflector(self,configuracion): # Determina si el parámetro de entrada funciona como reflector.
        try:
            entrada = str(configuracion[0])
        except:
            return False
        try:
            salida = str(configuracion[1])
        except:
            return False
        if len(entrada) == len(salida):
            contador = 0
            for indice in entrada:
                try:
                    indiceReflejo = salida.index(indice)
                    if salida[contador] != entrada[indiceReflejo]:
                        return False
                except:
                    return False
                contador += 1
        return True

    def refleja(self, contactoIn): # He cambiado letra_entrada x contactoIn para adaptarlo a pines y no a letras, como el rotor.
        letraIn = self.configuracion[0][contactoIn]
        return self.configuracion[1].index(letraIn)


class Rotor():
    '''
        TODO:
            - Conexion: Lista de cadenas (abecedario, cortocircuito) que 
              determina la entrada y salida según el caracter de salida o entrada (Hecho)
            - Posicion: Indice/caracter en posición cero de la conexión (Hecho como índice)
            - Pasos ¿?: Número de pasos girados desde que empezamos a codificar (Yo no veo la necesidad, pero lo he puesto para los que si lo quieran usar)
            - Salto: Indice, caracter de abecedario en que se obliga al salto del
              siguiente rotor si lo hubiera (Hecho como índice).
            - swSalto ¿?: True o False (Hecho)
            - codifica(indice): Devuelve el pin de salida (Hecho, controlando la posición del rotor)
            - decodifica(indice): Devuelve el pin de entrada (Hecho, controlando la posición del rotor)
            - avanza(): Rota una posición la conexión. Comprueba si debe activar swSalto (Hecho, )
    '''
    def __init__(self, abecedario, cortocircuito=None):
        
        self.conexion = [abecedario, cortocircuito]
        if not self.__esRotor(self.conexion):
            self.conexion = self.__creaRotor(abecedario)
        self._pos_ini = self.conexion[0][0] # Por defecto está en la primera posición.
        self.indicePosActual = self.conexion[0].index(self._pos_ini)
        self.pasos = 0
        self.indicePosArrastre = len(self.conexion[0])-1
        self.arrastrarSiguiente = False


    def codifica(self, indice):
        indice = (indice + self.indicePosActual) % len(self.conexion[0])
        letra = self.conexion[0][indice]
        indice_dcha = self.conexion[1].index(letra) - self.indicePosActual
        return indice_dcha

    def decodifica(self, indice):
        indice = (indice + self.indicePosActual) % len(self.conexion[0])
        letra = self.conexion[1][indice]
        indice_izda = self.conexion[0].index(letra) - self.indicePosActual
        return indice_izda
    
    def avanza(self):
        if self.indicePosActual == self.indicePosArrastre:
            self.arrastrarSiguiente = True
        self.pasos += 1
        self.indicePosActual = (self.indicePosActual + 1) % len(self.conexion[0])
    
    def posicion(self, posicion = None):
        if posicion != None:
            if posicion not in self.conexion[0]:
                posicion = self.rotor.conexion[0][0]
            self.indicePosActual = self.conexion[0].index(posicion)
        else:
            posicion = self.conexion[indicePosActual]
        return posicion

    
    def __creaRotor(self, alfabeto):
        conexiones=[alfabeto,""]
        listaAux = list(alfabeto)
        for item in alfabeto:
            indice = random.randrange(len(listaAux))
            conexiones[1] += listaAux[indice]
            listaAux.pop(indice)
        return conexiones

    def __esRotor(self,configuracion): # Determina si las conexiones están bien montadas.
        try:
            entrada = str(configuracion[0])
        except:
            return False
        try:
            salida = str(configuracion[1])
        except:
            return False
        if len(entrada) == len(salida):
            contador = 0
            for indice in entrada:
                if indice not in salida:
                    return False
                contador += 1
        return True

    @property
    def pos_ini(self):
        return self._pos_ini

    @pos_ini.setter
    def pos_ini(self, value):
        self._pos_ini = self.conexion[0].index(value)

class Enigma():
    '''
    TODO:
        - reflector: su configuración prefijada en principio (Hecho)
        - rotor: su conexión prefijada en principio (Hecho)
        - posi_inicial: Letra inicial del rotor (indice?) (Hecho. El rotor ya se configura así por defecto.)
        - codifica(mensaje): Transforma el mensaje en uno nuevo. Solo hay una dirección. (Hecho)
        Si se pasa la salida de codifica como entrada volviendo la posi_inicial. Obtenemos
        la otra entrada. (Hecho)
    '''
    __rotorPrefijado = ["ABCDEFGHIJKLMNÑOPQRSTUVWXYZ", "ÑMHCKWNOJFZEPSUBGRXAIQTVYLD"]
    __refletorPrefijado = ["ABCDEFGHIJKLMNÑOPQRSTUVWXYZ", "ZYXWVUTSRQPOÑNMLKJIHGFEDCBA"]
    __textoProcesado = ""
    listaErrores = {}

    def __init__(self, rotor=None, reflector=None, configIni=None):
        self.rotor = Rotor(self.__rotorPrefijado[0],self.__rotorPrefijado[1])
        self.reflector = Reflector(self.__refletorPrefijado)
    
    def codifica(self, clave):
        
        for letra in clave:
            if letra in self.__rotorPrefijado[0]:
                self.rotor.avanza()
                indiceLetra = self.rotor.conexion[0].index(letra) # Convierte la letra en el indice para mandar al rotor
                indiceLetra = self.rotor.codifica(indiceLetra) 
                indiceLetra = self.reflector.refleja(indiceLetra)
                indiceClave = self.rotor.decodifica(indiceLetra)
                if self.rotor.arrastrarSiguiente:
                    # Si ubiera mas rotores los tendríamos que avanzar aquí.
                    self.rotor.arrastrarSiguiente = False
                letraCodificada = self.rotor.conexion[0][indiceClave % len(self.rotor.conexion[0])] # Convierte la salida del circuito en una letra.
                self.__textoProcesado += letraCodificada
            else:
                if letra in self.listaErrores:
                    self.listaErrores[letra] += 1
                else:
                    self.listaErrores.update({letra:1})
        return self.__textoProcesado
    
    def configuraRotor(self,posicion = None):
        if posicion != None:
            if posicion not in self.rotor.conexion[0]:
                posicion = self.rotor.conexion[0][0]
            self.rotor.posicion(posicion)
            self.__textoProcesado = ""
            self.listaErrores = {}
        else:
            posicion = self.rotor.conexion[self.rotor.indicePosActual]
        return posicion

if __name__ == "__main__":

    # Prueba enigma.
    maquina = Enigma()
    textoPlano = "PUESVAMOS QUE NOS VAMOS AAAAAAAAAAAAAAAAVERRRRRRRRRRRRRRR QUE PARECE QUE SI FUNCIONA YA @.-733"
    textoEncriptado = ""
    textoDesencriptado = ""
    
    # Aquí se codifica el texto.
    textoEncriptado = maquina.codifica(textoPlano)
    print("Texto plano:")
    print(textoPlano)
    print("Texto encriptado:")
    print(textoEncriptado)
    print("Caracteres no procesados: {}".format(maquina.listaErrores))
    
    # Aquí se resetea la máquina a la posición inicial y se vuelve a codificar el texto ya encriptado.
    maquina.configuraRotor("A") # Esto implica resetear la máquina.
    textoDesencriptado = maquina.codifica(textoEncriptado)
    print("Texto decodificado:")
    print(textoDesencriptado)
    print("Caracteres no procesados: {}".format(maquina.listaErrores))
