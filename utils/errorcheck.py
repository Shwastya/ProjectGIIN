# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 10:16:27 2023

@author: Jose
"""

from core.constants import USER_CANCEL_MSG
from utils.logger import Logger

def alnumcheck(obj, length = 3, nom = "El identificador"):
    succes = obj.isalnum() and len(obj) >= length
    if not succes:
        Logger.warn(nom + " debe ser alfanumérico y tener al menos " + str(length) + " caracteres. Inténtalo de nuevo.")
    return succes

# Funciones para control de errores
def inputcheck(user_input):
    value = input(user_input)
    if value == USER_CANCEL_MSG:
        raise ValueError
    return value

