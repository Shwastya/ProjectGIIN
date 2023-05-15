# -*- coding: utf-8 -*-
"""
Created on Thu May  4 22:23:14 2023

@author: Jose
"""


from core.controllers.inputs import InputUser
from core.views.logger       import Logger

from core.models.dispatch    import DispatchStatus

class DispatcherController:
    def __init__(self, dispatcher_dic):        
        """
        Ojo con esto! si se cargan los datos desde archivo, habrá que averiguar
        el ultimo número de Despacho para '_index'
        """
        self._dispatcher_dic = dispatcher_dic
        self._index = self.update_index() # Usaremos indice incrementable         
        
        # Este "Controller" necesita acceso al 'DistributorController'
        self._distributor_controller = None              
        
    def update_index(self):
        """
        Para el diccionario de 'Despachos' he decidido asignar un 
        autoincrementable. Teniendo en cuenta que la información puede cambiar
        (por ejemplo, al cargar un archivo nuevo con datos nuevos o vacios).
        Se decide implementar esta función, la cual busca siempre en el Dic.
        el posible indice más alto cada vez que se asigna un despacho. Esto 
        garantiza que siempre se utilice el valor máximo del índice existente
        en el diccionario antes de agregar un nuevo elemento.
        
        NOTA: Por temas relacionados con selección de IDs por el usuario, se
        cambia el ID númerico por un string. En este caso, se utiliza una 
        función lambda para dividir cada clave del diccionario en la parte del 
        número y la del dispositivo, y luego se extrae solo la parte del 
        número (sin la letra "D"). El resultado se convierte a entero y se 
        pasa a la función max para obtener el valor máximo entre todos los 
        índices. Luego, se suma 1 al valor máximo para obtener el siguiente 
        índice.        
        """
        if not self._dispatcher_dic: return 1
        max_key = max(map(lambda key: int(key.split('_')[0][1:]), 
                          self._dispatcher_dic.keys()))
        return max_key + 1
        
    def link_distributor_controller(self, distributor_controller):
        self._distributor_controller = distributor_controller
        
        
    def get_dic(self):
        return self._dispatcher_dic   
 
        
        
    def new_dispatch(self, dispatch, id_distributor, id_device):       
        
        # Incrementamos contador para el proximo despacho
        self._index = self.update_index()    
        
        # Generamos id despacho (la key incrementable + id_device)
        
        dispatch_id = "D" + str(self._index)  + "_" + id_device                 
        
        # Accedemos al 'controller' de equipos (extraer de frábica)        
        device_ctrl = self._distributor_controller.get_device_controller()
        device_ctrl.dispatch_device_to_distributor(id_device)
        
        # Asignando distribuidor y equipo a despacho
   
        d = 'Despacho: "' + dispatch_id + '"'
        Logger.Core.info("Generando " + d + " ...")    
        dispatch.set_dispatch(id_distributor, id_device)
                          
        Logger.Core.info(d +' <── '+'(Distribuidor: "'+ id_distributor +'")')
        Logger.Core.info(d +' <── '+'(Equipo: "'      + id_device      +'")')
        
       
        # Consultamos el tiempo de entrega del distribuidor
        
        Logger.Core.info("Consultando tiempo de entrega distribuidor: " 
                         + '"' + id_distributor + '" ...')
        
        distributor_dic = self._distributor_controller.get_dic()
        
        delivery_days = distributor_dic[id_distributor].get_delivery_time()
        
        dispatch.set_delivery_days(delivery_days)
        dias = str(delivery_days)
        Logger.Core.info(d +' <── '+'(Tiempo estimado de entrega: ' 
                         + dias +' días.)')  
        
        self._dispatcher_dic[dispatch_id] = dispatch        
        Logger.Core.info(d + ' asignado. [Pendiente de envio].', n = True)
        return self._index
         
 
    
    def advance_days(self, dispatch_id):
        """
        Este método actualiza el tiempo restante de entrega para el despacho
        especificado en el diccionario. Si el dispositivo ha sido entregado 
        (tiempo restante de entrega alcanza 0), notifica al usuario y guarda el 
        dispositivo en el historial de entregas.
        
        Devuelve:
            
            - False -> No se encuentra ID o el usuario ha cancelado
            - None  -> Fallo en la entrada (continue iteración)
            - remaining_days -> Días faltantes
            
        """
        if dispatch_id not in self._dispatcher_dic:
            Logger.Core.error('No se encontró despacho con ID "' 
                              + dispatch_id + '".')
            return False

        # Cogemos el despacho
        dispatch = self._dispatcher_dic[dispatch_id]
        distri_days = dispatch._delivery_days  
        max_days    = dispatch._remaining_days
        
        n_to_s = str(distri_days)        
        Logger.Core.info("Tiempo de entrega del distribuidor: (" 
                         + n_to_s +" días).")
        
        n_to_s = str((distri_days - max_days))        
        Logger.Core.info("Tiempo transcurrido: (" + n_to_s +" días).")
        
        n_to_s = str(max_days)        
        Logger.Core.info("Tiempo estimado de entrega: (" + n_to_s + " días)."
                         , n = True)        
 
        question = "Ingrese la cantidad de días a transcurrir (mínimo 1) = "
        days = InputUser.get_uint(question, max_days)
        
        if days is None: return False, None

        if days < 1 or days > max_days:
            warn = "La cantidad de días debe ser un entero mayor a 0"
            Logger.Core.warn(warn + " y menor o igual a " + max_days + ".")
            
            return None, None # Cuando None (continue en View)

        previous_status = dispatch.get_status()
        dispatch.update_remaining_days(days)
        current_status = dispatch.get_status()
        
        delivered = DispatchStatus.DELIVERED
        
        # Estos controles no son precisos ya que solo quiero pasar IDs de 
        # Despachos 'Not Delivered'. (Pero no está de menos)
        
        if previous_status != delivered and current_status == delivered:
            distributor_id = dispatch._distributor_id
            device_id = dispatch._device_id
            
            i1 = 'Distribuidor: "' + distributor_id + '" '
            i2 = 'ha recibido Equipo: "' + device_id + '"'            
            Logger.Core.info(i1 + i2)

            # Si el distribuidor ha recibido el equipo, mmm... a ver...
                
            # - DeviceController (quitar de lista de despachados)
            device_ctrl = self._distributor_controller.get_device_controller()
            
            Logger.Core.info("Informando a fábrica de la recepción ..."
                             , n = True)            
            
            device_ctrl.remove_dispatched_device(device_id)

        # Devuelve siempre los días restantes para la entrega
        return True, dispatch._remaining_days
            
            
            
    def get_devices_by_distributor(self, id, status_filter = None):
        """
        Este método toma el distributor_id como argumento y recorre el 
        diccionario de despachos (self._dispatcher_dic). Si encuentra un 
        despacho que tiene el distributor_id, agrega el ID del dispositivo 
        asociado a la lista devices si el estado del despacho está en la 
        lista status_filter.
    
        Si status_filter es None, se devolverán todos los dispositivos y 
        despachos asociados al distribuidor sin importar su estado.
        """
        has_dispatch = False
        
        Logger.Core.info('Accediendo al historial de despachos para "'
                         + id + '" ...', n = '\n')
        
        devices_and_dispatches = []
        
        # Crear un mensaje con los filtros utilizados
        filter_msg = "Filtros aplicados: "
        
        if status_filter is None: filter_msg += "Todos los estados"
        else:
            filter_msg += ", ".join([status.name for status in status_filter])
    
        # Mostrar el mensaje con los filtros
        Logger.Core.info(filter_msg)       
    
        # Recorremos todos los despachos 
        for dispatch in self._dispatcher_dic.values():
    
            # Se ha encontrado despacho asociado al distribuidor
            found = dispatch._distributor_id == id
            device_id = dispatch._device_id
    
            e = 'Equipo: "' + device_id + '"'
    
            if found and (status_filter is None or dispatch.get_status()
                          in status_filter):
    
                has_dispatch = True
    
                Logger.Core.info(e + " en despacho." 
                                 + " Pasa a la lista de 'observación'.")
                devices_and_dispatches.append((device_id, dispatch))
    
        if not has_dispatch:
            Logger.Core.info("No hay despachos (bajo filtro).")
    
        return devices_and_dispatches

   
    # Es una llamada generica desde controller base, solo quien quiera 
    # usarla la implementará    
    def check_id_status_from_controller(self, id):
        pass