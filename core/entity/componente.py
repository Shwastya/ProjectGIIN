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
    
    # metodo de clase, es necesario poner @classmethod
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
        
    def user_set_values(self, id):
        
        is_cancel = USER_CANCEL_MSG.lower()
        
        # se ha superado la comprobación del indentificado en el manager
        Logger.info("[saved]> ID de componente: " + id)   
             
        # Mostrar la lista de componentes
        TipoComponente.display()

        
        while True: # tipo de componente hasta que sea válido -----------------
        
            cad = input("Seleccione un número para el tipo de componente o 'L' para listar de nuevo = ")
            if cad.lower() == is_cancel:
                return False
            elif cad.isdigit(): 
                index = int(cad) - 1
                if index < 0 or index >= len(TipoComponente):
                    Logger.warn("El Tipo de componente no está en la lista.")
                else:
                    tipo = TipoComponente(list(TipoComponente)[index].value)
                    Logger.info("[saved]> Tipo de componente: " + tipo.value)
                    break
            elif cad.lower() == 'l': TipoComponente.display()
            else: Logger.warn("Por favor, introduce un número entero válido.")
       
        while True: # peso hasta que sea válido -------------------------------
        
            peso = input("Peso en gramos del componente = ")
            if peso.lower() == is_cancel: return False
            elif peso.isdigit() and int(peso) > 0:
                Logger.info("[saved]> Peso del componente: " + peso)
                peso = int(peso)                
                break
            else: Logger.warn("El número debe ser entero y mayor que 0.")

        
        while True: # precio hasta que sea válido -----------------------------
        
            precio = input("Precio en euros del componente = ")
            if precio.lower() == is_cancel: return False
            elif precio.replace('.', '', 1).isdigit() and float(precio) > 0:
                Logger.info("[saved]> Precio del componente: " + precio)
                precio = float(precio)
                break
            else: Logger.warn("Por favor, introduce un número real mayor que 0.")
            
        
        while True: # cantidad hasta que sea válido ---------------------------
        
            cantidad = input("Cantidad de componentes = ")
            if cantidad.lower() == is_cancel: return False
            elif cantidad.isdigit() and int(cantidad) > 0:
                Logger.info("[saved]> Cantidad de componentes: " + cantidad)
                cantidad = int(cantidad)
                break
            else: Logger.warn("Por favor, introduce un número entero mayor que 0.")

        self.set_values(id, tipo.value, peso, precio, cantidad)
        return True
        
    # Para mostrar en consola
    def display_componente(self):
        return f'"{self.id}", {self.tipo.value}, {self.peso}, {self.precio} ,{self.cantidad}'
    # Para guardar en archivo
    def serialize_to_string(self):
        return f'{self.id};{self.tipo.value};{self.peso};{self.precio};{self.cantidad}'
    
    
  
    
    
    
    