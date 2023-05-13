# -*- coding: utf-8 -*-
"""
Created on Wed May  3 17:01:27 2023

@author: Jose

La clase DistributorController define funciones similares a las de 
ComponentController y DeviceController. La función get_model_data_from_user 
recopila los datos del usuario para crear o modificar un distribuidor, mientras
que la función remove se encarga de eliminar un distribuidor del sistema. 
También se proporciona una función get_dic para acceder al diccionario de 
distribuidores.

Esta implementación básica debería servir como punto de partida para trabajar 
en el controlador de distribuidores en tu sistema HardVIU. Es posible que necesites ajustar algunas partes del código para que se adapte completamente a tu proyecto.
"""

from core.controllers.inputs import InputUser
from core.views.logger       import Logger

class DistributorController:
    def __init__(self, distributor_dic):
        self._distributor_dic = distributor_dic

    def get_dic(self):
        return self._distributor_dic

    def get_model_data_from_user(self, id):
        """
        IMPORTANTE:
        Todos los controllers de los modelos deben implementar esta función
        Que debe estar en consonancia con la estructura del modelo.
        """
        name = InputUser.get_str("Nombre del distribuidor: ")
        if name is None:
            return False
        phone = InputUser.get_str("Teléfono del distribuidor: ")
        if phone is None:
            return False
        email = InputUser.get_str("Email del distribuidor: ")
        if email is None:
            return False
        address = InputUser.get_str("Dirección del distribuidor: ")
        if address is None:
            return False

        data = (name, phone, email, address)
        return data

    def remove(self, id):
        """
        Para todos los métodos de los 'controllers' específicos, la función
        debe tener el mismo nombre.
        """
        Logger.Core.action("Distribuidor a eliminar", id, pause=False)
        question = "¿Seguro que desea eliminar este distribuidor del sistema?"
        if InputUser.ask_yes_no_question("\n" + question):
            del self._distributor_dic[id]
            return True
        else:
            return False