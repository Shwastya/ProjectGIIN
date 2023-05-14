# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 22:28:07 2023

@author: Jose
"""

from core.controllers.inputs import InputUser
from core.models.component   import ComponentType
from core.views.logger       import Logger

class DeviceController:
    """
    Fábrica de equipos.
    """
    def __init__(self, device_dic):
        
        self._device_dic = device_dic   
        self._mode = "add" # Da igual el modo de inicio, se modifica         
        
        # "DeviceController" necesita acceso al 'ComponentController'
        self._component_controller = None    
        
        # A ver (esto es una idea), los equipo que se despechan a un 
        # distribuidor guardaremos aquí por. Si por algún motivo se devolvieran
        # como los 'controllers' Dispatch y Distributor tienen acceso a este
        # 'controller', podremos devolver el equipo a fábrica facilmente.
        self._device_dispatched = {}
        
    """
    Las siguientes funciones se pretende que sean privadas (similar a C++).
    Se añade '__' al principio de cada función como convención.
    Las funciones privadas son solo para el uso auxiliar de esta clase.
    """    
    
    def __available_components(self, component_type):        
        """
        Devuelve una lista con los componentes disponibles en el diccionario,
        de componentes, se le pasa como parametro 'component_type' que es el
        tipo de componente que se busca (en cada llamada se busca un tipo)        
        """        
        # Diccionario sacado directamente del controlador de Componentes
        # Tenemos acceso a él en este controlador (controlador de Equipos)  
            
        # 1. Debe de existir en el sistema
        # 2. El stock debe ser mayor a 0 
        
        available_components = []
        for comp_id, comp in self._component_controller.get_dic().items():
            if comp._tipo == component_type and comp._cantidad > 0:
                available_components.append((comp_id, comp))
        
        return available_components
            
    def __check_if_available_list_is_empty(self, available_components, tipo):
        """
        La lista obtenida de la función anterior, se comprueba si esta llena
        o vacia (para seguir con el registro o cancelar)
        Esta función podría ser util para cualquier lista en realidad, pero
        se pretende ser especifico en la definición de esta clase.
        
        TODO: De todas formas estamos metiendo mensajes en el controlador
        los mensajes debería ser más parte de la 'view'
        """        
        if not available_components:                                   
            Logger.Core.error_warn_pause(
                "Stock vacio para el Componente (" + tipo + "). ", 
                "Agregue más componentes desde el menú de Componentes.")
            return False
        return True
        
    def __user_choose_component(self, available_components, tipo):
        """
        Recopila las entradas del usuario para escoger un componente.
        (Permite entrar número del enumerado o ID):
            
            . En caso de cancelación del usuario esta función devolverá False.
            . En caso de exito, devolverá el Componente compactado para equipo.
        """        
        # (InputUser) functions          
        question = "Seleccione " + tipo
        rule     = "(ingresa número o el ID) = "
        
        # En la siguiente función el usuario no necesita pedir lista, pero
        # tenemos que recogerlo en la variable l aunque no la usemos.
        selected_comp_id, selected_comp, l = InputUser.get_valid_model(
            question, rule, available_components, has_shown_list = True)
        
        # Cancelación del usario
        if selected_comp_id is None and selected_comp is None: return False
        
        # No se ha cancelado, se devuelven los valores. Un diccionario del        
        compact_comp = self.__pack_component(selected_comp, selected_comp_id)
        return compact_comp
        
        
    def __pack_component(self, component, comp_id):
        """
        Toma un componente y su ID y devuelve un Dic. compacto del componente. 
        De momento hace uso de esta funció solo la función anterior. 
        Pero queda más separado para posibles modificaciones.
        
        Compactar un componente es para considerar solo la información
        necesaria para los componentes en Equipos (Devices).
        """
        return {"id"     : comp_id,
                "peso"   : component._peso,
                "precio" : component._precio}
        
    def __unpack_component(self, device_components):
        """
        Toma un diccionario de componentes compactos y devuelve un Dic con el 
        componente desempaquetado en component_data.
        """
        data = {}
        for component_type, compact_component in device_components.items():
            data[compact_component["id"]] = (component_type,
                                             compact_component["peso"],
                                             compact_component["precio"],)
        return data
            
    def __update_component_stock(self, component_data, operation
                                 , info = "Tomando componentes del stock ..."):
        """
        Realmente esta función ya tiene suficiente abstracción para separarlo
        como función auxiliar, pero ya que son 3 lineas de código y lo usamos
        en distintas funciones, no está de menos crear esta función auxiliar.
        """
        Logger.Core.info(info)
        self._component_controller.update_stock_by_component_list(
            operation, component_data)
        Logger.Core.info("Stock actualizado.", n = True)
        
        
    def __check_initial_conditions(self):
        
        # Si Dic. está vacío: informa y devuelve False. Se cancela el alta.        
        if not self._component_controller.there_are_components_in_system():
            Logger.Core.info("No hay componentes en el sistema.")
            return False
    
        # Hay al menos un componente, revisamos si hay suficientes componentes
        # de cara tipo para ensamblar al menos un equipo.         
        if not self._component_controller.check_at_least_one_of_each_type():
            
            i ="No hay suficientes componentes para ensamblar un equipo."
            w ="El registro se cancelará cuando no se encuentre un componente."
            
            Logger.Core.info(i)
            Logger.Core.warn(w)
            
            q = "¿Desea seguir con el 'alta' hasta que lo cancele el sistema?"
            
            # Aquí se le pregunta al usuario. De nuevo, estamos asignando mal
            # las responsabilidades,pero de otra manera se convierte en locura.
            if not InputUser.ask_yes_no_question(q): return False    
        return True    
        
    def __display_available_components(self, available_components):
        for index, (comp_id, component) in enumerate(available_components, 
                                                     start = 1):
            print("\t" + str(index) + ". ", end = "", sep="")
            component.display(comp_id, col=True, idx = 0)
    
    """
    Las siguientes funciones son las funciones públicas        
    """  
    
    def get_dic(self):
        return self._device_dic
    
    def get_dispatched_devices_dic(self):
        return self._device_dispatched 
        
        
    def link_component_controller(self, component_controller):
        self._component_controller = component_controller
        
    def set_add_or_modify_mode(self, mode): 
        self._mode = mode            
    
    # ADD -DEVICES-
    def get_model_data_from_user(self, id):         
        
        
        # Condiciones iniciales (definido en función auxiliar)
        if not self.__check_initial_conditions(): return False           
        
        device_components = {}
        
        # recorremos lista de componentes basandonos en el enum de 'Component'
        for component_type in ComponentType:            
            
            tipo = component_type.value # el valor del tipo de componente
            
            # Usamos función auxiliar para obtener los componentes disponibles            
            available_c = self.__available_components(component_type)           
            
            # Si no se ha creado una lista temporal es que no existe
            # ningún componente para poder continuar (Error and return False)            
            check = self.__check_if_available_list_is_empty(available_c, tipo)                                                    
            if not check: return False            
            
            # En el caso de que no haya habido ningún error al crear la lista
            # temporal. Mostramos los componenetes disponibles (enumerados)
            self.__display_available_components(available_c)
                
            # Recopila las entradas del usuario para escoger un componente.
            # Devuelve un componente compacto (para device) en modo Dic.
            compact_component = self.__user_choose_component(available_c, tipo)
            if not compact_component: return 
            
            # Guardar el diccionario compacto en device_components
            device_components[component_type] = compact_component            
    
            # Mensaje de ensamblado
            # 'Equipo "' + 
            c = '"' + compact_component['id'] + '"'   
            info = '("' + id + '") <── (' + tipo + ': ' + c + ')'
            Logger.Core.info(info, n = True)               
    
        #.... Actualización del stock de componentes        
        component_data = self.__unpack_component(device_components)            
        self.__update_component_stock(component_data, -1)        
        Logger.Core.info('Ensamblando equipo "' + id + '" ...' , n = '\n' ) 
        return device_components        
  
    # MODIFY -DEVICES-
    def set_modify_data_from_user(self, id):
        
        # Verificación de la existencia del equipo en el diccionario.
        # Aunque venimos de seleccionar ese ID del Dic. Este control
        # podría ser innecesario (pero por máxima prevención)
        id_ = '"' + id + '"'
        if id not in self._device_dic:
            Logger.Core.error('El equipo con ID ' + id_ + '" no existe.')
            return False        
        
        # Diccionarios (temporales) para componentes actualizados,
        # componentes a actualizar y componentes modificados.
        updated_device_components = {}
        components_to_update      = {}
        modified_components       = {}
        
        components = self._device_dic[id]._components
        
        is_modified = False
        
        # Iteramos sobre todos los componentes del equipo
        for component_type, current in components.items():
            tipo = component_type.value
    
            # Info antes de pregunta
            c = '"' + current["id"] + '"'   
            info = '("' + id + '") ──> (' + tipo + ': ' + c + ')'
            Logger.Core.info(info)
            
            # Se le pregunta al usuario si quiere modificar cada componente
            c_tipo_question = tipo + " (ID: " + current["id"] + ")?"
            question = "¿Desea cambiar " + c_tipo_question

            if not InputUser.ask_yes_no_question(question):
                updated_device_components[component_type] = current
                continue
            else: is_modified = True
    
            # Obtenemos los componentes disponibles para escoger
            available_c = self.__available_components(component_type)    
            check = self.__check_if_available_list_is_empty(available_c, tipo)
            if not check: continue    
    
            # Display de los componentes disponibles
            self.__display_available_components(available_c)
    
            compact_component = self.__user_choose_component(available_c, tipo)
            if not compact_component: return False
    
            updated_device_components[component_type] = compact_component
            
            # Agregamos el componente modificado
            modified_components[component_type] = compact_component  
    
            # Info después de añadir el componente
            c = '"' + compact_component['id'] + '"'   
            info = '("' + id + '") <── (' + tipo + ': ' + c + ')'
            Logger.Core.info(info, n = True)
            
            # Compactamos componentes que son para actualizar el stock
            # La funcionalidad del stock 
            components_to_update[current["id"]] = (component_type, 
                                                   current["peso"], 
                                                   current["precio"])
    
        # Actualizamos el stock de componentes en dos pasos:
            # 1. Componentes que devolvemos al Stock
            # 2. Componentes nuevos que hemos selccionado
        if components_to_update:
            info = "Devolviendo componentes desmontados al stock ..."
            self.__update_component_stock(components_to_update, 1, info)
    
            component_data = self.__unpack_component(modified_components)
            self.__update_component_stock(component_data, -1)
    
        
        if is_modified:            
            Logger.Core.info("Reconfigurando equipo '" + id + "' ...", n =True)
        else:
            Logger.Core.info("No se realizaron modificaciones en el equipo '" 
                             + id + "'.", n = True)
            Logger.pause()
            return False
        
        # Devolvemos el resultado al controlador principal
        # (y de ahí a la clase 'view' de este modelo)
        return updated_device_components        
        
    def remove(self, id):
        """
        TODO: Empezamos a realizar cierta parte de la separación de
        responsabilidades
        """
        c_data = self.__unpack_component(self._device_dic[id]._components)
        
        info = "Devolviendo componentes desmontados al stock ..."
        self.__update_component_stock(c_data, 1, info)
        
        
        Logger.Core.info("Eliminando registro de equipo " + '"' + id + '" ...')
        del self._device_dic[id]          
        Logger.Core.info("Equipo " + '"' + id + '" eliminado.', n = True)
        return True


    """
    Las siguientes funciones. Si creamos un despacho, he creido oportuno llevar
    aquí el control de equipos despachados
    """
    def dispatch_device_to_distributor(self, id): # device_id
        """
        Despacha un dispositivo a un distribuidor, moviéndolo del
        diccionario principal a self._device_dispatched.        
        """
        id_  = '(Equipo: "' + id + '")'
        info = 'Extrayendo de Fábrica ' + id_ + ' ...'
        Logger.Core.info(info)
        
        if id in self._device_dic:
            device = self._device_dic[id]
            self._device_dispatched[id] = device
            del self._device_dic[id]            
            
            Logger.Core.info('Se ha enviado al distribuidor ' + id_, n = True)
        else:
            # Este error nunca debería ocurrir
            Logger.Core.error('No existe en fábrica: ' + id_, n = True)

    def return_device_from_distributor(self, id): # device_id
        """
        Devuelve un dispositivo desde un distribuidor, moviéndolo desde
        self._device_dispatched al diccionario principal.
        """
        id_  = 'Equipo: "' + id + '"'
        info = 'Devolviendo ' + id_ + ' a fábrica ...'
        Logger.Core.info(info)
        
        if id in self._device_dispatched:
            device = self._device_dispatched[id]
            self._device_dic[id] = device
            del self._device_dispatched[id]
            
            Logger.Core.info(id_+ ' ha sido devuelto del distribuidor.')
        else:
            Logger.Core.error(id_+ ' no existe como dispositivo despachado.')
    
    def remove_dispatched_device(self, id):
       """
       Elimina un dispositivo del diccionario de dispositivos despachados.
       Esta función es útil cuando un dispositivo ha sido entregado, por lo 
       tanto, ya no se encuentra en el control de la empresa.
       """
       id_  ='Equipo: "' + id + '"'
       info ='Eliminando' + id_ + 'del registro de dispositivos despachados ...'
       Logger.Core.info(info)
       
       if id in self._device_dispatched:
           del self._device_dispatched[id]
           i =' ha sido eliminado del registro de dispositivos despachados.\n'
           Logger.Core.info(id_ + i)
       else:
           Logger.Core.error(id_
                             + ' no existe como dispositivo despachado.\n')

    def is_device_in_dispatched(self, id):
        """
        Comprueba si un dispositivo está en el diccionario de dispositivos 
        despachados. Esta función es útil para verificar si un dispositivo 
        específico se encuentra actualmente en tránsito o ya ha sido entregado 
        al distribuidor.
        """
        result = id in self._device_dispatched
        if result: Logger.Core.info('"' + id + '" está en lista-despacho.')
        return result
    
    
    def remove_device_in_dispatched(self, id):
        
        if self.is_device_in_dispatched(id):
            Logger.Core.info('Eliminando de equipos en despacho "' + id + '"')
            del self._device_dispatched[id]
            Logger.Core.info('ID: "' + id + '" ahora disponible para nuevas altas.')
    
    
    
    
    
    