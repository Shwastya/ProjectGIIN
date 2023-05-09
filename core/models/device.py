# -*- coding: utf-8 -*-
"""
Proyecto: HardVIU
Created on Tue Mar 28 16:42:39 2023
@author: José Luis Rosa Maiques
"""

from config.settings   import K_SEPARATOR
from core.views.drawer import Displayer

class Device:
    def __init__(self):
        
        self._components    = {}   # clave = tipo de componente

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
        Esta función, se ha hecho debido a que, cuando se elimina un Equipo, 
        se desea restaurar el stock correspondiente.
        """
        components_list = []
        for component_type, component_info in self._components.items():
            components_list.append(component_info["id"])

        return components_list

    def display(self, id, col = False, tab = True, p_l = True, max_id_len = 0,
                idx = 1):
        """
        TODO: Display debería ser parte de la 'view'. Hay que replantear mejor 
        las responsabilidades:
            - ¿En Logger o en Drawer?
            - ¿LLamar desde las clases menu de la 'view'?
        """
        Displayer.device(self, id, col, tab, p_l, max_id_len, idx)
        

    def serialize_to_string(self, id):
        s = K_SEPARATOR
        device_info = "#" + id + "\n"
        comps_info = ""
        for comp_type, comp in self._components.items():
            comps_info += (comp['id'] + s + comp_type.value
                           + s + str(comp['peso']) + s
                           + str(comp['precio']) + "\n")
        return device_info + comps_info

