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
clase para gestionar archivos.
"""
from core.controllers.system_controller import SystemController

from core.views.drawer import MenuDrawer
from core.views.logger import Logger

from core.views.menu_components   import MenuComponents
from core.views.menu_devices      import MenuDevices
from core.views.menu_distributors import MenuDistributors
from core.views.menu_dispatches   import MenuDispatches

class System:
    """    
    La clase System representa el sistema completo de componentes:
        equipos
        distribuidores
        despachos.
    """
    def __init__(self):          
        self._components     = MenuComponents()                
        self._equipos        = MenuDevices(self._components)   
        self._distribuidores = MenuDistributors(self._equipos) 
        self._despachos      = MenuDispatches(self._distribuidores)
        # self.dias      = ...
        # self.historico = ...
        
        self._main_menu = MenuDrawer("- HardVIU Menu -", [
            "Componentes", "Equipos", "Distribuidores", "Despachar", "Días",
            "Info sistema", "Ficheros"])
        
        self._main_menu.set_first_init(True)    
        
        self._system = SystemController()

    def run(self):
        while True:
            self._main_menu.display()  
            
            option = self._main_menu.get_option()

            if   option == 1: self._components.update()
            elif option == 2: self._equipos.update()                
            elif option == 3: self._distribuidores.update()                
            elif option == 4: self._despachos.update()
            elif option == 5:
                print("Option 5 (En implemtación)")
                Logger.pause();
            elif option == 6:
                print("Option 6 (En implemtación)")
                Logger.pause();
            elif option == 7:
                print("Option 7 (En implemtación)")
                Logger.pause();
            elif option == 0: 
                if self._system.exit_control(): break
            else: Logger.UI.bad_option()  
                
