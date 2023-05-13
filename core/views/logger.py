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

La implementación básica de colores suele estar asociada al nivel de alerta 
del mensaje:
    
    Trace (Blanco): mensajes normales
    Info (verde): mensajes informativos
    Warn (amarillo): mensajes de alerta
    Error (rojo): mensajes de error
    Core (magenta): mensajes del núcleo del programa (preferencia personal)
    
Incluir funciones adicionales podría exceder la responsabilidad del Logger. 
Sin embargo, dado que se trata de una aplicación que funciona a nivel de 
consola, se ha tomado la decisión de personalizar un poco los mensajes 
utilizando este módulo.
"""

from config.settings import K_ENABLE_SYSTEM_INFO, K_USER_CANCEL, K_SCROLL

class Logger:
    
    # b = 0 -> Texto normal
    # b = 1 -> Texto negrita (bold)
    
    def scroll_screen(l = 100):
        if K_SCROLL: print("\n" * l)
        
    def print_line(n = 60, color = False):
        if color:
            print("\033[37m" + n * "─" + "\033[0m")
        else:
            print(n * "─")
    
    def pause(msg = "Pulsa [ENTER] para continuar..."):
        input(msg)
        
    def low_info(msg, newline = False):
        n = ""
        if newline: n = "\n"
        print("\033[0;37m" + msg + ".\033[0m" + n)
        
    def pluralize(word):
        if   word.lower() == "componente"  : return "Componentes"
        elif word.lower() == "equipo"      : return "Equipos"
        elif word.lower() == "distribuidor": return "Distribuidores"
        elif word.lower() == "despacho"    : return "Despachos"
        elif word.lower() == "fichero"     : return "Ficheros"
        else: return word
    
    def box_title(title, line_length = 60):
        padding = (line_length - len(title) - 2) // 2
        pad_end = line_length - len(title) - padding
    
        # Código ANSI para color rojo brillante
        bright_red_color = "\033[1;35m"
    
        # Código ANSI para resetear el color
        reset_color = "\033[0m"
    
        print("┌" + "─" * line_length + "┐")
        print("│" + " " * padding + bright_red_color + title + reset_color 
              + " " * pad_end + "│")
        print("└" + "─" * line_length + "┘")

        
    class Core: # Logger.Core 
        
        def trace(msg, b = 0):
            """ Blanco (97) """
            print("\033[" + str(b) + ";97m" + msg + "\033[0;m")
            
        def info(msg, b = 0, n = ''):            
            """ Magenta (35) """
            if K_ENABLE_SYSTEM_INFO:
                print(n+"\033[" + str(b) + ";35m[System]: " + msg + "\033[0;m")        
            
        def warn(msg, b = 1):
            """ Amarillo (33) """
            print("\033[" + str(b) + ";33m" + msg + "\033[0;m")
            
        def error(msg, b = 1):
            """ Rojo (35) """
            print("\033[" + str(b) + ";31m" + "Error: " + msg + "\033[0;m")   
            
        def warn_pause(msg):            
            Logger.Core.warn(msg)
            Logger.pause()
        def error_warn_pause(msg1, msg2):
            Logger.Core.error(msg1)    
            Logger.Core.warn(msg2)
            Logger.pause()
            
        def action(msg1, obj, msg2="", newline = True, pause = True, 
                   c1 = "green", c2 = "green"):
            
            color_codes = {"green": "\033[1;32m", 
                           "white": "\033[1;37m", 
                           "reset": "\033[0;m"}
            
            colored_msg1 = color_codes[c1] + msg1 + color_codes["reset"]
            colored_msg2 = color_codes[c2] + msg2 + color_codes["reset"]
            
            print(colored_msg1 + ' \033[1;34m"' + obj + '" \033[0;m' + colored_msg2)
            
            n = ""
            if newline: n = "\n"
            if pause: input(n + "Presione [ENTER] para continuar...")

                
        def two_actions(msg1, obj1, msg2, obj2, newline = True, pause = True):
            print('\033[1;30m' + msg1 + ' \033[0;m\033[0;35m"' + obj1 
                  + '"\033[0;m\033[1;30m: ' + '\033[0;m\033[1;30m' + msg2 
                  + "\033[0;m \033[0;35m" + obj2 + "\033[0;m")    
            
            n = ''
            if newline: n = '\n'
            if pause: 
                input(n + "Presione [ENTER] para continuar...")
        
        def deregistration():
            Logger.Core.warn("Se ha cancelado el registro.")
            Logger.Core.info("Entradas actuales descartadas.")
            Logger.pause()
            
                
                
        
            
    class UI: # Logger.UI
        
        def trace(msg, b = 0):
            """ Blanco (97) """
            print("\033[" + str(b) + ";97m" + msg + "\033[0;m")
            
        def info(msg, b = 1):
            """ Verde (32) """
            print("\033[" + str(b) + ";32m" + msg + "\033[0;m")
            
        def emph(msg, b = 1):
            """ Azul (34) o (36)"""
            print("\033[" + str(b) + ";34m" + msg + "\033[0;m")
            
        def cancel_info(n1 = '', n2 = '', level = 0):
            info = "Para cancelar las entradas de registro (=), ingrese"
            if level == 0:
                Logger.low_info(n1 + info + " '" + K_USER_CANCEL + "'" + n2)
            else:
                Logger.UI.info(n1 + info + " '" + K_USER_CANCEL + "'" + n2, 0)
            
        def success(msg1, obj, msg2, newline = True, pause = True):                        
            print('\033[1;32m' + msg1 + ' \033[0;m\033[1;34m"' + obj 
                  + '"\033[0;m\033[1;32m ' + msg2 + "\033[0;m")            
            n = ''
            if newline: n = '\n'
            if pause: 
                input(n + "Presione [ENTER] para continuar...")   
                
        def bad_option(msg = "Opción inválida. Elija una opción válida."):
            Logger.UI.emph(msg)
            Logger.pause()
            Logger.scroll_screen()
  
    def starting():
        print("\n")
        Logger.Core.info("Console Logger Starting")
        Logger.UI.info(" - Ajuste en (True|False) la info de [System] en 'settings.py'", 0)
        Logger.UI.info(" - El proposito principal de info [System] es para 'Debug'", 0)
    def shutdown():
        Logger.Core.info("Shutting-down Logger")          

