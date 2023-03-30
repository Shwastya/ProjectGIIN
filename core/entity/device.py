# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 16:42:39 2023

@author: Jose
"""

from core.entity.component import ComponentType


class Device:
    def __init__(self):
        self._id = None
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

    def display(self): 
        return self.to_string()
    def to_string(self):
        device_info = 'Device ID: ' + self._id + '\n'
        components_info = ''
        for component_type, component in self._components.items():
            components_info += component_type + ': ' 
            + component.serialize_to_string() + '\n'
        return device_info + components_info
