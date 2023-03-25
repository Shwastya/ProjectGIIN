# -*- coding: utf-8 -*-
"""
Proyecto: HardVIU
Created on Tue Mar 21 09:53:06 2023
@author: José Luis Rosa Maiques

Este módulo contiene la implementación de la clase Menu, que representa un
menú interactivo con opciones. La clase dispone de tres métodos: display(),
get_option() y clear_screen().

para clear_screen() se consulta:
    https://www.youtube.com/watch?v=SC-wyZpE93M&ab_channel=JohnOrtizOrdo%C3%B1ez
"""
import platform
import os

class Menu:
    """
    La clase Menu representa un menú interactivo con opciones.
    Las opciones se inicializan en el constructor a través de una lista
    pasada como parámetro al instanciar la clase en el Engine.
    La clase dispone de tres métodos: display(), get_option() y clear_screen().
    """

    def __init__(self, opciones):
        """
        Inicializa un objeto Menu con una lista de opciones.

        Args:
            opciones (list): lista de cadenas con las opciones del menú.
        """
        self.opciones = opciones

    def clear_screen(self):
        """
        Limpia la pantalla de la consola.       
        Nota: No quiere funcionar este modo en Spyder
        """        
            
        
        # Esto en teoria es lo que toca
        # pero no quiere funcionar, no sé por qué: 
        
        # Para Windows
        #if os.name == 'nt':  
         #   os.system('cls')
            
            #print("Estamos en windows")
        # Para Linux, macOS
        #else:                
         #   os.system('clear')
            #print("NO Estamos en windows")    

        # print("\n" * 100)    
        
        
    def display(self):
        """
        Dibuja el menú utilizando un bucle que recorre la lista de opciones.
        Muestra las opciones del menú numeradas y (0) para salir.
        """
        counter = 1
        for opcion in self.opciones:
            print(str(counter) + ") " + opcion)
            counter += 1

        print("0) Salir")

    def get_option(self):
        """
        Solicita al usuario una opción del menú y controla errores.

        Returns:
            int: opción seleccionada por el usuario o -1 si no es válida.
        """
        op = input("Elija una opción: ")
        if op.isdigit():
            return int(op)
        else:
            return -1
        

import IPython
from utils.logger import Logger

class MenuDrawer:
    """
    Se implementa otro modulo Menu con la propiedad de dibujar bordes
    adaptandose al ancho del texto.
    
    Se hacen varias pruebas mas para poder limpiar la pantalla en Spyder:
        Probamos con %clear% en IPython pero desafortunadamente
        esto borra la salida de la celda en ejecución, incluido el menú que se muestra.
        
        Probamos metodo mas sencillo haciendo un scroll en la consola, 
        aunque mantenemos el metodo con %clear%, podría tener alguna utilidad
    """
    def __init__(self, opciones, titulo="Menu"):
        self.opciones = opciones
        self.titulo = titulo
        
    def scroll_screen(self, lines):
        print("\n" * lines)
    def clear_screen(self):
        #print("\n" * 100)       
        try:
            shell = IPython.get_ipython()
            shell.run_line_magic("clear", "")
        except (NameError, AttributeError):
            if os.name == 'nt':
                os.system('cls')
            else:
                os.system('clear')
    
    def draw_up(self, width):        
        print("┌" + "─" * width + "┐")
    def draw_empty(self, width):
        print("│" + " " * width + "│")    

    def draw_title(self, width):
        title_length = len(self.titulo)
        padding = (width - title_length) // 2
        
        print("│\033[1;36m" + " " * padding + self.titulo + " " * (width - title_length - padding) + "\033[0;m│")
        
        #print("│" + " " * padding + "\033[1;37m" + self.titulo +  + "\033[0;m" + " " * (width - title_length - padding) + "│")
        
        
        padding = (width + title_length) // 2
        print("│" + " " * padding + " " * (width - title_length - padding) + "  │")
        

    def draw_option(self, option_number, option_text, width):
        print("│ " + str(option_number) + ") " + option_text + " " * (width - len(option_text) - 4) + "│")

    def draw_down(self, width):
        print("└" + "─" * width + "┘")
        
    def display(self):
        max_width = max(len(opcion) for opcion in self.opciones)
        width = max(len(self.titulo), max_width) + 4

        self.draw_up(width)
        self.draw_empty(width)
        self.draw_title(width)

        index = 1
        for opcion in self.opciones:
            self.draw_option(index, opcion, width)
            index += 1

        self.draw_option(0, "Salir", width)
        self.draw_empty(width)
        self.draw_down(width)

    def get_option(self):
        op = input("Elija una opción: ")
        if op.isdigit():
            return int(op)
        else:
            return -1
