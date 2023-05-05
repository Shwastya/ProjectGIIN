# -*- coding: utf-8 -*-
"""
Proyecto: HardVIU
Created on Fri Mar 24 16:18:11 2023
@author: José Luis Rosa Maiques
    
La clase 'MenuComponents' es una subclase del modelo 'Component' que se utiliza
en la capa de vista del patrón MVC. Se instancia como subclase de la clase 
'Controller'. Es necesario especificar el tipo de modelo a la superclase 
'Controller', pasando como parámetro el tipo de modelo:
    
    super().__init__(ModelType.COMPONENT)
    
La superclase 'Controller' incluye métodos genéricos aplicables a todos los 
modelos. Además, emplea composición y el patrón Factory Method para instanciar 
un controlador específico para cada modelo. El diccionario para almacenar otros
diccionarios para los diferente modelos se encuentra siempre en la superclase 
'Controller'.
"""

from core.views.drawer import MenuDrawer
from core.views.logger import Logger

from core.controllers.controller import Controller, ModelType

class MenuDevices(Controller):

    def __init__(self, menu_components):       
        
        # FACTORY method: Instancia del controlador con modelo "DEVICE"
        super().__init__(ModelType.DEVICE)
        
        # Controlador de componentes al controlador de equipos (control stock).    
        component_controller = menu_components.get_controller()
        self._controller.link_component_controller(component_controller)       
       
        # Menu principal. Mostramos al principio solo "Alta" ('max_options') 
        self._menu_dev = MenuDrawer("HardVIU / 2) Equipos", [
            "Alta", "Modificar", "Listar Equipos"], max_options = 1)
    
        # Submenu nueva alta
        self._menu_add = MenuDrawer("HardVIU / 2) Equipos / 1) Alta")
    
        # Submenu modificación equipo
        self._menu_modi = MenuDrawer("HardVIU / 2) Equipos / 2) Modificación",[
                "Cambiar configuración", "Desensamblar"])   
        
        # Submenu cambiar información
        self._menu_info = MenuDrawer("HardVIU / 1) Equipos / 2) " + 
                                     "Modificar / 2) Cambiar configuración")
                       
        self._result = "Ensamblado con éxito."    
    
    def get_controller(self): return self._controller
    
    def add_device(self): # Alta de componente
        self._id_config["rule"] = "alfanumérico, mínimo 3 caracteres"        
        self._controller.set_add_or_modify_mode("add")               
        id = True
        o  = "Nuevo Equipo"               
        while True:                        
            self._menu_add.display(True, False, True, obj = '"' + str(o) + '"')             
            if id == True:
                id = super().get_and_check_id(mode = "add");
                if id is None: 
                    break
                elif id != True: o = id
                continue
            else:
                if super().new_model(id):                   
                    Logger.UI.success("Equipo", id, self._result,
                                      pause = False)                     
                    id = True
                    o  = "Nuevo Equipo"
                else: break            
                if not super().ask_this_question("Introducir otro componente"):                
                    break
                
    def select_device(self, pre_list):         
        self._id_config["rule"] = "o 'l' para listar"             
        if pre_list: super().list_models_from_dic()      
        Logger.UI.cancel_info()
        return super().select_model_from_dic()    
        
    def modify_info(self, id):            
        self._controller.set_add_or_modify_mode("modify")        
        Logger.UI.cancel_info()
        if super().modify_model_info(id):
            success = "Ensamblaje actualizado con éxito."
            Logger.UI.success("Equipo", id, success)  
        
    def remove_device(self, id):       
        if self._controller.remove(id):   
            success = "Desensamblado y eliminado del sistema."
            Logger.UI.success("Equipo", id, success)  
            return True            
            
    """  Función a llamar desde 'System' """
    def update(self):                   
        while True:                         
            numero_opciones_visibles = 1
            if len(self._dic.items()) > 0: numero_opciones_visibles = 3                  
            self._menu_dev.set_max_options(numero_opciones_visibles)            
            self._menu_dev.display(zero = "Menú anterior")            
            option = self._menu_dev.get_option()    
            
            if option == 1: # Alta componente                    
                self.add_device() 
            elif option == 2 or option == 3: # Sub Menú Modificación  
                p_list = False if option < 3 else True                           
                id = self.select_device(pre_list = p_list)                
                if not id: continue            
                while True:
                    self._menu_modi.display(True, True, obj = '"'+ id + '"',
                                            zero = "Menú anterior")
                    option = self._menu_modi.get_option()                    
                    if option == 0: # Salir de Menu modificación
                        Logger.scroll_screen()
                        break
                    elif option == 1: # Cambiar configuración
                        self.modify_info(id)
                        continue
                    elif option == 2: # Eliminar equipo
                        if self.remove_device(id):
                            break
                        continue
                    else: Logger.UI.bad_option()                   
            elif option == 0: break # Salir de menu Componentes
            else: Logger.UI.bad_option()
