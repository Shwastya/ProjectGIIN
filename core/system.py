# -*- coding: utf-8 -*-
"""
Proyecto: HardVIU
Created on Tue Mar 21 19:54:47 2023
@author: José Luis Rosa Maiques

La clase Sistema tiene como objetivo crear un sistema de gestión de:
    componentes, equipos, distribuidores, despachos, Etc.    

Esta clase tiene el sistema completo, pero la implementación se encuentra en 
los modelos, vistas y controladores. en Sistema se llamarán principalmente a 
los métodos de la vista y algunas herramientas especificas como 'serializer'
clase para gestionar archivos. Generalmente todo a partir de 
'system_controller'
"""
from core.controllers.system_controller import SystemController

from core.views.drawer import MenuDrawer
from core.views.logger import Logger

class System:
    """    
    La clase System representa el sistema completo de componentes:
        equipos
        distribuidores
        despachos.
    """
    def __init__(self):   
        
        self._system = SystemController()
        
        self._main_menu = MenuDrawer("- HardVIU Menu -", [
            "Componentes", "Equipos", "Distribuidores", "Despachar", "Días",
            "Info Sistema", "Ficheros"])        
        self._main_menu.set_first_init(True)  
        

    def run(self):
        while True:
            self._main_menu.display()              
            op = self._main_menu.get_option()

            if   op == 1: self._system.components_run()
            elif op == 2: self._system.devices_run()
            elif op == 3 or op == 4 or op == 5 or op == 6: 
                self._system.management_run(op)     
            
                
                
            elif op == 7:
                print("Option 7 Files (En implemtación)")
                Logger.pause();
            elif op == 0: 
                if self._system.exit_control(): break
            else: Logger.UI.bad_option()  
                
