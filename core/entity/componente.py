# -*- coding: utf-8 -*-
"""
Proyecto: HardVIU
Created on Tue Mar 24 19:28:54 2023
@author: José Luis Rosa Maiques

Entidades:
    La clases de este modulo representan la estructura de datos del sistema como entidades.
    La función to_string se usará para facilitar el guardado de ficheros con el separador ';'
"""

# Entidad Componente ----------------------------------------------------------

from utils.logger import Logger
from core.constsk import K_USER_CANCEL_MSG

from enum import Enum
class TipoComponente(Enum):
    
    FUENTE = "Fuente"
    PB     = "PB"
    TG     = "TG"
    CPU    = "CPU"
    RAM    = "RAM"
    DISCO  = "Disco"
    
    # metodo de clase, es necesario poner @classmethod y usar cls
    # para poder llamar de manera estatica a la función (sin instanciar)
    @classmethod
    def display(cls):
        #print("Tipos de componentes:")
        index = 1
        for tipo_componente in cls:
            print("\t" + str(index) + ". " + tipo_componente.value)            
            index += 1            

class Componente:
    def __init__(self):
        """
        Sin argumentos, se quiere poder instanciar la clase,
        pero sin necesidad de dar valores al crear el objeto.
        TODO: Revisar si esta es la mejor opción.
        """
        self._id       = None       
        self._tipo     = None
        self._peso     = None
        self._precio   = None
        self._cantidad = None
        
        self._u_peso   = "gramos"
        self._u_precio = "euros"
        
    def set_values(self, id, tipo, peso, precio, cantidad):
        self._id = id        
        self._tipo = TipoComponente(tipo)
        self._peso = peso
        self._precio = precio
        self._cantidad = cantidad     
    
    # Tipo de componente hasta que sea válido ---------------------------------        
    def get_tipo_input(self):
        while True: 
            cad = input("Seleccione un número para el tipo de componente o 'L' para listar de nuevo = ")
            if cad.lower() == K_USER_CANCEL_MSG.lower(): return None
            elif cad.isdigit():
                index = int(cad) - 1
                if index < 0 or index >= len(TipoComponente):
                    Logger.warn("El Tipo de componente no está en la lista.")
                else: return TipoComponente(list(TipoComponente)[index].value)
            elif cad.lower() == 'l': TipoComponente.display()
            else: Logger.warn("Error. Introduce un número entero válido.")
           
    # Peso hasta que sea válido -----------------------------------------------
    def get_peso_input(self):
        while True:
            peso = input("Peso en " + self._u_peso + " del componente = ")
            if peso.lower() == K_USER_CANCEL_MSG.lower(): return None
            elif peso.isdigit() and int(peso) > 0: return int(peso)
            else: Logger.warn("Error. El número debe ser entero y mayor que 0.")
    
    # Precio hasta que sea válido ---------------------------------------------
    def get_precio_input(self):
        while True:
            precio = input("Precio en " + self._u_precio + " del componente = ")
            if precio.lower() == K_USER_CANCEL_MSG.lower(): return None
            elif precio.replace('.', '', 1).isdigit() and float(precio) > 0: return float(precio)
            else: Logger.warn("Error. Introduce un número real mayor que 0.")
            
    # Cantidad hasta que sea válido -------------------------------------------
    def get_cantidad_input(self, msg = "Cantidad"):
        while True:
            cantidad = input(msg + " de componentes = ")
            if cantidad.lower() == K_USER_CANCEL_MSG.lower(): return None
            elif cantidad.isdigit() and int(cantidad) > 0: return int(cantidad)
            else: Logger.warn("Por favor, introduce un número entero mayor que 0.")
    
    
    def user_set_values(self, id):        
        
        # se ha superado la comprobación del indentificado en el manager
        #Logger.info("[saved]> ID de componente: " + id + "\n")   
        Logger.info('\nComponente id ' + '"' + id + '"')        
        
        # Mostrar la lista de componentes
        TipoComponente.display()

        ti = self.get_tipo_input()
        if ti is None: return False
        Logger.info('"'+id+'" <- '+ str(ti.value) + '.')

        pe = self.get_peso_input()
        if pe is None: return False
        Logger.info('"'+id+'" <- '+ str(pe) + ' ' + self._u_peso + '.')        

        pr = self.get_precio_input()
        if pr is None: return False
        Logger.info('"'+id+'" <- '+ str(pr) + ' ' + self._u_precio + '.')
        
        ca = self.get_cantidad_input()
        if ca is None: return False
        Logger.info('"'+id+'" <- '+ str(ca) + ' stock.')        

        self.set_values(id, ti.value, pe, pr, ca)        
        
        Logger.succes("Componente: ", self.display_componente(), " dado de alta con éxito.")
        return True        
    
    def user_set_new_stock(self):
        ca  = self.get_cantidad_input("Nueva cantidad")
        if ca is None: return False
        self._cantidad = ca
        #Logger.info("[Modified]> Stock actualizado a " + str(ca) + "\n")
        Logger.succes("Componente: ", self.display_componente(), " modificado con éxito.")
        input("\nPresione [ENTER] para continuar...")
        return True
    
    
    # Para mostrar en consola
    def display_componente(self):
        return f'"{self._id}": {self._tipo.value}, {self._peso}, {self._precio}, {self._cantidad}'
    
    # Para guardar en archivo
    def serialize_to_string(self):
        return f'{self._id};{self._tipo.value};{self._peso};{self._precio};{self._cantidad}'
    
    
  
    
    
    
    