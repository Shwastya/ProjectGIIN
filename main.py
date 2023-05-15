# -*- coding: utf-8 -*-
"""
Project: HardVIU
Created on Tue Mar 21 09:53:06 2023
@author: José Luis Rosa Maiques

Se busca en el proyecto hacer un diseño OOP, Los principales retos, son: 
    
    1-  Enfoque OOP, abstracción a través de la herencia y el polimorfismo.        
    
    2-  Se busca seguir el patrón de diseño MVC (Model View Controller).         
            
    3-  Se tiene támbien pensado implementar un patrón de diseño sencillo.
        Patrón FACTORY Method.
        
    4-  La idea es hacer un motor que haga este tipo de aplicaciones, hasta 
        donde se llegue, dificilmente llegará a ser un 'Framework' completo.
        
    5-  La aplicación, al margen de que su implementación como 'Framework'
        no sea perfecta, debe funcionar perfectamente, manejando todos los 
        casos y posibles errores.

Este archivo implementa el punto de entrada al programa. Main crea un objeto
System, que ejecuta el sistema del proyecto 'HardVIU'.

En la medida de lo posible, se intenta seguir el estilo de código PEP 8:
https://peps.python.org/pep-0008/
"""

from core.system import System, Logger

def main():
    """
    'EntryPoint' del programa: Crea y ejecuta System
    """    
    hardviu = System()
    
    Logger.starting()
    hardviu.run()
    Logger.shutdown()


if __name__ == '__main__':
    main()
