# -*- coding: utf-8 -*-
"""
Created on Sat May  6 16:29:38 2023

@author: Jose

Esta clase es más especifica para el sistema menos generica para los modelos.
Tiene una implementación propia para manejar ciertas cosas del sistema
"""

from core.controllers.inputs import InputUser
from core.views.logger       import Logger

class SystemController:
    def __init__(self):
        
        self._nada = "nada"
    
    def exit_control(self):        
        warn = "La información no guardada se perderá."
        Logger.Core.info(warn)
        question = "¿Está seguro de querer salir?"
        return InputUser.ask_yes_no_question(question)