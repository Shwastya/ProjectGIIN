# -*- coding: utf-8 -*-
"""
Proyecto: HardVIU
Created on Tue Mar 28 16:43:02 2023
@author: José Luis Rosa Maiques
"""

# from core.kconfig import K_USER_CANCEL
from utils.drawer import MenuDrawer
#from utils.inputs import InputUser
from utils.logger import Logger


#from core.entity.device import Device

from core.entitymanager.EntityManager import EntityType, EntityManager

# NOTA IMPORTANTE:
# La clase ManagerDevices hereda de la clase EntityManager e implementa sus
# métodos, que tienen como objetivo ser genéricos para todas las entidades.
# Además, se pasa la clase ManagerComponents como parámetro en el
# constructor (composición), ya que necesitamos el listado de componentes del
# diccionario que se instancia mediante herencia desde EntityManager.

class ManagerDevices(EntityManager):
    
    def __init__(self, manager_components):
        
        super().__init__(EntityType.DEVICE)
        
        self._manager_components = manager_components
    
        # Menu principal
        self._menu_dev = MenuDrawer("HardVIU / 2) Equipos", ["Alta",
                                                             "Modificación"])
    
        # Submenu nueva alta
        self._menu_add = MenuDrawer("HardVIU / 2) Equipos / 1) Alta")
    
        # Submenu modificación equipo
        self._menu_modi = MenuDrawer("HardVIU / 2) Equipos / 2) Modificación",[
                "Cambiar configuración", "Desensamblar"])
    
    def add_device(self, repat = True):   
        
        components_dic = self._manager_components.get_components_dic()        
        return super().add_entity(self._menu_add, "Nombre/ID", 
                                  "alfanumérico, mínimo 3 caracteres", 
                                  components_dic, True)
    
    def select_device(self):
        q = "Nombre/ID para acceder a menú Modificación"  # Question
        t = "o 'L' para listar"                           # Tip
    
        return super().select_entity(q, t)
    
    def sub_menu_modification(self, id):
        while True:
            self._menu_modi.display(
                True, show_options=True, zero="Salir", obj=id)
            option = self._menu_modi.get_option()
            if option == 0:    # Salir de Menu modificación
                Logger.scroll_screen()
                break
            elif option == 1:  # Cambiar configuración
                self.modify_device_configuration(id)
                continue
            elif option == 2:  # Desensamblar
                if self.disassemble_device(id):
                    break
                continue
            else:
                Logger.bad_option()
    
    def change_configuration(self, device_id):
        device = self._entities_dic[device_id]
        old_components = device._components.copy()
    
        if self.configure_device(device):
            # Update the stock of the old components
            for component_type, component in old_components.items():
                self._manager_components._entities_dic[component].increase_stock(1)
            Logger.success_pause("Equipo: ", device.display(),
                                 " configuración actualizada.", True)
        else:
            Logger.register_quit("Cancelado por usuario")
    
    def disassemble_device(self, device_id):
        device = self._entities_dic[device_id]
    
        if Logger.there_is_the_question(
                "¿Está seguro de que desea desensamblar este equipo?"):
            for component_type, component in device._components.items():
                self._manager_components._entities_dic[component].increase_stock(1)
            Logger.success_pause("Equipo: ", device.display(),
                                 " desensamblado y eliminado del sistema.", True)
            del self._entities_dic[device_id]
            return True
        else:
            Logger.register_quit("Cancelado por usuario")
            return False
        
    
                
    def update(self):                 # Función a llamar desde sistema
        while True:
            self._menu_dev.display(zero="Salir")
            option = self._menu_dev.get_option()
            if option == 1:
                self.add_device()  # Alta equipo
            elif option == 2:
                id = self.select_device()
                if id is None:
                    continue
                self.sub_menu_modification(id)
            elif option == 0:
                break                 # Salir de menu Equipos
            else:
                Logger.bad_option()   # Opción no encontrada       
    