# -*- coding: utf-8 -*-
"""
Project: HardVIU
Created on Sat Mar 25 10:16:27 2023
@author: José Luis Rosa Maiques
"""


"""
K_ENABLE_SYSTEM_INFO, activa o desactiva la información proveniente del [core]
actualmente lo he llamado [System], son (controladores, etc.)
"""
K_ENABLE_SYSTEM_INFO = True
"""
K_ENABLE_SCROLL, para habilitar o deshabilitar el desplazamiento en la 
aplicación en los menus (View), según preferencias del usuario.
"""
K_ENABLE_SCROLL = True
K_SCROLL = K_ENABLE_SCROLL  # nombre corto





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
K_USER_CANCEL = "x"


"""
Constante K_LIST, caracter usado para dar opcion al usuario a listar 
"""
K_LIST = 'l'
k_L = K_LIST

"""
Si se activan las constantes DEBUG el sistema se iniciará con elementos
en memoria, el tipo de elementos dependerá de que constantes se activen.
"""
K_DEBUG_ALL              = True # Habilitará todo, independientemente de 
                                 # si el resto está en True o False
K_DEBUG_TESTS_COMPONENTS = False
K_DEBUG_TESTS_DEVICES    = False


