# -*- coding: utf-8 -*-
"""
Proyecto: HardVIU
Created on Tue Mar 21 09:53:06 2023
@author: José Luis Rosa Maiques

Este archivo implementa el punto de entrada del programa y se encarga de crear y 
ejecutar un objeto Engine, que a su vez ejecutará los sistemas del proyecto. 

En este momento, el Engine solo se ha implementado para gestionar un sistema:
    'HardVIU'.
    
Se busca seguir las convenciones de estilo en Python (PEP 8), 
que pueden consultarse en el siguiente enlace: 
    https://www.python.org/dev/peps/pep-0008/.
"""

from engine import Engine

def main():
    """
    Punto de entrada del programa:
        Crea y ejecuta un objeto Engine para ejecutar los sistemas.    
    
    Aunque se ha llamado a la variable 'sistemas' en plural, 
    en este proyecto solo se ejecuta un sistema. 
    Sin embargo, se ha mantenido el nombre en plural para mantener 
    la coherencia con el propósito del diseño.
    """
    sistemas = Engine()
    sistemas.run()

if __name__ == '__main__':
    main()