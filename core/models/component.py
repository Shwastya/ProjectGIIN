# -*- coding: utf-8 -*-
"""
Proyecto: HardVIU
Created on Tue Mar 24 19:28:54 2023
@author: José Luis Rosa Maiques

Se separa la estructura y funcionalidad de Component en este módulo.
La función to_string se usará para facilitar el guardado de ficheros con el 
separador ';' definido como constante en el archivo de config.settings.py. 
"""

from config.settings   import K_SEPARATOR
from core.views.drawer import Displayer
from enum import Enum

class ComponentType(Enum):

    FUENTE = "Fuente"
    PB     = "PB"
    TG     = "TG"
    CPU    = "CPU"
    RAM    = "RAM"
    DISCO  = "Disco"
   
    @classmethod
    def display(cls):
        # Listado de Tipos de componentes:
        print("Tipos de componente definidos en el sistema:")
        index = 1
        for ct in cls:           
            print("\033[1;34m\t" + str(index) + ". " + ct.value + "\033[0;m")
            index += 1

class Component:
    def __init__(self):          
        self._tipo     = None
        self._peso     = None
        self._precio   = None
        self._cantidad = None   
        
    def set_from_user_data(self, data):
        """
        Ingresamos los datos directamente pasando un parametro como tupla
        """
        tipo, self._peso, self._precio, self._cantidad = data
        # Almacena como una instancia de ComponentType
        self._tipo = ComponentType(tipo) 

        
    def set_quantity(self, n): 
        """
        Si queremos cambiar el stock directamente. 
        (Aunque en Python no hay atributos privados como, lo hacemos hace por 
         mantener la similitud con una estructura OOP)
        """
        self._cantidad = n
        
    def update_quantity(self, n):
        """
        Se añaden o agregan unidades al stock existente por acciones del 
        usuario. Se puede agregar o substraer dependiendo de si es -n o +n
        """
        self._cantidad += n
        if self._cantidad < 0: return False
        return True         
    
    def display(self, id, col=False, tab=False, p_l=True, max_id_len=0, idx=1):
        Displayer.component(self, id, col, tab, p_l, max_id_len, idx)


    # Para guardar en archivo
    def serialize_to_string(self, id):
        """
        Serialización personalizada a string para guardar en archivo. 
        La var.'s' de una constante definida en kconfig.py. Por defecto ';'.
        """
        s = K_SEPARATOR
        to_string = id + s + self._tipo.value + s + str(self._peso) + s + str(self._precio) + s + str(self._cantidad)
        return to_string
    
    
    
