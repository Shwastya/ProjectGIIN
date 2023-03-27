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
from core.constsk import K_SCROLL

class MenuDrawer:
    def __init__(self, opciones, titulo="Menu"):
        self.opciones = opciones
        self.titulo = titulo
        
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
            print("│\033[1;32m" + " " * padding + obj + " " * (width -  title_length - padding) + "\033[0;m│")

        print("│" + " " * width + "│")        

    def draw_option(self, option_number, option_text, width):
        print("│ " + str(option_number) + ") " + option_text + " " * (width - len(option_text) - 4) + "│")

    def draw_down(self, width):
        print("└" + "─" * width + "┘")
        
    def display(self, extra = False, zero = "Salir" ,obj = "unknow"):
        max_width = max(len(opcion) for opcion in self.opciones)
        width = max(len(self.titulo), max_width) + 4

        self.draw_up(width)
        self.draw_empty(width)
        self.draw_title(width)

        if extra: self.draw_title(width, obj, 2)

        index = 1
        for opcion in self.opciones:
            self.draw_option(index, opcion, width)
            index += 1

        self.draw_option(0, zero, width)
        self.draw_empty(width)
        self.draw_down(width)

    def get_option(self):
        op = input("Seleccione una opción: ")
        if op.isdigit(): return int(op)
        else: return -1
