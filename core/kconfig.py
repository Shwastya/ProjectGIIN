# -*- coding: utf-8 -*-
"""
Project: HardVIU
Created on Sat Mar 25 10:16:27 2023
@author: José Luis Rosa Maiques


"""

"""
Define el separador de cadena que se utilizará en las entidades.
Hay que tener en cuenta que si se modifica el separador y se intenta acceder
a archivos antiguos con otro separador, pueden surgir problemas.
"""
K_SEPARATOR = ';'
K_S = K_SEPARATOR  # nombre corto

"""
Constante K_USER_CANCEL, mensaje que el usuario ingresará si desea cancelar 
un registro en curso. Esta constante se aplicará en todo el programa.
"""
K_USER_CANCEL = "X"

"""
K_ENABLE_SCROLL, para habilitar o deshabilitar el desplazamiento en la 
aplicación según preferencias del usuario.
"""
K_ENABLE_SCROLL = True
K_SCROLL = K_ENABLE_SCROLL  # nombre corto

"""
Para validaciones en entradas alfanuméricas que permitan caracteres especiales 
adicionales, como el '-' en: i9-13900KS". 
Se han incluido algunos caracteres adicionales para probar.
Modifique esta variable para controlar este tipo de entradas.
"""
K_ALLOWED_CHARS = "-*+.#@€%&/"
