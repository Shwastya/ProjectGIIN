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
from core.kconfig import K_USER_CANCEL

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
        """
        self._id       = None       
        self._tipo     = None
        self._peso     = None
        self._precio   = None
        self._cantidad = None
        
        self._u_peso   = "gramos"
        self._u_precio = "euros"
        
    def set_values(self, id, tipo, peso, precio, cantidad = 0):
        self._id = id        
        self._tipo = TipoComponente(tipo)
        self._peso = peso
        self._precio = precio
        if cantidad != 0: self._cantidad = cantidad
    
    # Tipo de componente hasta que sea válido ---------------------------------        
    def get_tipo_input(self):
        while True: 
            cad = input("Elija un número de la lista para especificar el tipo de componente = ")
            if cad.lower() == K_USER_CANCEL.lower():
                return None
            elif cad.isdigit():
                index = int(cad) - 1
                if index < 0 or index >= len(TipoComponente):
                    Logger.warn("El Tipo de componente no está en la lista.")
                else: return TipoComponente(list(TipoComponente)[index].value)
            else: Logger.warn("Introduce un número válido de la lista.")
           
    # Peso hasta que sea válido -----------------------------------------------
    def get_peso_input(self):
        while True:
            peso = input("Peso en " + self._u_peso + " del componente = ")
            if peso.lower() == K_USER_CANCEL.lower(): return None
            elif peso.isdigit() and int(peso) > 0: return int(peso)
            else: Logger.warn("El número debe ser entero y mayor que 0.")
    
    # Precio hasta que sea válido ---------------------------------------------
    def get_precio_input(self):
        while True:
            precio = input("Precio en " + self._u_precio + " del componente = ")
            if precio.lower() == K_USER_CANCEL.lower(): return None
            elif precio.replace('.', '', 1).isdigit() and float(precio) > 0: return float(precio)
            else: Logger.warn("Introduce un número real mayor que 0.")
            
    # Cantidad hasta que sea válido -------------------------------------------
    def get_cantidad_input(self, stock):
        while True:
            cantidad = input(stock + " de componentes = ")
            if cantidad.lower() == K_USER_CANCEL.lower(): return None
            elif cantidad.isdigit() and int(cantidad) > 0: return int(cantidad)
            else: Logger.warn("Introduce un número entero mayor que 0.")
    
    
    def user_set_values(self, id, stock = "Cantidad"):        
        
        if stock == "Cantidad":
            """
            Si no se trata de "Nueva cantidad", la función se llama para registrar 
            un nuevo componente. Primero, se muestra el listado de componentes existentes.
            """            
            TipoComponente.display()            
            
            ti = self.get_tipo_input()
            if ti is None: return False
            Logger.info(ti.value + ' "' + id + '".')

            pe = self.get_peso_input()
            if pe is None: return False
            Logger.info(ti.value + ' "' + id + '". ' + str(pe) + ' gramos.')        

            pr = self.get_precio_input()
            if pr is None: return False
            Logger.info(ti.value + ' "' + id + '". ' + str(pr) + ' euros.') 
                
            self.set_values(id, ti.value, pe, pr)  
            
        ca = self.get_cantidad_input(stock)
        if ca is None: return False
        Logger.info(self._tipo.value + ' "' + id + '". ' + str(ca) + ' de stock.')        
        self._cantidad = ca           
        
        return True    
    
    # Para mostrar en consola
    def display(self):
        return f'"{self._id}": {self._tipo.value}, {self._peso}, {self._precio}, {self._cantidad}'
    
    # Para guardar en archivo
    def serialize_to_string(self):
        return f'{self._id};{self._tipo.value};{self._peso};{self._precio};{self._cantidad}'
    
    
  
    
    
    
    