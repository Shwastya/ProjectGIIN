# -*- coding: utf-8 -*-
"""
Proyecto: HardVIU
Created on Fri Apr 21 22:28:07 2023
@author: José Luis Rosa Maiques

Métodos específicos para el controlador del tipo de modelo 'Component'. 
La herencia del controlador se realiza sobre modelos específicos como 
'ComponentController' mediante composición, compartiendo el diccionario origen 
desde el controlador base.
"""
from config.DEBUG import debug_components # Debug y testeo

from core.controllers.inputs import InputUser
from core.models.component   import ComponentType
from core.views.logger       import Logger

# provisional
from core.models.component   import Component

class ComponentController:
    def __init__(self, component_dic):
        self._component_dic = component_dic      
        
        # Con propositos de testeo/debug. Se activa desde settings.py        
        debug_components(self._component_dic)        
       
    def get_dic(self): return self._component_dic
    
    def get_new_stock_from_user(self, id):
        """
        Pregunta al usuario por una cantidad de componentes. 
        Si devuelve 'False' es cancelación por parte del usuario.
        En caso de exito devuelve 'True'
        
        Esta función es propia del modelo 'Component'
        """                
        question = "Nueva stock de componentes para " + id + " = "
        cantidad = InputUser.get_uint(question)        
        if cantidad is None: return False  
        self._component_dic[id].set_quantity(cantidad)
        
        return True
    
    def get_model_data_from_user(self, id):
        """
        La función pregunta al usuario por los datos del componente.
    
        Devuelve 'False' si el usuario ha cancelado desde InputUser (None).
        Devuelve una tupla con los datos si todo ha ido correctamente para 
        guardar mediante método del model.
        
        IMPORTANTE:
        Todos los controllers de los modelos deben implementar esta función
        Que debe estar en consonancia con la estructura del modelo.
        
        
        """
        ComponentType.display()
    
        msg1 = "Elija un número de la lista para el tipo de componente = "
        msg2 = "El Tipo de componente no está en la lista."
    
        tipo = InputUser.get_from_enum(ComponentType, msg1, msg2)
        if tipo    is None: return False
        Logger.low_info('[saved]: ' + tipo.value + ' "' + id + '"')                  
        peso = InputUser.get_uint("Peso en gramos del componente = ")
        if peso    is None: return False
        Logger.low_info('[saved]: ' + tipo.value + ' "' + id + '" ' 
                        + str(peso) + ' gramos')               
        precio = InputUser.get_float("Precio en euros del componente = ")
        if precio  is None: return False
        Logger.low_info('[saved]: ' + tipo.value + ' "' + id + '" '  
                        + str(precio) + ' euros')                
        cantidad = InputUser.get_uint("Cantidad de componentes = ")
        if cantidad is None: return False           
        Logger.low_info('[saved]: ' + tipo.value + ' "' + id + '" ' 
                        + str(cantidad) + ' stock')        
              
        data = (tipo, peso, precio, cantidad)
        return data
        
    def remove(self, id):        
        Logger.Core.action("Componente a dar de baja", id, pause = False)         
        question = "¿Seguro que desea eliminar este componente del sistema?"        
        if InputUser.ask_yes_no_question("\n" + question):            
            del self._component_dic[id]            
            return True
        else: return False
        
    def update_stock_by_component_list(self, component_list, increment): 
        """
        Podemos usar esta función para actualizar el stock usando la función 
        de la clase Component 'update_quantity'. Este método lo usará 
        principalmente el 'controller' de equipos, al ensamblar o desensamblar.
        El 'controller' devices tendrá un enlace a este controlador.
        """
        for id in component_list:
            updated = self._component_dic[id].update_quantity(increment)
            if not updated:
                Logger.Core.warn('Stock de componente "' 
                                 + id + "' es menor a 0.")
    
    
    
    
    