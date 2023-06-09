# -*- coding: utf-8 -*-
"""
Proyecto: HardVIU
Created on Wed May  3 16:46:05 2023
@author: José Luis Rosa Maiques

Esta implementación sigue la misma estructura de la clase menu para los modelos 
La clase `MenuDistributors` hereda de `Controller` y utiliza el patrón Factory 
Method para instanciar un controlador específico para distribuidores.

La función `add_distributor` permite dar de alta a un distribuidor, mientras 
que las funciones `modify_info` y `remove_distributor` permiten modificar la 
información y eliminar un distribuidor del sistema, respectivamente.

La función `update` se encarga de mostrar las opciones disponibles en el menú 
de distribuidores y de gestionar la navegación entre las distintas opciones y 
submenús.

Aun hay que ajustar algunas partes del código para que se adapte completamente 
al proyecto, pero este ejemplo debería proporcionarte una base sólida para 
empezar a trabajar en la implementación del menú de distribuidores en el
sistema HardVIU.
"""

from core.views.drawer import MenuDrawer
from core.views.logger import Logger

from core.controllers.controller import Controller, ModelType, ModelFactory

class MenuDistributors(Controller):

    def __init__(self, menu_devices):
        
        # FACTORY method: Instancia del controlador con modelo "COMPONENT"
        super().__init__(ModelType.DISTRIBUTOR)
        
        # Controlador de equipos a controlador de distribuidores (ctrl equipos)
        device_controller = menu_devices.get_controller()        
        self._controller.link_device_controller(device_controller)   
        
        # Esta instancia es un poco rebuscada, pero 'DistributorController'
        # necesita de 'DispatchController' además de 'DeviceController'                
        dm = ModelType.DISPATCH
        dc = ModelFactory.create_controller(dm, self._controller._dispatch_dic)        
        self._controller.link_dispatch_controller(dc)
        

        # Menu principal. Mostramos al principio solo "Alta" ('max_options') 
        self._menu_distributor = MenuDrawer("HardVIU / 3) Distribuidores", [
            "Alta", "Modificar", "Listar Distribuidores"], max_options = 1)

        # Submenú nueva alta
        self._menu_add = MenuDrawer("HardVIU / 3) Distribuidores / 1) Alta")

        # Submenú modificación distribuidor
        self._menu_modi = MenuDrawer(
            "HardVIU / 3) Distribuidores / 2) Modificar", [
                "Cambiar información", "Dar de baja"])

        self._result = "dado de alta con éxito."
        
    def get_controller(self): return self._controller

    def add_distributor(self):  # Alta de distribuidor    
    
        self._id_config["question"] = "Nombre/ID de " + self._model._name
        self._id_config["rule"]     = "alfanumérico, mínimo 3 caracteres" 
        
        id = True
        o  = "Nuevo Distribuidor"            
        while True:                        
            self._menu_add.display(True, False, True, obj = '"' + str(o) + '"')             
            if id == True:
                id = super().get_and_check_id(mode = "add");
                if id is None: break
                elif id != True: o = id
                continue
            else:
                if super().new_model(id):                   
                    Logger.UI.success("Distribuidor", id, self._result,
                                      pause = False)                     
                    id = True
                    o  = "Nuevo Distribuidor"
                else: 
                    break            
                if not super().ask_this_question("Introducir otro Distribuidor"):                
                    break

    def select_distributor(self, pre_list):
        self._id_config["question"] = "Nombre/ID o número de la lista"
        self._id_config["rule"] = "'l' para listar"  
        
        if pre_list: super().list_models_from_dic()
        Logger.UI.cancel_info(level = 1)
        return super().select_model_from_dic()

    def modify_info(self, id):
        Logger.UI.cancel_info(n1 = '\n', level = 1)
        if super().modify_model_info(id):
            Logger.UI.success("Distribuidor", id, 
                              "ha sido modificado con éxito.")

    def remove_distributor(self, id):
        if self._controller.remove(id):
            Logger.UI.success("Distribuidor", id, 
                              "eliminado del sistema.")
            return True
        
    def menu_distributor(self):
        while True:
            numero_opciones_visibles = 1
            if len(self._dic.items()) > 0: numero_opciones_visibles = 3 
            self._menu_distributor.set_max_options(numero_opciones_visibles)
            self._menu_distributor.display(zero = "Menú anterior")
            option = self._menu_distributor.get_option()

            if option == 1: # Alta distribuidor
                self.add_distributor()  
            elif option == 2 or option == 3:  # Submenú Modificación            
                p_list = False if option < 3 else True
                id = self.select_distributor(pre_list = p_list)
                if not id: continue
                while True:                    
                    self._menu_modi.display(True, True, obj = '"' + id + '"', 
                                            zero = "Menú anterior")
                    option = self._menu_modi.get_option()
                    if option == 0:  # Salir de modificación
                        Logger.scroll_screen()
                        break
                    elif option == 1:  # Cambiar información
                        self.modify_info(id)
                        continue
                    elif option == 2:  # Dar de baja
                        if self.remove_distributor(id):
                            break
                        continue
                    else: Logger.UI.bad_option()
            elif option== 0:  # Salir del menú Distribuidores
                break
            else: Logger.UI.bad_option()
    
    def menu_dispatch(self):
        Logger.UI.emph("Menu Despachos")
        Logger.pause()
        
    def menu_days(self):
        Logger.UI.emph("Menu Días")
        Logger.pause()
        
    """  Función a llamar desde 'System' """
    def update(self, op):        
        if   op == 3: self.menu_distributor()
        elif op == 4: self.menu_dispatch()
        elif op == 5: self.menu_days()
        
