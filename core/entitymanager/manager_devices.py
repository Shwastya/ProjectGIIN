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
        self._menu_dev = MenuDrawer("HardVIU / 2) Equipos", [
            "Alta", "Modificación", "Listar Equipos"], 1)
    
        # Submenu nueva alta
        self._menu_add = MenuDrawer("HardVIU / 2) Equipos / 1) Alta")
    
        # Submenu modificación equipo
        self._menu_modi = MenuDrawer("HardVIU / 2) Equipos / 2) Modificación",[
                "Cambiar configuración", "Desensamblar"])   
        
        # Submenu cambiar información
        self._menu_info = MenuDrawer("HardVIU / 1) Equipos / 2) " + 
                                     "Modificación / 2) Cambiar configuración")   
   
        
    def add_device(self, repeat = True):  # Alta de equipo  
        
        p = {"mode"    : "add", 
             "menu"    : self._menu_add,                      # Menu de alta             
             "question": "Nombre/ID del equipo:",             # Pregunta input
             "rule"    : "alfanumérico, mínimo 3 caracteres", # regla en input
             "minim"   : 3,                                   # min. chars
             "success" : "Ensamblado",                        # exito alta
             "repeat"  : repeat,                              # activa repetic
             "is_add"  : True,                                # repetir Q.
             "manager" : self._manager_components,
             "fail"    : "Agregue componentes"  }           
        
        #return super().add_entity(p)
        return super().manage_entity(p)  
    
    def select_device(self, pre_list):
        p = {"question": "Nombre/ID del equipo a modificar",
             "rule"    : "o 'L' para listar", 
             "minim"   : 3 }
        return super().select_entity(p, pre_list)
    
    def change_configuration(self, id):
        
        p = {"mode"    : "modify",
             "menu"    : self._menu_info,
             "manager" : self._manager_components,
             "device"  : self._entities_dic[id],
             "id"      : id, 
             "success" : "Configuración actualizada",
             "fail"    : "Agregue componentes"  }
        #super().update_entity_based_on_mode(p) 
        return super().manage_entity(p)  
    
    def remove_device(self, id):
        p = {"mode"     : "remove",
             "id"       : id,
             "manager"  : self._manager_components,
             "device"   : self._entities_dic[id],
             "action"   : "Equipo a desemsamblar",
             "question" : "Seguro de que desea dar de baja este Equipo",
             "success"  : "desemsamblado. Componentes devueltos a stock"}
        #return super().update_entity_based_on_mode(p)
        return super().manage_entity(p)  
    
    
        # device = self._entities_dic[device_id]
    
        # if Logger.there_is_the_question(
        #         "¿Está seguro de que desea desensamblar este equipo?"):
        #     for component_type, component in device._components.items():
        #         self._manager_components._entities_dic[component].increase_stock(1)
        #     Logger.success_pause("Equipo: ", device.display(),
        #                          " desensamblado y eliminado del sistema.", True)
        #     del self._entities_dic[device_id]
        #     return True
        # else:
        #     Logger.register_quit("Cancelado por usuario")
        #     return False        
    
    """  Función a llamar desde 'System' """
    def update(self):            
      
        atras = "Menú anterior"    
        while True:            
            self._menu_dev.set_max_options(super().dic_len_ctrl(1, 3))            
            self._menu_dev.display(zero = atras)  
            option = self._menu_dev.get_option()   
            
            if option == 1: self.add_device() # Alta de equipo
                
            elif option == 2 or option == 3:  # Sub Menú Modificación  
            
                id = self.select_device(False if option < 3 else True)                
                if not id: continue
                while True:                    
                    self._menu_modi.display(True, True, obj=id, zero= atras)
                    option = self._menu_modi.get_option()
                    
                    if option == 0:               # Salir de Menu modificación
                        Logger.scroll_screen()
                        break
                    elif option == 1:             # Cambiar configuración
                        self.change_configuration(id)
                        continue
                    elif option == 2:             # Eliminar equipo
                        if self.remove_device(id):
                            break
                        continue
                    else: Logger.bad_option()                    
                    
                    
            elif option == 0: break          # Salir de menu Equipos
            else: Logger.bad_option()        # Opción no encontrada       
    