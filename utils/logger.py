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

from core.kconfig import K_USER_CANCEL

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
        Logger.core("Starting System")
        
    def shutdown():
        Logger.core("Shutting-down System")
        
    def white_bold(msg, e ='\n'):
        print("\033[1;37m" + msg + "\033[0;m", end = e)
    
    def yellow_bold(msg, e ='\n'):
        print("\033[1;33m" + msg + "\033[0;m", end = e)
        
    def cian_bold(msg, e ='\n'):
        print("\033[1;36m" + msg + "\033[0;m", end = e)
        
    def green_bold(msg, e ='\n'):
        print("\033[1;36m" + msg + "\033[0;m", end = e)
        
    # Algunos mensajes muy recurrentes en el programa
    def cancel_info(n1 = '', n2 = '' ):  
        Logger.info(n1 + "Ingresa '"+ K_USER_CANCEL +"' para cancelar." + n2)
        
    def succes_pause(msg = "Presione [ENTER] para continuar...", newline = False):
        n = ''
        if newline: n = '\n'
        input(n + msg)
        
    
    def cancel_input_by_user(msg):
        input("\033[1;33m"+ msg +". Presione [ENTER] para continuar...\033[0;m")
        
    
  
    
    def there_is_the_question(msg):
        while True:
            r = input(msg + " (Y/N) = ")
            if r.lower()   == 'y': return True
            elif r.lower() == 'n': return False
            else: print("\033[1;33mIntroduzca 'y' para sí o 'n' para no.\033[0;m")
            
  
        
    def bad_option():
        Logger.warn("Opción inválida. Elija una opción válida.")
        input("Pulsa [ENTER] para continuar...")
        
    def succes(msg1, obj, msg2 = ""):
        print("\033[1;32m" + msg1 + "\033[0;m" + "\033[1;36m" + obj + "\033[0;m" + "\033[1;32m" + msg2 + "\033[0;m")
        #input("\nPresione [ENTER] para continuar...")
        
    def draw_list(msg, obj):
        print("\033[1;32m" + msg + " " + obj + "\033[0;m")
        
    
        

        
        
    
        
        
        
    
    
    