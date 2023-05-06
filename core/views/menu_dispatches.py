# -*- coding: utf-8 -*-
"""
Created on Thu May  4 19:12:46 2023

@author: Jose
"""

from core.views.drawer import MenuDrawer
from core.views.logger import Logger

from core.controllers.controller import Controller, ModelType

class MenuDispatches(Controller):

    def __init__(self, menu_distributors):

        # FACTORY method: Instancia del controlador con modelo "DISPATCH"
        super().__init__(ModelType.DISPATCH)

        # Controlador de dispositivos al controlador de envíos.
        distributor_controller = menu_distributors.get_controller()
        self._controller.link_distributor_controller(distributor_controller)

        # Menú único de despachos        
        self._menu_disp = MenuDrawer(4*" " + "HardVIU / 4) Despachar" + 4*" ")
        
        self._result = "asignado con éxito."
        
    def add_dispatch(self): # Nuevo despacho
        
        # reglas (mensajes) especifico para este caso
        self._id_config["question"] = "Seleccione un distribuidor"
        self._id_config["rule"]     = "alfanumérico único"        
        
        # solo hay opción a añadir distribuidores no necesitamos especificar 
        # si es "add" o "modify"
        
        # self._controller.set_add_or_modify_mode("add")               
        id = True
        o  = "Nuevo Despacho"               
        while True:                        
            self._menu_disp.display(True, False, True, obj = '"' + str(o) + '"')             
            if id == True:
                aux = self._controller._distributor_controller.get_dic()
                id = super().get_and_check_id(auxiliar_dic = aux);
                if id is None:
                    break
                elif id != True: o = id
                continue
            else:
                if super().new_model(id):                   
                    Logger.UI.success("Despacho", id, self._result,
                                      pause = False)                     
                    id = True
                    o  = "Nuevo Despacho"
                else: break            
                # No se quiere la opción de dar de alta a distribuidor
                # if not super().ask_this_question("Introducir otro componente"):                
                break
        
    def update(self): self.add_dispatch()
            
            
            