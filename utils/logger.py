# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 22:30:35 2023

@author: Jose

Uso de la biblioteca colorama para hacer nuestro sistema Logger:
    // NO FUNCIONA EN MI SPYDER
    https://github.com/tartley/colorama 
    
Uso de Logger con secuencias de escape ANSI:
    https://python-para-impacientes.blogspot.com/2016/09/dar-color-las-salidas-en-la-consola.html
    
La idea es que la clase funcione como un conjunto de funciones estáticas, 
similar a lo que se haría en C++:
    https://docs.python.org/3/library/functions.html#staticmethod
    

Algunos de los colores:
    Blanco: mensajes normales
    Verde claro: mensajes normales mas bonitos (core sistema)
    Verde: mensajes de información
    Amarillo: mensajes de alerta
    Rojo: mensajes de error
"""

import time
from core.constants import USER_CANCEL_MSG

# Clase con métodos estáticos.
class Logger:    
    
    def core(msg):
        """
        Estilo: No (0)
        Color: Magenta (35) 
        """        
        print("\033[0;35m" + "Core: " + msg + "\033[0;m")
        
    def system(msg):
        print("\033[92mSystem: " + msg + "\033[0;m")   
        
    def trace(msg):
        print("\033[97m" + msg + "\033[0;m")
    
    def info(msg):
        print("\033[32m" + msg + "\033[0;m")
    
    def warn(msg):
        print("\033[1;33m" + msg + "\033[0;m")
    
    def error(msg):
        print("\033[31m" + msg + "\033[0;m")    
        
    """ 
        Definimos aqui mismo ciertas funcs. usadas con frecuencia en el programa.
        No lo considero responsabilidad del Logger, pero para el ejercicio ya va bien
    """
    def starting():
        print("\n")
        Logger.core("starting system")
        
    def shutdown():
        Logger.core("shutting down system")
        
    def white_bold(msg, e ='\n'):
        print("\033[1;37m" + msg + "\033[0;m", end = e)
    
    def yellow_bold(msg, e ='\n'):
        print("\033[1;33m" + msg + "\033[0;m", end = e)
        
    def cian_bold(msg, e ='\n'):
        print("\033[1;36m" + msg + "\033[0;m", end = e)
        
    # Algunos mensajes muy recurrentes en el programa
    def cancel_info(msg = USER_CANCEL_MSG):
        Logger.info("Recuerde que puede anular el registro introduciendo '"+ USER_CANCEL_MSG +"'.\n")
        
    def cancel_pause(t = 1):
        Logger.warn("Cancelando...")
        time.sleep(t)
    
    def cancel_input():
        Logger.warn("Se ha cancelado el registro.")
        input("Presione ENTER para continuar...")
        
    def bad_option():
        Logger.warn("Opción inválida. Elija una opción válida.")
        input("Pulsa [ENTER] para continuar...")
        
        
        
    
    
    