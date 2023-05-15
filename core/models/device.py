# -*- coding: utf-8 -*-
"""
Proyecto: HardVIU
Created on Tue Mar 28 16:42:39 2023
@author: José Luis Rosa Maiques
"""

from config.settings   import K_SEPARATOR
from core.views.drawer import Displayer

from enum import Enum

class DeviceStatus(Enum):
    
    NEW_DEVICE = 1
    DISPATCHED = 2
    DELIVERED  = 3
    RETURNED   = 4

class Device:
    def __init__(self):
        
        self._status     = DeviceStatus.NEW_DEVICE  # Estado inicial
        self._components = {}                       # clave = Tipo Componente
    
    def set_newdevice_status (self): self._status = DeviceStatus.NEW_DEVICE 
    def set_dispatched_status(self): self._status = DeviceStatus.DISPATCHED
    def set_delivered_status (self): self._status = DeviceStatus.DELIVERED
    def set_returned_status  (self): self._status = DeviceStatus.RETURNED
        
    def is_newdevice (self): return self._status == DeviceStatus.NEW_DEVICE
    def is_dispatched(self): return self._status == DeviceStatus.DISPATCHED
    def is_delivered (self): return self._status == DeviceStatus.DELIVERED
    def is_returned  (self): return self._status == DeviceStatus.RETURNED
    
        
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
        
    def get_status(self): return self._status

    def display(self, id, col=False, tab=True, p_l=True, max_id_len=0, idx=1):
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

