# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 10:16:27 2023

@author: Jose
"""
from core.kconfig import K_ALLOWED_CHARS
from utils.logger import Logger

def alnumcheck(obj, length = 3, nom = "El identificador"):
    
    if len(obj) < length:
        Logger.warn(nom + " debe tener al menos " + str(length) + " caracteres.")
        return False
    
    for char in obj:
        if not (char.isalnum() or char in K_ALLOWED_CHARS):
            Logger.warn("Solo se permiten caracteres alfanuméricos o los caracteres específicos (" + K_ALLOWED_CHARS + ").")
            return False
    return True

# Funciones para control de errores
#def inputcheck(user_input):
#    value = input(user_input)
#    if value == USER_CANCEL_MSG:
#        raise ValueError
#    return value

