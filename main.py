# -*- coding: utf-8 -*-
"""
Project: HardVIU
Created on Tue Mar 21 09:53:06 2023
@author: José Luis Rosa Maiques

Se busca en el proyecto hacer un diseño OOP, Los principales retos, sin 
demasiadas pretensiones, son: 
    
    1-  Todo con clases y emplear la abstracción a través de la herencia y el
        polimorfismo, permitiendo que las clases existentes sean extendidas 
        mediante nuevas clases que hereden su comportamiento.
    
    2-  Se busca seguir el patrón de diseño  MVC (Model View Controller).         
            
    3-  Se tiene támbien pensado implementar un patrón de diseño algo más
        sencillo para ciertas clases: Patrón FACTORY Method.

Este archivo implementa el punto de entrada al programa. Main crea un objeto
System, que ejecuta el sistema del proyecto 'HardVIU'.

En la medida de lo posible, se intenta seguir el estilo de código PEP 8:
https://peps.python.org/pep-0008/
"""

from core.system import System, Logger

def main():
    """
    EntryPoint del programa: Crea y ejecuta un objeto engine.App 
    encargado de ejecutar la clase System.
    """    
    hardviu = System()
    
    Logger.starting() 
    hardviu.run()
    Logger.shutdown()


if __name__ == '__main__':
    main()
