# -*- coding: utf-8 -*-
"""
Proyecto: HardVIU
Created on Tue Mar 24 19:28:54 2023
@author: José Luis Rosa Maiques

Se separa la estructura y funcionalidad de Component en este módulo.
La función to_string se usará para facilitar el guardado de ficheros con el 
separador ';' definido como constante en el archivo de config. kconfig.py. 
"""

from core.kconfig import K_SEPARATOR

from enum import Enum
class ComponentType(Enum):

    FUENTE = "Fuente"
    PB     = "PB"
    TG     = "TG"
    CPU    = "CPU"
    RAM    = "RAM"
    DISCO  = "Disco"

    # metodo de clase, es necesario poner @classmethod y usar cls
    # para poder llamar de manera estatica a la función sin instanciar
    @classmethod
    def display(cls):
        # Listado de Tipos de componentes:
        print("Tipos de componente definidos en el sistema:")
        index = 1
        for ct in cls:           
            print("\033[1;36m\t" + str(index) + ". " + ct.value + "\033[0;m")
            index += 1

class Component:
    def __init__(self):
        """
        Algunos método tienen que ser comunes para todas las entidades.
        Nota: 
            investigar si se puede hacer interfaz virtual override como en C++               
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
        
    def set_quantity(self, n): 
        """
        Si queremos cambiar el stock directamente
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
    
    def set_from_user_data(self, data):
        self.set_values(data[0], data[1], data[2], data[3])   
        
    def get_type(self): 
        return self._tipo.value 
    
    def display_component_type_list(self):
        """
        Muestra la lista de componentes del class enum.
        """
        ComponentType.display()
    
    def display(self, id, show_type = True): 
        """ 
        Para mostrar de manera personalizada en consola 
        """       
        tipo = self._tipo.value
        if not show_type: tipo = ""
        
        return "\t" + '"' + id + '": ' + tipo + ", " + str(self._peso) + "g, " + str(self._precio) + "€, " + str(self._cantidad) + " stock."

    # Para guardar en archivo
    def serialize_to_string(self, id):
        """
        Serialización personalizada a string para guardar en archivo. 
        La var.'s' de una constante definida en kconfig.py. Por defecto ';'.
        """
        s = K_SEPARATOR
        to_string = id + s + str(self._tipo.value) + s + str(self._peso) 
        + s + str(self._precio) + s + str(self._cantidad)
        return to_string
    
    
    
