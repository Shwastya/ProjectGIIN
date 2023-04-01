# -*- coding: utf-8 -*-
"""
Proyecto: HardVIU
Created on Tue Mar 24 19:28:54 2023
@author: José Luis Rosa Maiques


Se separa la estructura y funcionalidad de Component separada en este módulo.
La función to_string se usará para facilitar el guardado de ficheros con el separador ';'.
El separador ';' está definidad como constante en el archivo de configuración kconfig.py. 
"""

# Entidad Componente ----------------------------------------------------------

from utils.logger import Logger
from utils.inputs import InputUser
from core.kconfig import K_SEPARATOR as sep

from enum import Enum
class ComponentType(Enum):

    FUENTE = "Fuente"
    PB = "PB"
    TG = "TG"
    CPU = "CPU"
    RAM = "RAM"
    DISCO = "Disco"

    # metodo de clase, es necesario poner @classmethod y usar cls
    # para poder llamar de manera estatica a la función (sin instanciar)
    @classmethod
    def display(cls):
        # Listado de Tipos de componentes:
        index = 1
        for ct in cls:
            print("\t" + str(index) + ". " + ct.value)
            index += 1


class Component:
    def __init__(self):
        """
        Sin argumentos, se quiere poder instanciar la clase,
        pero sin necesidad de dar valores al crear el objeto.
        Atributos privados en Python... no exactamente, son convenciones.                
        """    
        self._tipo = None
        self._peso = None
        self._precio = None
        self._cantidad = None

    def set_values(self, tipo, peso, precio, cantidad = 0):     
        self._tipo = ComponentType(tipo)
        self._peso = peso
        self._precio = precio
        if cantidad != 0: self._cantidad = cantidad

    def get_type(self, t): return self._tipo

    def user_set_values(self, id, prmtrs): # stock = "Cantidad"
        """
        # La función devuelve los valores o False en caso 
        de cancelación o fallo.
        """
       # id        = pr
        stock     = prmtrs.get("stock", None)
        stock_msg = "Nueva cantidad"
        
        # Si se trata de nueva cantidad, la función se llama para modificar
        # el stock.
        
        # Si no se trata de "Nueva cantidad", la función se llama para
        # registrar un nuevo componente y mostramos primero el listado
            
        if stock == "Cantidad":
            
            stock_msg = stock            
            
            ComponentType.display()

            tipo = InputUser.get_enum(ComponentType,
                "Elija un número de la lista para el tipo de componente = ",
                "El Tipo de componente no está en la lista.")
            if tipo is None: return False
            Logger.info(tipo.value + ' "' + id + '".')

            peso = InputUser.get_int("Peso en gramos del componente = ")
            if peso is None: return False
            Logger.info(tipo.value +' "'+ id +'". '+ str(peso) +' gramos.')

            precio = InputUser.get_float("Precio en euros del componente = ")
            if precio is None: return False
            Logger.info(tipo.value +' "'+ id +'". '+ str(precio) +' euros.')

            self.set_values(tipo.value, peso, precio)

        ca = InputUser.get_int(stock_msg + " de componentes = ")
        
        if ca is None: return False
        
        Logger.info(self._tipo.value +' "'+ id +'". '+ str(ca) +' de stock.')
        self._cantidad = ca

        #return tipo.value, 
        return True

    # Para mostrar en consola
    def display(self, id):
        return id + ": " + self._tipo.value + ", " + str(self._peso) + ", " + str(self._precio) + ", " + str(self._cantidad)

    # Para guardar en archivo
    def serialize_to_string(self, id):
        return id + sep + str(self._tipo.value) + sep + str(self._peso) + sep + str(self._precio) + sep + str(self._cantidad)
    
    
    
