# -*- coding: utf-8 -*-
"""
Proyecto: HardVIU
Created on Wed May  3 16:37:01 2023
@author: José Luis Rosa Maiques
"""

from config.settings import K_SEPARATOR
from core.views.drawer import Displayer

class Distributor:
    def __init__(self):
        """
        Algunos método tienen que ser comunes para todas los modelos.             
        """    
        self._delivery_time = None
        self._address       = None

    def set_from_user_data(self, data):
        self._delivery_time, self._address = data

    def update_delivery_time(self, new_delivery_time):
        self._delivery_time = new_delivery_time

    def update_address(self, new_address): self._address = new_address

    def display(self, id, col = False, tab = True, p_l = True, max_id_len = 0):
        """
        TODO: Display debería ser parte de la 'view'. Hay que replantear mejor 
        las responsabilidades:
            - ¿En Logger o en Drawer?
            - ¿LLamar desde las clases menu de la 'view'?
        """
        Displayer.distributor(self, id, col, tab, p_l, max_id_len)

    def serialize_to_string(self, id):
        s = K_SEPARATOR
        to_string = id + s + str(self._delivery_time) + s + self._address
        return to_string
