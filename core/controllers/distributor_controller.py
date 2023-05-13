# -*- coding: utf-8 -*-
"""
Created on Wed May  3 17:01:27 2023

@author: Jose

La clase DistributorController define funciones similares a las de 
ComponentController y DeviceController. La función get_model_data_from_user 
recopila los datos del usuario para crear o modificar un distribuidor, mientras
que la función remove se encarga de eliminar un distribuidor del sistema. 
También se proporciona una función get_dic para acceder al diccionario de 
distribuidores.

Esta implementación básica debería servir como punto de partida para trabajar 
en el controlador de distribuidores en tu sistema HardVIU. Es posible que necesites ajustar algunas partes del código para que se adapte completamente a tu proyecto.
"""

from core.controllers.inputs import InputUser
from core.views.logger       import Logger

from core.models.dispatch    import DispatchStatus

class DistributorController:
    def __init__(self, distributor_dic):
        
        self._distributor_dic = distributor_dic       
        
        # se pasará a traves de menu_distributor al 'DispatchController'
        self._dispatch_dic    = {} 
        
        # Este "Controller" necesita acceso al 'DeviceController'
        self._device_controller   = None       
        # Este "Controller" necesita acceso al 'DispatcherController'        
        self._dispatch_controller = None  
        
        self._address_config = {"question": "Dirección del distribuidor",
                                "rule"    : "máximo 100 caracteres", 
                                "minim"   : 1,   
                                "maxim"   : 100}       
    
    # Diccionario de la instancia 'Distributors'
    def get_dic(self):
        return self._distributor_dic
    
    # Todo lo referente a 'Device'
    def link_device_controller(self, device_controller):
        self._device_controller = device_controller        
        
    def get_device_controller(self):
        return self._device_controller

    def get_device_dic(self):
        return self._device_controller.get_dic()
        
    # Todo lo referenre a 'Dispatch'       
    def link_dispatch_controller(self, dispatch_ctrl):        
        dispatch_ctrl.link_distributor_controller(self)
        self._dispatch_controller = dispatch_ctrl
                
    def get_dispatch_controller(self): 
        return self._dispatch_controller
        
    def get_dispatch_dic(self):
        return self._dispatch_dic
        

    # ADD
    def get_model_data_from_user(self, id):
        """
        Devuelve una tupla para guardar mediante método del model.
        """
       
        delivery = InputUser.get_uint(
            "Tiempo de entrega desde fábrica en días = ")
        
        if delivery is None: return False
        Logger.Core.info('<── ' + '"' + id + '". (Tiempo de entrega ' 
                         + str(delivery) + ' días)\n')
        
        address = InputUser.get_str(self._address_config["question"],
                                    self._address_config["rule"    ],
                                    self._address_config["minim"   ],
                                    self._address_config["maxim"   ], False)
        
        if address is None: return False
        Logger.Core.info('<── ' + '"' + id + '". (' + address + ")\n")        

        data = (delivery, address)        
        if not data: return None
        
        Logger.Core.info('Registrando distribuidor "' + id + '"...'  ) 
        return data
    
    # MODIFY
    def set_modify_data_from_user(self, id):
        """
        Permite al usuario modificar un distribuidor existente en función de 
        su id. Pregunta al usuario si desea modificar cada elemento. Funciona
        de manera identica al resto de controladores
        """
    
        # Distribuidor actual (old)
        old_id = '"' + id + '"'
        old = self._distributor_dic.get(id)
    
        is_modified = False
    
        if old is None:
            Logger.Core.warn(
                "Distribuidor " + id + " no encontrado en el sistema.")
            return False
    
        # A partir de aquí se le pregunta al usuario si quiere modificar
        # cada elemento del distribuidor (independientemente)
    
        # TIEMPO DE ENTREGA
        old_delivery = str(old._delivery_time)
        Logger.Core.info("──> (" + old_id + ": " + old_delivery + " días)")
    
        question = "¿Desea modificar el tiempo de entrega del distribuidor?"
        if InputUser.ask_yes_no_question(question):
            new_delivery = InputUser.get_uint(
                "Nuevo tiempo de entrega desde fábrica en días = ")
            if new_delivery is None:
                return False
            Logger.Core.info("<── (" + old_id + ": " + str(new_delivery) 
                             + " días)\n")
            is_modified = True       
            
        else: new_delivery = old._delivery_time
    
        # DIRECCIÓN DEL DISTRIBUIDOR
        old_address = old._address
        Logger.Core.info("──> (" + old_id + ": " + old_address + ")")
    
        question = "¿Desea modificar la dirección del distribuidor?"
        if InputUser.ask_yes_no_question(question):
            
            q = "Nueva dirección del distribuidor"
            new_address = InputUser.get_str(q, self._address_config["rule"],
                                            self._address_config["minim"],
                                            self._address_config["maxim"], 
                                            False)
            if new_address is None:  return False
            Logger.Core.info("<── (" + old_id + ": " + new_address + ")\n")
            is_modified = True
        else: new_address = old._address
    
        # Si no se realizó ninguna modificación, informamos al usuario
        # y devolvemos False
        if not is_modified:
            i = old_id
            r = "No se realizaron modificaciones en el distribuidor "+ i +"\n"
            Logger.Core.info(r)
            Logger.pause()
            return False
    
        data = (new_delivery, new_address)
        Logger.Core.info("Modificando distribuidor '" + id + "'...")
        
        # Si se modifica el distribuidor, es lógico que afecte a los despachos.
        # Sin embargo, puede ser problemático modificar los despachos que ya
        # están en tránsito, ya que también sería necesario ajustar el cálculo
        # de los días restantes. De la misma manera los despachos cuya entrega
        # ya haya sido realiza no se deberían modificar.
        
        # El sistema informará que solo se hace responsable de los cambios del
        # distribuidor en los Despachos pendientes de envio
        
        i1 = "La modificación del distribuidor solo afectará a los despachos "
        Logger.Core.info(i1 + "pendientes.")
        i2 = "El sistema no se hace responsable de los despachos en transito."                
        Logger.Core.info(i2)
                        
        # Acceso al 'controller' de Despachos
        disp_ctrl = self._dispatch_controller
        
        filtro = [DispatchStatus.PENDING] # Filtro (solo los pendientes)
        devices_dispatches = disp_ctrl.get_devices_by_distributor(id, filtro)
        
        has_dispatch = False
        
        for device_id, dispatch in devices_dispatches:
            
            has_dispatch = True
            
            dev_id = '"' + device_id + '"'
            Logger.Core.info("Despacho pendiente para Equipo :" + dev_id)
            
            Logger.Core.info("Modificando: 'Días de Entrega'")
            dispatch.set_delivery_days(new_delivery)
            
        if has_dispatch:
            i1 = 'Despachos pendientes asociados al distribuidor "' + id + '" '
            i2 = 'Modificados.\n'
            Logger.Core.info(i1 + i2)       
        else:
            i = 'Distribuidor: "' + id + '" sin despachos pendientes.\n'
            Logger.Core.info(i)       
        
        return data


    def remove(self, id):
        """
        Para todos los métodos de los 'controllers' específicos, la función
        debe tener el mismo nombre.
        """        
        
        # Al dar de baja hay que regresar los posibles equipos en despacho
        # a fábrica. Por eso tenemos acceso al controlador de despachos, y
        # usamos la siguiente función.
        
              
        dispatch_ctrl = self._dispatch_controller
        
        filt = [DispatchStatus.PENDING, DispatchStatus.IN_TRANSIT] # FILTRO
        
        devices_dispatches = dispatch_ctrl.get_devices_by_distributor(id, filt)
        
        
        
        
        # Ahora accedemos al controlador de Devices, usando la función 
        # return_device_from_distributor recorremos la lista devices
        # y los vamos devolviendo a fabrica.
        for device_id, dispatch in devices_dispatches:
            
            self._device_controller.return_device_from_distributor(device_id)        
            dispatch.set_status_returned()  
        
        Logger.Core.info("Eliminando distribuidor " + '"' + id + '"...',n='\n')
        del self._distributor_dic[id]          
        Logger.Core.info("Distribuidor " + '"' + id + '" eliminado.\n') 
        return True
        
    
    
    
        
        
        