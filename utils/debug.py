# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 10:16:27 2023

@author: Jose
"""

from core.constants import USER_CANCEL_MSG


# Funciones para control de errores
def inputcheck(user_input):
    value = input(user_input)
    if value == USER_CANCEL_MSG:
        raise ValueError
    return value

