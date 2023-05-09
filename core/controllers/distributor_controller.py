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
        
        # Este "Controller" necesita acceso al 'DeviceController'
        self._device_controller = None      
        
        self._address_config = {"question": "Dirección del distribuidor",
                                "rule"    : "máximo 100 caracteres", 
                                "minim"   : 1,   
                                "maxim"   : 100} 
        
    def link_device_controller(self, device_controller):
        self._device_controller = device_controller
        
    def get_dic(self):
        return self._distributor_dic

    # ADD
    def get_model_data_from_user(self, id):
        """
        Devuelve una tupla para guardar mediante método del model.
        """
       
        delivery = InputUser.get_uint(
            "Tiempo de entrega desde fábrica en días = ")
        
        if delivery is None: return False
        Logger.Core.info('<── ' + '"' + id + '". Tiempo de entrega ' 
                         + str(delivery) + ' días')
        
        address = InputUser.get_str(self._address_config["question"],
                                    self._address_config["rule"    ],
                                    self._address_config["minim"   ],
                                    self._address_config["maxim"   ], False)
        
        if address is None: return False
        Logger.Core.info('<── ' + '"' + id + '". ' + address)        

        data = (delivery, address)
        return data
    
    # MODIFY
    def set_modify_data_from_user(self, id):
        """
        No se ha pedido implementación para este caso
        """
        pass

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