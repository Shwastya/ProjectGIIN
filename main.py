# -*- coding: utf-8 -*-
"""
Project: HardVIU
Created on Tue Mar 21 09:53:06 2023
@author: José Luis Rosa Maiques

Se busca en el proyecto hacer un diseño OOP, Los principales retos, sin 
demasiadas pretensiones, son: 
    
    1-  Enfoque OOP, abstracción a través de la herencia y el polimorfismo.        
    
    2-  Se busca seguir el patrón de diseño 1MVC (Model View Controller).         
            
    3-  Se tiene támbien pensado implementar un patrón de diseño sencillo.
        Patrón FACTORY Method.

Este archivo implementa el punto de entrada al programa. Main crea un objeto
System, que ejecuta el sistema del proyecto 'HardVIU'.

En la medida de lo posible, se intenta seguir el estilo de código PEP 8:
https://peps.python.org/pep-0008/
"""

from core.system import System, Logger

def main():
    """
    EntryPoint del programa: Crea y ejecuta System
    """    
    hardviu = System()
    
    Logger.starting() 
    hardviu.run()
    Logger.shutdown()


if __name__ == '__main__':
    main()
