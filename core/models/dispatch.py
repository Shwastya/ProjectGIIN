# -*- coding: utf-8 -*-
"""
Created on Thu May  4 17:33:28 2023

@author: Jose
"""

from config.settings import K_SEPARATOR
from core.views.drawer import Displayer

from enum import Enum

class DispatchStatus(Enum):
    
    PENDING    = 1
    IN_TRANSIT = 2
    DELIVERED  = 3   
    RETURNED   = 4 # Devuelto a fábrica    

class Dispatch: # Modelo Despacho

    def __init__(self):
        
        self._status = DispatchStatus.PENDING
        
        self._distributor_id = None
        self._device_id      = None        
        self._delivery_days  = None
        self._remaining_days = None

    """
    '__update_status' es método privado de la clase.
    """
    def __update_status(self):       
        
        if self._remaining_days == self._delivery_days:
            self._status = DispatchStatus.PENDING
            
        elif 0 < self._remaining_days < self._delivery_days:
            self._status = DispatchStatus.IN_TRANSIT
            
        elif self._remaining_days == 0:
            self._status = DispatchStatus.DELIVERED
            
    """
    A partir de aquí los métodos públicos.
    """
    def set_dispatch(self, distributor_id, device_id):
        self._distributor_id = distributor_id
        self._device_id = device_id        

    def set_delivery_days(self, distributor_days):
        self._delivery_days = self._remaining_days = distributor_days        

    def update_remaining_days(self, days_passed):
        self._remaining_days -= days_passed
        if self._remaining_days < 0:
            self._remaining_days = 0
        
        # AL modificar los días faltantes se actualiza el estado (status).
        self._update_status()

    def get_status(self):
        return self._status
    
    def set_status_returned(self):
        self._status = DispatchStatus.RETURNED
    
    def display(self, id, col=False, tab=True, p_l=True, max_id_len=0, idx=1):        
        Displayer.dispatch(self, id, col, tab, p_l, max_id_len, idx)

    def serialize_to_string(self):
        s = K_SEPARATOR
        return self._device_id + s + self._distributor_id + s + str(self._delivery_days) + s + str(self._remaining_days)

