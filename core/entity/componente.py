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
from core.constants import USER_CANCEL_MSG

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
        print("Tipos de componentes:")
        index = 1
        for tipo_componente in cls:
            print("\t" + str(index) + ". " + tipo_componente.value)            
            index += 1
            

class Componente:
    def __init__(self):
        """
        Sin argumentos, se quiere poder instanciar la clase,
        pero sin necesidad de dar valores al crear el objeto.
        Revisar si esta es buena opción.
        """
        self.id       = None       
        self.tipo     = None
        self.peso     = None
        self.precio   = None
        self.cantidad = None
        
    def set_values(self, id, tipo, peso, precio, cantidad):
        self.id = id        
        self.tipo = TipoComponente(tipo)
        self.peso = peso
        self.precio = precio
        self.cantidad = cantidad      
    
    def patata(self):
        print("PATATA")         
    
    # Tipo de componente hasta que sea válido ---------------------------------        
    def get_tipo_input(self):
        while True: 
            cad = input("Seleccione un número para el tipo de componente o 'L' para listar de nuevo = ")
            if cad.lower() == USER_CANCEL_MSG.lower(): return None
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
            peso = input("Peso en gramos del componente = ")
            if peso.lower() == USER_CANCEL_MSG.lower(): return None
            elif peso.isdigit() and int(peso) > 0: return int(peso)
            else: Logger.warn("Error. El número debe ser entero y mayor que 0.")
    
    # Precio hasta que sea válido ---------------------------------------------
    def get_precio_input(self):
        while True:
            precio = input("Precio en euros del componente = ")
            if precio.lower() == USER_CANCEL_MSG.lower(): return None
            elif precio.replace('.', '', 1).isdigit() and float(precio) > 0: return float(precio)
            else: Logger.warn("Error. Introduce un número real mayor que 0.")
            
    # Cantidad hasta que sea válido -------------------------------------------
    def get_cantidad_input(self, msg = "Cantidad"):
        while True:
            cantidad = input(msg + " de componentes = ")
            if cantidad.lower() == USER_CANCEL_MSG.lower(): return None
            elif cantidad.isdigit() and int(cantidad) > 0: return int(cantidad)
            else: Logger.warn("Por favor, introduce un número entero mayor que 0.")
    
    
    def user_set_values(self, id):        
        
        # se ha superado la comprobación del indentificado en el manager
        Logger.info("[saved]> ID de componente: " + id)   
             
        # Mostrar la lista de componentes
        TipoComponente.display()

        ti = self.get_tipo_input()
        if ti is None: return False
        Logger.info("[saved]> Tipo de componente: " + str(ti.value))        

        pe = self.get_peso_input()
        if pe is None: return False
        Logger.info("[saved]> Peso del componente: " + str(pe))        

        pr = self.get_precio_input()
        if pr is None: return False
        Logger.info("[saved]> Precio del componente: " + str(pr))

        ca = self.get_cantidad_input()
        if ca is None: return False
        Logger.info("[saved]> Cantidad de componentes: " + str(ca))

        self.set_values(id, ti.value, pe, pr, ca)        
        
        Logger.succes("\nComponente: ", self.display_componente(), " agregado con éxito.") 
        return True
    
    # Para modificar un Stock ya existente, igual podria tratar de usarse la
    # función get_cantidad_input, siempre que se mantuviera la lógica de mensajes
    def user_set_new_stock(self):
        
        while True:
            cantidad = input("Nueva cantidad de componentes = ")
            if cantidad.lower() == USER_CANCEL_MSG.lower():
                return self.register_quit()
            elif cantidad.isdigit() and int(cantidad) > 0:
                Logger.info("[Modified]> Stock actualizado: " + cantidad)
                #componente.cantidad = int(cantidad)                
                break
            else:
                Logger.warn("Por favor, introduce un número entero mayor que 0.")
    
    
    # Para mostrar en consola
    def display_componente(self):
        return f'"{self.id}": {self.tipo.value}, {self.peso}, {self.precio}, {self.cantidad}'
    
    # Para guardar en archivo
    def serialize_to_string(self):
        return f'{self.id};{self.tipo.value};{self.peso};{self.precio};{self.cantidad}'
    
    
  
    
    
    
    