# -*- coding: utf-8 -*-
"""
Proyecto: HardVIU
Created on Tue Mar 21 09:53:06 2023
@author: José Luis Rosa Maiques

La clase Engine se encarga de gestionar y ejecutar sistemas.
En este caso, solo tenemos el sistema HardVIU.

Todos los menús son creados utilizando la misma clase/módulo Menu.
Cada elemento o componente del sistema empleará dicha clase para su propio menú.
"""

from core.sistema import Sistema
from utils.logger import Logger

class Engine:
    """
    La clase Engine se encarga de gestionar y ejecutar el sistema deseado.
    Logger es una clase personalizada con métodos estáticos.
    """

    def __init__(self):        
        self._sistema = Sistema()
    
    def run(self):
        
        Logger.starting()
        # ->
        self._sistema.update()
        # <-
        Logger.shutdown()
