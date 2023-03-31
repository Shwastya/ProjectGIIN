# -*- coding: utf-8 -*-
"""
Project: HardVIU
Created on Sat Mar 25 10:16:27 2023
@author: José Luis Rosa Maiques
"""

from core.kconfig import K_ALLOWED_CHARS, K_USER_CANCEL
from utils.logger import Logger


class InputUser:

    # Permite escoger al usuario de un enumerado pasado como parametro
    def get_enum(enum_class, msg1, msg2):
        """
        Se puede llamar a get_enum_input pasando el enumerado y dos cadenas 
        que describa el tipo de elemento que se selecciona. Por ejemplo, para 
        seleccionar un tipo de componente, llamarías a la función de la 
        siguiente manera:

            tipo = self.get_enum_input(ComponentType, "msg1", "msg2")        
        """
        while True:
            cad = input(msg1)
            if cad.lower() == K_USER_CANCEL.lower():
                return None
            elif cad.isdigit():
                index = int(cad) - 1
                if index < 0 or index >= len(enum_class):
                    Logger.warn(msg2)
                else:
                    return enum_class(list(enum_class)[index].value)
            else:
                Logger.warn("Introduce un número válido de la lista.")

    # Pide un número entero
    def get_int(msg):
        while True:
            i = input(msg)
            if i.lower() == K_USER_CANCEL.lower():
                return None
            elif i.isdigit() and int(i) > 0:
                return int(i)
            else: Logger.warn("El número debe ser entero y mayor que 0.")

    # Pide un número real
    def get_float(msg):
        while True:
            r = input(msg)
            if r.lower() == K_USER_CANCEL.lower():
                return None
            elif r.replace('.', '', 1).isdigit() and float(r) > 0:
                return float(r)
            else:
                Logger.warn("Introduce un número real mayor que 0.")
                
                
    # Pide un alfanúmerico, verificará si el ID existe o no en función del 
    # valor del parámetro check_non_existence. Si es True, buscará un ID que 
    # no exista en el diccionario; si es False, buscará uno que exista.   
    # Para que se use esta funcionalidad hay que pasarle un Dic
    
    def get_alphanum(question =" Nombre/ID entidad", # textos de ejemplo
                         regla="alfanumérico, mínimo 3 caracteres", l = 3,
                         obj = "Identificador", dic = None,
                         check_non_exist=False):
        
        warn = obj + " debe tener al menos (" + str(l) + ") caracteres."
        if check_non_exist: 
            l = 1
            warn = "Entrada vacia. Intenta de nuevo."
        
        while True:
            id = input(question + " (" + regla + ") = ")
            if id.lower() == K_USER_CANCEL.lower():
                Logger.register_quit("Cancelado por usuario")
                return None            
            
            if len(id) < l:                
                Logger.warn(warn)
                continue
    
            chars_are_valid = True
            # <-
            for char in id:
                if not (char.isalnum() or char in K_ALLOWED_CHARS):
                    Logger.warn(
                        "Solo se permiten caracteres alfanuméricos o los " +
                        "caracteres específicos (" + K_ALLOWED_CHARS + ").")
                    chars_are_valid = False
                    break
            # ->
            if not chars_are_valid: continue
    
            if dic is not None:
                if check_non_exist and id not in dic:
                    if id == 'l' or id == 'L': return id
                    Logger.warn(obj + " no se encuentra. Elija otro.")                    
                    continue
                elif not check_non_exist and id in dic:
                    Logger.warn(obj + " ya existe. Elija otro.")
                    continue
    
            return id
        
        