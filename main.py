# -*- coding: utf-8 -*-
"""
Proyecto: HardVIU
Created on Tue Mar 21 09:53:06 2023
@author: José Luis Rosa Maiques

Este archivo implementa el punto de entrada del programa.
Main crea un objeto Engine, que ejecutará los sistemas del proyecto. 

En este momento, el Engine solo se ha implementado para gestionar un sistema:
    'HardVIU'.
"""

from engine import Engine

def main():
    """
    Punto de entrada del programa:
        Crea y ejecuta un objeto Engine para ejecutar los sistemas.
    """
    hardviu = Engine()
    hardviu.run()

if __name__ == '__main__':
    main()