# -*- coding: utf-8 -*-
"""
Created on Sat May  6 16:29:38 2023

@author: Jose

Esta clase es más especifica para el sistema menos generica para los modelos.
Tiene una implementación propia para manejar ciertas cosas del sistema
"""

from core.controllers.inputs import InputUser
from core.views.logger       import Logger

from core.views.menu_components   import MenuComponents
from core.views.menu_devices      import MenuDevices
from core.views.menu_management   import MenuManagament

class SystemController:
    def __init__(self):
        
        self._components = MenuComponents()                
        self._equipos    = MenuDevices(self._components)   
        self._gestion    = MenuManagament(self._equipos) 
    
    
    def components_run(self):
        self._components.update()
    def devices_run(self):
        self._equipos.update()
    def management_run(self, op):
        self._gestion.update(op)
    
    def exit_control(self):        
        warn = "La información no guardada se perderá."
        Logger.Core.info(warn)
        question = "¿Está seguro de querer salir?"
        return InputUser.ask_yes_no_question(question)