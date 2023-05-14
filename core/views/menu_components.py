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

class MenuComponents(Controller):

    def __init__(self):       
        
        # FACTORY method: Instancia del controlador con modelo "COMPONENT"
        super().__init__(ModelType.COMPONENT)

        # Menu principal. Mostramos al principio solo "Alta" ('max_options') 
        self._menu_comp = MenuDrawer("HardVIU / 1) Componentes", [
            "Alta", "Modificar", "Listar Componentes"], max_options = 1)

        # Submenu nueva alta
        self._menu_add = MenuDrawer("HardVIU / 1) Componentes / 1) Alta")

        # Submenu modificación componente
        self._menu_modi = MenuDrawer(
            "HardVIU / 1) Componentes / 2) Modificar", [
                "Cambiar Stock", "Cambiar Información", "Eliminar"])

        # Submenu cambiar información
        self._menu_info = MenuDrawer("HardVIU / 1) Componentes / 2) " + 
                                     "Modificar / 2) Cambiar Información") 
                       
        self._result = "dado de alta con éxito."        
    
    def get_controller(self): return self._controller
    
    def add_component(self): # Alta de componente        
    
        self._id_config["question"] = "Nombre/ID de " + self._model._name
        self._id_config["rule"    ] = "alfanumérico, mínimo 3 caracteres"         
        
        id = True
        o  = "Nuevo Componente"  
             
        while True:                        
            self._menu_add.display(True, False, True, obj = '"' + str(o) + '"')             
            if id == True:
                id = super().get_and_check_id(mode = "add", auxiliar_dic=None);
                if id is None: break
                elif id != True: o = id
                continue
            else:
                if super().new_model(id):                   
                    Logger.UI.success("Componente",id,self._result,pause=False)      
                    id = True
                    o  = "Nuevo Componente"
                else: break            
                if not super().ask_this_question("Introducir otro componente"):                
                    break
    
    def modify_stock(self, id):
        Logger.UI.cancel_info(level = 1)        
        if self._controller.get_new_stock_from_user(id):        
            success = "stock actualizado."
            Logger.UI.success("Componente", id, success)  
        
    def modify_info(self, id):        
        Logger.UI.cancel_info(level = 1)
        if super().modify_model_info(id):
            success = "modificado con éxito."
            Logger.UI.success("Componente", id, success)  
        
    def remove_component(self, id): 
        
        Logger.UI.success("Componente", id, 'seleccionado para su eliminación.', 
                          pause   = False)  
        
        question = "Seguro que desea eliminar este componente del sistema"
        if self.ask_this_question(question):  
            if self._controller.remove(id):
                success = "eliminado del sistema."
                Logger.UI.success("Componente", id, success)  
                return True
            
            
    """  Función a llamar desde 'System' """
    def update(self):                  
        while True:                         
            numero_opciones_visibles = 1
            if len(self._dic.items()) > 0: numero_opciones_visibles = 3            
            self._menu_comp.set_max_options(numero_opciones_visibles)            
            self._menu_comp.display(zero = "Menú anterior")                        
            option = self._menu_comp.get_option()     
            
            if option == 1: # Alta componente                
                self.add_component()
                
            # Sub Menú Modificación 
            elif (option == 2 or option == 3) and numero_opciones_visibles > 1:                 
                
                p_list = False if option < 3 else True
                args = [self._dic, "Componente", p_list, True]
                id, user_cancel = super().select_model(*args)                
                if not id: continue            
            
                while True:                                       
                    self._menu_modi.display(True, True, obj = '"'+ id + '"',
                                            zero = "Menú anterior")
                    option = self._menu_modi.get_option()                       
                    
                    if option == 0: # Salir de modificación
                        Logger.scroll_screen()
                        break                    
                    elif option == 1: # Cambiar stock            
                        self.modify_stock(id)
                        continue                    
                    elif option == 2: # Cambiar información
                        self.modify_info(id)
                        continue
                    elif option == 3: # Dar de baja                    
                        if self.remove_component(id): break
                        continue
                    else: Logger.UI.bad_option()               
            elif option == 0: break # Salir de menu Componentes
            else: Logger.UI.bad_option()           
                
