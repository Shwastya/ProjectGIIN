# -*- coding: utf-8 -*-
"""
Proyecto: HardVIU
Created on Tue Mar 21 09:53:06 2023
@author: José Luis Rosa Maiques

Menu 


para clear_screen() se consulta:
    // NO FUNCIONA BIEN EN LA CONSOLA SPYDER
    https://www.youtube.com/watch?v=SC-wyZpE93M&ab_channel=JohnOrtizOrdo%C3%B1ez
    
"""

from core.kconfig import K_SCROLL, K_USER_CANCEL

class MenuDrawer:
    def __init__(self, titulo, opciones = [""]):
        self.opciones = opciones
        self.titulo   = titulo
        
    def scroll_screen(self, l = 100):
        if K_SCROLL: print("\n" * l)
    
    def draw_up(self, width):        
        print("┌" + "─" * width + "┐")
    def draw_empty(self, width):
        print("│" + " " * width + "│")    

    def draw_title(self, width, obj = "", color = 1):
        title_length = len(self.titulo)
        padding = (width - title_length) // 2

        if color == 1:
            print("│\033[1;36m" + " " * padding + self.titulo + " " * (width - title_length - padding) + "\033[0;m│")            
        else:
            title_length = len(obj)
            padding = (width -  title_length) // 2
            if color == 2:                
                print("│\033[1;32m" + " " * padding + obj + " " * (width -  title_length - padding) + "\033[0;m│")
            else:
                print("│\033[0;32m" + " " * padding + obj + " " * (width -  title_length - padding) + "\033[0;m│")           

        if color < 3: print("│" + " " * width + "│")        

    def draw_option(self, option_number, option_text, width):
        print("│ " + str(option_number) + ") " + option_text + " " * (width - len(option_text) - 4) + "│")

    def draw_down(self, width):
        print("└" + "─" * width + "┘")
        
    def display(self, extra=False, show_options=True, zero="Salir", obj="unknow", show_info = ""):
        
        self.scroll_screen()
        
        max_width = max(len(opcion) for opcion in self.opciones)
        width = max(len(self.titulo), max_width) + 4

        self.draw_up(width)
        self.draw_empty(width)
        self.draw_title(width)

        if extra:
            self.draw_title(width, obj, 2)

        if show_options:
            index = 1
            for opcion in self.opciones:
                self.draw_option(index, opcion, width)
                index += 1
            self.draw_option(0, zero, width)
        if show_info: 
            self.draw_title(width, "Ingresa '"+ K_USER_CANCEL +"' para cancelar", 3)

        self.draw_empty(width)
        self.draw_down(width)

    def get_option(self, inp = "Seleccione una opción"):
        op = input(inp + " = ")
        if op.isdigit(): return int(op)
        else: return -1
