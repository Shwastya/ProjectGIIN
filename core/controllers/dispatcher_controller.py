# -*- coding: utf-8 -*-
"""
Created on Thu May  4 22:23:14 2023

@author: Jose
"""


from core.controllers.inputs import InputUser
from core.views.logger       import Logger

class DispatcherController:
    def __init__(self, dispatcher_dic):
        
        self._dispatcher_dic = dispatcher_dic
        
        # Este "Controller" necesita acceso al 'DistributorController'
        self._distributor_controller = None              
        
    def link_distributor_controller(self, distributor_controller):
        self._distributor_controller = distributor_controller
        
    def get_dic(self):
        return self._dispatcher_dic
    
    def get_model_data_from_user(self, id):
        Logger.Core.error("'get_model_data_from_user()' [sin implementar]")
        Logger.pause()
        pass