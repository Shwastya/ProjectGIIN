# -*- coding: utf-8 -*-
"""
Project: HardVIU
Created on Sat Mar 25 10:16:27 2023
@author: José Luis Rosa Maiques

Clase 'InputUser' métodos estáticos de tipo input con controles
"""

#from core.kconfig import K_ALLOWED_CHARS, K_USER_CANCEL
#from core.entity.component import ComponentType
from config.settings import K_USER_CANCEL, K_LIST

from core.views.logger import Logger

#from core.controllers.model_factory import ModelType
#from core.models.component          import ComponentType

class InputUser:   
    
    def get_uint(msg):
        """ Pide un número entero mayor que cero"""
        while True:
            i = input(msg)
            if i.lower() == K_USER_CANCEL.lower():
                Logger.Core.warn("Proceso anulado por usuario.")
                Logger.pause();
                return None
            elif i.isdigit() and int(i) > 0:
                return int(i)
            else: Logger.Core.warn("El número debe ser entero y mayor que 0.")
    
    def get_float(msg):
        """ Pide un número real """
        while True:
            r = input(msg)
            if r.lower() == K_USER_CANCEL.lower():
                Logger.Core.warn("Proceso anulado por usuario.")
                Logger.pause();
                return None
            elif r.replace('.', '', 1).isdigit() and float(r) > 0:
                return float(r)
            else:
                Logger.Core.warn("Introduce un número real mayor que 0.")                
       
    def get_str(question, regla = None, minim = 1, maxim = None, 
                     need_list = False):
        """
        Pide un alfanumérico.Se añade la posibilidad de validar 'K_USER_CANCEL'
        con 'need_list' por si queremos dar opción o no a pedir un listado.
    
        Parámetros:
            question (str): La pregunta que se mostrará al usuario.
            regla (str, opcional): Una regla adicional para validar la entrada
            minim (int, opcional): La longitud mínima permitida para la entrada
            Por defecto es 1.
            maxim (int, opcional): La longitud máxima permitida para la entrada
            Por defecto es None (sin límite).
            need_list (bool, opcional): Si se debe permitir o no la opción 
            de listar. Por defecto es False.
    
        Returns:
            str: La entrada validada del usuario o None si el usuario cancela 
            la acción.
        """
        while True:
            r = ""
            if regla is not None:  r = " (" + regla + ")"
                
            id = input(question + r + " = ")
    
            if id.lower() == K_USER_CANCEL.lower():
                Logger.Core.warn("Proceso anulado por usuario.")
                Logger.pause()
                return None
            
            if id.lower() == K_LIST and need_list: return id    
            
            # Elimina espacios en blanco al inicio y al final del string
            id_stripped = id.strip()   
            
            if len(id_stripped) < minim:                
                Logger.Core.warn("La entrada debe tener al menos " 
                                 + str(minim) + " caracteres.")
                continue    
            
            if maxim is not None and len(id_stripped) > maxim:                
                Logger.Core.warn("La entrada no debe tener más de " 
                                 + str(maxim)  + " caracteres.")
                continue    
            
            return id
  
    
    def get_from_enum(enum_class, msg1, msg2):        
        """
        Permite escoger al usuario de un enumerado pasado como parametro
        Se puede llamar a get_from_enum pasando el enumerado y dos cadenas 
        que describa el tipo de elemento que se selecciona. Por ejemplo, para 
        seleccionar un tipo de componente, llamarías a la función de la 
        siguiente manera:

            tipo = self.get_enum_input(ComponentType, "msg1", "msg2")        
        """
        while True:
            cad = input(msg1)
            if cad.lower() == K_USER_CANCEL.lower():
                Logger.Core.warn("Proceso anulado por usuario.")
                Logger.pause();
                return None
            elif cad.isdigit():
                index = int(cad) - 1
                if index < 0 or index >= len(enum_class):
                    Logger.Core.warn(msg2)
                else:
                    return enum_class(list(enum_class)[index].value)
            else:
                Logger.Core.warn("Introduce un número válido de la lista.") 
    
    
    
    def ask_yes_no_question(msg):
        while True:
            r = input(msg + " (s/n) = ")
            info = "Las opciones son 's' (sí) o 'n' (no). Intente de nuevo."
            if r.lower()   == 's': return True
            elif r.lower() == 'n': return False
            else: Logger.Core.warn(info)
   

    @staticmethod
    def get_valid_index_or_id(question, max_index, id_list):
        while True:
            input_str = input(question)

            if input_str.lower() == K_USER_CANCEL.lower():
                Logger.Core.warn("Proceso anulado por usuario.")
                Logger.pause()
                return None, None

            if input_str.isdigit():
                index = int(input_str)
                if 1 <= index <= max_index:
                    return "index", index

            if input_str in id_list:
                return "id", input_str

            Logger.Core.warn("La entrada no es válida. Intento de nuevo.")

    @staticmethod
    def get_valid_component(question, disp_components):
        
        max_index = len(disp_components)
        id_list = [comp_id for comp_id, comp in disp_components]

        input_type, input_value = InputUser.get_valid_index_or_id(question, max_index, id_list)

        if input_type is None:
            return None, None

        if input_type == "index":
            selected_comp_id, selected_comp = disp_components[input_value - 1]
        elif input_type == "id":
            selected_comp_id = input_value
            selected_comp = next(comp for comp_id, comp in disp_components if comp_id == selected_comp_id)

        return selected_comp_id, selected_comp
    
    
   
    



    
    
  
    
    
        