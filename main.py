# -*- coding: utf-8 -*-
"""
Project: HardVIU
Created on Tue Mar 21 09:53:06 2023
@author: José Luis Rosa Maiques

Este archivo implementa el punto de entrada del programa.
Main crea un objeto Engine, que ejecutará los sistemas del proyecto. 

En este momento, el Engine solo se ha implementado para gestionar un sistema:
    'HardVIU'.
    
En la medida de lo posible, se intenta seguir las reglas de estilo PEP 8:
    https://peps.python.org/pep-0008/
"""

from engine import Engine

def main():
    """
    'EntryPoint' del programa: Crea y ejecuta un objeto Engine encargado de 
    ejecutar la clase System hardviu.
    """
    hardviu = Engine()
    hardviu.run()


if __name__ == '__main__':
    main()
