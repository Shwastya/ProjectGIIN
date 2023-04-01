# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 16:42:39 2023

@author: Jose
"""


from utils.inputs import InputUser

from core.entity.component import ComponentType

class Device:
    def __init__(self):
        
        """
        Se planteaba inicialmente una lista de componentes, pero
        considerando que contamos con una función que selecciona los
        componentes según su tipo, se ha decidido redefinir la estructura
        como un diccionario, donde la clave será el tipo de componente.
        """
        self._components = {}

    def set_id(self, id):
        self._id = id

    def add_component(self, component):
        component_type = component.get_type()
        self._components[component_type] = component

    def get_component_by_type(self, component_type):
        return self._components.get(component_type)

    def remove_component_by_type(self, component_type):
        if component_type in self._components:
            del self._components[component_type]

    def get_componente(self, tipo):
        return self._componentes.get(tipo, None)
    
    def user_set_values(self, id, stock_dic):
        """
        Permite al usuario ingresar información para configurar el dispositivo.

        Args:
            stock (dict): 
                diccionario de componentes disponibles donde las claves son 
                tipos de componentes y los valores son listas de componentes 
                disponibles de ese tipo.
        """

        for component_type, components in stock_dic.items():
            print(f"\nComponentes disponibles de tipo {component_type}:")
            
            # Mostrar los componentes disponibles de este tipo
            for component in components:
                print(f"  - {component.serialize_to_string()}")
            
            # Solicitar al usuario que seleccione un componente de este tipo
            selected_component_id = InputUser.get_string(f"Seleccione un componente de tipo {component_type} (ID): ")
            
            # Agregar el componente seleccionado al dispositivo
            selected_component = next((c for c in components if c.get_id() == selected_component_id), None)
            if selected_component is not None:
                self.add_component(selected_component)
            else:
                print(f"No se encontró ningún componente con ID {selected_component_id}.")

    def display(self): 
        return self.to_string()
    
    def to_string(self):
        device_info = 'Device ID: ' + self._id + '\n'
        components_info = ''
        for component_type, component in self._components.items():
            components_info += component_type + ': ' 
            + component.serialize_to_string() + '\n'
        return device_info + components_info
