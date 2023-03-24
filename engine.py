# -*- coding: utf-8 -*-
"""
Proyecto: HardVIU
Created on Tue Mar 21 09:53:06 2023
Author: José Luis Rosa Maiques

la clase Engine que se encarga de gestionar y ejecutar cualquier sistema que se desee implementar,
en este caso, solo tenemos el sistema HardVIU.
Cada sistema que se implemente tendrá su propio menú. 
Del mismo modo, cada elemento o componente del sistema tendrá su propio menú si es necesario. 
Todos los menús son creados por la misma clase/modulo Menu.
"""

from modulos.sistema import SistemaHardVIU
from modulos.menu import Menu

class Engine:
    """
    La clase Engine se encarga de gestionar y ejecutar el sistema deseado.

    Atributos:
        _sistema (obj): objeto de la clase SistemaHardVIU que representa el sistema a ejecutar.
    """

    def __init__(self):
        self._sistema = SistemaHardVIU()
    
    def run(self):
        self._sistema.run()
        
