# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 16:42:39 2023

@author: Jose
"""

from core.kconfig import K_SEPARATOR

class Device:
    def __init__(self):
        
        """
        Se planteaba inicialmente una lista de componentes, pero
        considerando que contamos con una función que selecciona los
        componentes según su tipo, se ha decidido redefinir la estructura
        como un diccionario, donde la clave será el tipo de componente.
        """
        self._components = {} # clave = tipo de componente

    def add_component(self, component_type, compact_component):
        """
        Agrega un componente compacto al dispositivo. El componente compacto es
        un diccionario que contiene la información esencial del componente como 
        su ID, peso y precio, no se incluye el tipo de componente ni el stock,
        ya que el tipo de componente se utiliza como clave en el diccionario 
        de componentes del dispositivo y el stock no es relevante para 
        el ensamblaje de un equipo.
        """
        self._components[component_type] = compact_component
        
    def set_from_user_data(self, data): # data -> Dic. recibido del usuario 
        for component_type, compact_component in data.items():
            self.add_component(component_type, compact_component)
            
    def get_component_by_type(self, component_type):
        return self._components.get(component_type)

    def remove_component_by_type(self, component_type):
        if component_type in self._components:
            del self._components[component_type]

    def get_componente(self, tipo):
        return self._components.get(tipo, None)
    
    def get_components_list(self):
        """
        Devuelve una lista de componentes presentes en el dispositivo.
        """
        components_list = []
        for component_type, component_info in self._components.items():
            components_list.append(component_info["id"])

        return components_list

    def display(self, id):
        device_info = "Equipo/ID = '" + id + "'\n"
        comps_info = ""
        for comp_type, comp in self._components.items():
            comps_info += ("\t- " + comp_type.value + ": "
                           + '"' + comp['id'] + '", '
                           + str(comp['peso']) + "g, "
                           + str(comp['precio']) + "€"
                           + "\n")
        return device_info + comps_info

    def serialize_to_string(self, id):
        s = K_SEPARATOR
        device_info = "#" + id + "\n"
        comps_info = ""
        for comp_type, comp in self._components.items():
            comps_info += (comp['id'] + s + comp_type.value
                           + s + str(comp['peso']) + s
                           + str(comp['precio']) + "\n")
        return device_info + comps_info

    """
    
    display mostraria de la siguiente manera
    
    Equipo: id
        - "Fuente": "cp1", peso, etc..
        - ... (otros componentes: PB, TB, TG, CPU, RAM, Disco)
        
        
    serialize_to_string, para guardar en archivo y recuperar despues
    mostraria de la siguiente manera
    
    #id
        componente serializado 1
        componente serializado 2
        ... (otros componentes serializados)
    """