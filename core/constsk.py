# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 10:16:27 2023

@author: Jose
"""

"""
Definimos string que queremos usar como separador en las entidades.
Existe el peligro de si se cambia y se trata de acceder a archivos antiguos
en los que se ha usado otro separador (hay que tenerlo en cuenta).
"""
K_SEPARATOR = ';'
K_S = K_SEPARATOR # nombre corto

"""
Se define constante, mensaje que el usuario introducirá si quiere cancelar 
un registro en ejecución, cambiarlo aquí funcionará para todo el programa
"""
K_USER_CANCEL_MSG = "Q"

"""
K_ENABLE_SCROLL, por si se quisiera anular el scrollo en la aplicación
por no ser del agrado del usuario
"""
K_ENABLE_SCROLL = True
K_SCROLL = K_ENABLE_SCROLL

