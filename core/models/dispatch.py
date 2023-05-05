# -*- coding: utf-8 -*-
"""
Created on Thu May  4 17:33:28 2023

@author: Jose
"""

from config.settings import K_SEPARATOR
from core.views.drawer import Displayer

class Dispatch:
    def __init__(self, device_id, distributor_id, delivery_days):
        """
        Algunos método tienen que ser comunes para todas los modelos.             
        """    
        self._device_id = device_id
        self._distributor_id = distributor_id
        self._delivery_days = delivery_days
        self._remaining_days = delivery_days

    def get_device_id(self):
        return self._device_id

    def get_distributor_id(self):
        return self._distributor_id

    def get_delivery_days(self):
        return self._delivery_days

    def get_remaining_days(self):
        return self._remaining_days

    def update_remaining_days(self, days_passed):
        self._remaining_days -= days_passed
        if self._remaining_days < 0: self._remaining_days = 0

    def is_delivered(self):
        return self._remaining_days == 0

    def display(self):
        print(f"Dispositivo: {self._device_id}, Distribuidor: {self._distributor_id}, Días restantes: {self._remaining_days}")

    def serialize_to_string(self):
        s = K_SEPARATOR
        return self._device_id + s + self._distributor_id + s + str(self._delivery_days) + s + str(self._remaining_days)

