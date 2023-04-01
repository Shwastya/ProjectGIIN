# -*- coding: utf-8 -*-
"""
Project: HardVIU
Created on Fri Mar 24 22:30:35 2023
@author: José Luis Rosa Maiques

La idea es que la clase funcione como un conjunto de funciones estáticas, 
similar a lo que se haría en C++ en una clase Logger:
    
    https://docs.python.org/3/library/functions.html#staticmethod
    
Colores y secuencias de escape ANSI:
    
    https://python-para-impacientes.blogspot.com/2016/09/dar-color-las-salidas-en-la-consola.html

La implementación básica de colores suele estar asociada al nivel de alerta del mensaje:
    
    Trace (Blanco): mensajes normales
    Info (verde): mensajes informativos
    Warn (amarillo): mensajes de alerta
    Error (rojo): mensajes de error
    Core (magenta): mensajes del núcleo del programa (preferencia personal)
    
Incluir funciones adicionales podría exceder la responsabilidad del Logger. 
Sin embargo, dado que se trata de una aplicación que funciona a nivel de consola, 
se ha tomado la decisión de personalizar un poco los mensajes utilizando este módulo.
"""


from core.kconfig import K_USER_CANCEL, K_SCROLL#, delete_constants


class Logger:

    def trace(msg):
        print("\033[97m" + msg + "\033[0;m")

    def info(msg):
        print("\033[32m" + msg + "\033[0;m")

    def warn(msg):
        print("\033[1;33m" + msg + "\033[0;m")

    def error(msg):
        print("\033[1;31m" + "Error:" + msg + "\033[0;m")

    def core(msg):
        """ Color: Magenta (35) """
        print("\033[0;35m" + "Core: " + msg + "\033[0;m")

    """ 
        Definimos aquí ciertas funciones que se utilizan con frecuencia en el 
        programa. Aunque no se consideran responsabilidad del Logger, 
        para este ejercicio resultan adecuadas.
    """   

    def starting():
        print("\n")
        Logger.core("Starting System")

    def shutdown():
        # delete_constants()
        Logger.core("Shutting-down System")
        
    def scroll_screen(l=100):
        if K_SCROLL:
            print("\n" * l)
        
    def register_quit(msg):
        Logger.cancel_input_by_user(msg)
        Logger.scroll_screen()

    def cancel_info(n1='', n2=''):
        Logger.info(n1 + "Ingresa '" + K_USER_CANCEL + "' para cancelar." + n2)

    def succes(msg1, obj, msg2=""):
        print("\033[1;32m" + msg1 + "\033[0;m" + "\033[1;36m" +
              obj + "\033[0;m" + "\033[1;32m" + msg2 + "\033[0;m")
        
    def success_pause(msg1, obj, msg2, newline=True):
        Logger.succes(msg1, obj, msg2)        
        n = ''
        if newline: n = '\n'
        input(n + "Presione [ENTER] para continuar...")
        
    def cancel_input_by_user(msg):
        input("\033[1;33m" + msg +
              ". Presione [ENTER] para continuar...\033[0;m")

    def there_is_the_question(msg):
        while True:
            r = input(msg + " (Y/N) = ")
            if r.lower() == 'y':
                return True
            elif r.lower() == 'n':
                return False
            else:
                print("\033[1;33mIntroduzca 'y' para sí o 'n' para no.\033[0;m")

    def bad_option():
        Logger.warn("Opción inválida. Elija una opción válida.")
        input("Pulsa [ENTER] para continuar...")

    

    def draw_list(msg, obj):
        print("\033[1;32m" + msg + " " + obj + "\033[0;m")
