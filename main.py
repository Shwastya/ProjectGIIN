# -*- coding: utf-8 -*-
"""
Proyecto: HardVIU
Created on Tue Mar 21 09:53:06 2023
@author: José Luis Rosa Maiques

Se trata de usar en el proyecto, convenciones de estilo en Python (PEP 8):
https://www.python.org/dev/peps/pep-0008/

Este módulo contiene el punto de entrada del programa, que crea y ejecuta un
objeto Engine para gestionar y ejecutar el menú interactivo.
"""

from engine import Engine

def main():
    """
    Punto de entrada del programa que ejecuta el objeto Engine.
    
    La función principal del Engine es gestionar y ejecutar el menú.
    El menú importa el módulo correspondiente según la opción seleccionada.
    """
    HardVIU = Engine()
    HardVIU.run()


if __name__ == '__main__':
    main()
