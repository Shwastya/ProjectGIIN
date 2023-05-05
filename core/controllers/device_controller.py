# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 22:28:07 2023

@author: Jose
"""

from core.controllers.inputs import InputUser
from core.models.component   import ComponentType
from core.views.logger       import Logger

class DeviceController:
    def __init__(self, device_dic):
        
        self._device_dic = device_dic   
        self._mode = "add" # Da igual el modo de inicio, se modifica         
        
        # Este "Controller" necesita acceso al 'ComponentController'
        self._component_controller = None           
    
    def link_component_controller(self, component_controller):
        self._component_controller = component_controller
        
    def set_add_or_modify_mode(self, mode): self._mode = mode
    
    def get_model_data_from_user(self, id):
        """        
        IMPORTANTE:
        Todos los controllers de los modelos deben implementar esta función
        Que debe estar en consonancia con la estructura del modelo.
        
        En este caso se está usando la función tanto para ensamblar equipos
        como para desensamblarlos.
        
        Teniendo en cuenta que tenemos acceso al controlador 'Components'.
        Que hay que controlar el 'stock'. Que hago todo tipo de controles.
        Aun usando como ayuda el 'InputUser' la función me queda demasiado
        compleja. Como ejercicio antes del examen estaría bien refactorizarlo.
        
        Esta función devuelve una tupla para guardar mediante método del model.
        """   
        # Accedemos al diccionario directamente desde el  controlador
        comp_dic = self._component_controller.get_dic()  
        
        cancel="Registro cancelado..."
        warn="Agregue los componentes necesarios desde el menú de Componentes."
        
        if len(comp_dic) == 0:           
            error = "¡Stock de componentes vacío! " + cancel           
            Logger.Core.error_warn_pause(error, warn)
            return False
    
        device_components = {}
        
        # Lista temporal para almacenar componentes desmontados
        # en caso de que el modo esté en "modify"
        disassembled_components = []  
        
        # recorremos lista de componentes basandonos en el enum de 'Component'
        for component_type in ComponentType: 
            
            c_t = component_type.value
            if self._mode == "modify" and component_type in self._device_dic[id]._components:
                
                # Guardamos en una lista temporal los componentes a desmontar
                device = self._device_dic[id]
                old_comp_id = device._components[component_type]["id"]
                disassembled_components.append(old_comp_id) 
                
                # Mensaje de sustitución
                o_c = old_comp_id
                Logger.Core.action("Cambiar (" + c_t +")", o_c, "por:",
                                   newline = False, pause = False)
    
            disp_components = []
            for comp_id, comp in comp_dic.items():
                if comp._tipo == component_type and comp._cantidad > 0:
                    disp_components.append((comp_id, comp))
    
            if not disp_components:                
                tipo  = component_type.value                
                error = "No se dispone de Componentes (" + tipo + "). " 
                Logger.Core.error_warn_pause(error + cancel, warn)
                return False            
            
            print("Componentes disponibles de tipo " + c_t + ":")
            for index, (comp_id,component) in enumerate(
                    disp_components,start=1):                
               
                print("\t" + str(index) + ". ", end="", sep="") 
                component.display(comp_id, col = True)
                
            
            # (InputUser) functions
            # Recopila las entradas del usuario para escoger un componente.
            # Permite entrar número del enumerado o ID
            question = "Seleccione " + c_t + " (ingresa número o el ID): "
            selected_comp_id, selected_comp = InputUser.get_valid_component(
                question, disp_components)

            # Cancelación del usario
            if selected_comp_id is None and selected_comp is None: return        
            
            # Crear un diccionario solo con la información necesaria
            compact_component = {"id"    : selected_comp_id,
                                 "peso"  : selected_comp._peso,
                                 "precio": selected_comp._precio}
    
            # Guardar el diccionario compacto en device_components
            device_components[component_type] = compact_component            
    
            # Mensaje de ensamblado
            e = 'Ensamblando en equipo "'
            c = '"'+ selected_comp_id +'"'            
            Logger.low_info(e +  id + '": (' + c_t + ') ' + c)            

    
        """ Aquí usamos el controlador de componentes """ # modify
        # Agregamos los componentes desmontados al stock solo después de 
        # seleccionar todos los componentes nuevos.        
        if self._mode == "modify":
            Logger.Core.info("Devolviendo componentes desmontados al stock.")
            self._component_controller.update_stock_by_component_list(
                disassembled_components, 1)            
        
        """ Aquí usamos el controlador de componentes """ # add
        # Actualizamos el stock una vez que se hayan seleccionado todos 
        # los componentes correctamente
        for component_type, compact_component in device_components.items():
            self._component_controller.update_stock_by_component_list(
                [compact_component["id"]], -1)
        
        return device_components
        
  
    def remove(self, id):       
        """
        Para todos los métodos de los 'controllers' especificos, la función 
        debe tener el mismo nombre.
        """
        Logger.Core.action("Equipo a desensamblar", id, pause = False)         
        question = "¿Seguro que desea eliminar este equipo del sistema?"        
        if InputUser.ask_yes_no_question("\n" + question):   
            c_list = self._device_dic[id].get_components_list()
            self._component_controller.update_stock_by_component_list(c_list,1)           
            del self._device_dic[id]          
            return True
        else: 
            return False
       
    