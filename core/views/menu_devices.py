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
from core.models.device          import DeviceStatus

class MenuDevices(Controller):

    def __init__(self, menu_components):       
        
        # FACTORY method: Instancia del controlador con modelo "DEVICE"
        super().__init__(ModelType.DEVICE)
        
        # Controlador de componentes al controlador de equipos (control stock).    
        component_controller = menu_components.get_controller()
        self._controller.link_component_controller(component_controller)       
       
        # Menu principal. Mostramos al principio solo "Alta" ('max_options') 
        self._menu_dev = MenuDrawer("HardVIU / 2) Equipos", [
            "Alta", "Modificar", "Listar Disponibles"], max_options = 1)
    
        # Submenu nueva alta
        self._menu_add = MenuDrawer("HardVIU / 2) Equipos / 1) Alta")
    
        # Submenu modificación equipo
        self._menu_modi = MenuDrawer("HardVIU / 2) Equipos / 2) Modificación",[
                "Cambiar Configuración", "Desensamblar"])   
        
        # Submenu cambiar información
        self._menu_info = MenuDrawer("HardVIU / 1) Equipos / 2) " + 
                                     "Modificar / 2) Cambiar Configuración")
                       
        self._result = "ensamblado con éxito."    
    
    def get_controller(self): return self._controller
    
    def add_device(self): # Alta de componente
    
        self._id_config["question"] = "Nombre/ID de " + self._model._name
        self._id_config["rule"]     = "alfanumérico, mínimo 3 caracteres" 
        
     
        a="Se deja la compatibilidad entre componentes a criterio del usuario:"
        
        self._controller.set_add_or_modify_mode("add")               
        id = True
        o  = "Nuevo Equipo"               
        while True:         
            
            self._menu_add.display(True, False, True, obj = '"' + str(o) + '"')             
            if id == True:
                        
                id = super().get_and_check_id(mode="add", auxiliar_dic=None);
                if id is None: 
                    break
                elif id != True: 
                    
                    # Tenemos disponible este ID para dar de alto en el
                    # diccionario principal:
                    # Pero que pasa con los equipos que están en despacho?
                    
                    # Controlamos este caso pues: 
                    # if not self._controller.is_device_in_dispatched(id):
                    #     o = id
                    # else:                        
                    #     e = 'El ID "' + id + '" no está disponible, '
                    #     info1 = e + 'corresponde a un equipo en despacho.'
                    #     n = "El ID estará disponible una vez llegue a destino "
                    #     info3 = n + "(salvo en caso de devolución)."
                    #     Logger.UI.emph(info1)                        
                    #     Logger.UI.emph(info3)
                    #     Logger.pause()  
                        
                    #     id = True # Reniciamos el tema.
                    
                    o = id
                        
                continue
            else:
                Logger.UI.emph(a)       
                Logger.print_line(50, color = True)
                if super().new_model(id):                   
                    Logger.UI.success("Equipo", id, self._result,
                                      pause = False, newline = False)                     
                    id = True
                    o  = "Nuevo Equipo"
                else: break            
                if not super().ask_this_question("Ensamblar otro equipo"):                
                    break
        
    def modify_info(self, id):            
        self._controller.set_add_or_modify_mode("modify")        
        Logger.UI.cancel_info(level = 1)
        
        
        if super().modify_model_info(id):
            success = "modificado con éxito."
            Logger.UI.success("Equipo", id, success, newline = False)  
        
    def remove_device(self, id):
        Logger.Core.action("Equipo a desensamblar", id, pause = False)        
        question = "Seguro que desea eliminar este equipo del sistema"
        if self.ask_this_question(question): 
            if self._controller.remove(id):
                success = "desensamblado y eliminado del sistema"
                Logger.UI.success("Equipo", id, success)  
                return True
            
            
    """  Función a llamar desde 'System' """
    def update(self):                   
        while True:                         
            numero_opciones_visibles = 1               
            
            # Solo podemos modificar equipos NEW_DEVICE o RETURNED
            filtro   = [DeviceStatus.NEW_DEVICE, DeviceStatus.RETURNED]              
            # filtramos modelos con la función base 'controller'                
            dic = super().filter_models(self._dic, filtro) 
            
            if len(dic.items()) > 0: numero_opciones_visibles = 3     
             
            self._menu_dev.set_max_options(numero_opciones_visibles)            
            self._menu_dev.display(zero = "Menú anterior")            
            option = self._menu_dev.get_option()             
            
            if option == 1: # Alta componente                    
                self.add_device() 
                
            # Sub Menú Modificación              
            elif (option == 2 or option == 3) and numero_opciones_visibles > 1:                               
                
                p_list = False if option < 3 else True   
                d_list = "Nuevos; Devueltos"
                args = [dic, "Equipo", p_list, True, d_list] 
                
                Logger.UI.emph("Equipos disponibles para modificación.")
                Logger.print_line(50, color = True)
                id, user_cancel = super().select_model(*args)                
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
