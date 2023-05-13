# -*- coding: utf-8 -*-
"""
Project: HardVIU
Created on Sat Mar 25 10:16:27 2023
@author: José Luis Rosa Maiques

Clase 'InputUser' métodos estáticos de tipo input con controles
"""

from core.views.logger import Logger
from config.settings   import K_USER_CANCEL, K_LIST


class InputUser:   
    
    @staticmethod
    def get_uint(msg):
        """ Pide un número entero mayor que cero"""
        while True:
            i = input(msg)
            if i.lower() == K_USER_CANCEL.lower():
                Logger.Core.deregistration()
                return None
            elif i.isdigit() and int(i) > 0:
                return int(i)
            else: Logger.Core.warn("El número debe ser entero y mayor que 0.")
    
    @staticmethod
    def get_float(msg):
        """ Pide un número real """
        while True:
            r = input(msg)
            if r.lower() == K_USER_CANCEL.lower():
                Logger.Core.deregistration()
                return None
            elif r.replace('.', '', 1).isdigit() and float(r) > 0:
                return float(r)
            else:
                Logger.Core.warn("Introduce un número real mayor que 0.")                
       
    @staticmethod
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
                Logger.Core.deregistration()
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
  
    @staticmethod
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
                Logger.Core.deregistration()
                return None
            elif cad.isdigit():
                index = int(cad) - 1
                if index < 0 or index >= len(enum_class):
                    Logger.Core.warn(msg2)
                else:
                    return enum_class(list(enum_class)[index].value)
            else:
                Logger.Core.warn("Introduce un número válido de la lista.") 
    
    
    @staticmethod
    def ask_yes_no_question(msg):
        while True:
            r = input(msg + " (s/n): ")
            info = "Las opciones son 's' (sí) o 'n' (no). Intente de nuevo."
            if r.lower()   == 's': return True
            elif r.lower() == 'n': return False
            else: Logger.Core.warn(info)
   

    @staticmethod
    def get_valid_index_or_id(question, max_index, id_list, need_list=False):
        """
        TODO: Esta función controla tambien un caso de ambiguedad entre indice
        y Nombre/ID
        
        Solicita al usuario que ingrese un índice o ID válido.
        
        Parámetros:
        - question: La pregunta que se le hará al usuario.
        - max_index: El índice máximo permitido.
        - id_list: La lista de IDs válidos.
        - need_list: Si se necesita la opción de mostrar la lista (opcional).
        
        Retorno:
        - Una tupla que contiene el tipo de entrada ("index" o "id"), el valor 
        de entrada y un booleano que indica si se debe mostrar la lista.
    
        La función verifica si la entrada del usuario es un número dentro del 
        rango permitido de índices. Si el usuario ingresa un número de 3 
        caracteres que también está presente en la lista de IDs, se le pedirá 
        que ingrese directamente el ID para evitar confusiones. Si la entrada 
        es válida, devuelve una tupla con el tipo de entrada, el valor y un 
        booleano que indica si se debe mostrar la lista de elementos 
        (si need_list es True).
    
        Si el usuario cancela la operación, devuelve None en lugar del tipo y 
        el valor de entrada.
        """
        while True:
            input_str = input(question)
    
            if input_str.lower() == K_USER_CANCEL.lower():
                Logger.Core.deregistration()
                return None, None, False
    
            if need_list and input_str.lower() == K_LIST.lower():
                return None, None, True
    
            if input_str.isdigit():
                index = int(input_str)
                if 1 <= index <= max_index:
                    if input_str in id_list:
                        Logger.Core.info("Ambiguedad entre índice e ID.")                        
                        Logger.Core.warn(
                            "El número ingresado coincide con un ID.")
                        s="Ingrese el ID directamente para evitar confusiones."
                        Logger.Core.warn(s)
                        continue
                    return "index", index, False
    
            if input_str in id_list:
                return "id", input_str, False
    
            Logger.Core.warn("La entrada no es válida. Intento de nuevo.")


    @staticmethod
    def get_valid_model(q, r, disp_models, need_list = False):
        
        question = q + " " + r # question + rule
        
        max_index = len(disp_models)
        id_list = [model_id for model_id, model in disp_models]

        i_type, i_value, show_list = InputUser.get_valid_index_or_id(question,
                                                                     max_index,
                                                                     id_list,
                                                                     need_list)
        if i_type is None:  return None, None, show_list

        if i_type == "index":
            selected_model_id, selected_model = disp_models[i_value - 1]
        elif i_type == "id":
            selected_model_id = i_value
            selected_model = next(model for model_id, 
                                  model in disp_models 
                                  if model_id == selected_model_id)

        return selected_model_id, selected_model, show_list
    
    
   
    



    
    
  
    
    
        