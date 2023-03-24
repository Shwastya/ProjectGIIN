"""
Proyecto: HardVIU
Created on Tue Mar 21 09:53:06 2023
@author: José Luis Rosa Maiques

Este módulo contiene la implementación de la clase Menu, que representa un
menú interactivo con opciones. La clase dispone de tres métodos: display(),
get_option() y clear_screen().
"""

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
        Returns:
        bool: True si la limpieza se realiza con éxito, False en caso contrario.
        """
        limpia = False
        
        # Para Windows
        if os.name == 'nt':  
            os.system('cls')
            limpia = True
            
        # Para Linux, macOS
        else:                
            os.system('clear')
            limpia = True
        return limpia

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
"""       
La clase Sistema tiene como objetivo crear un sistema de gestión de:
    componentes, equipos, distribuidores y despachos.
    
Se busca simular técnicas de puntero a implementación similares a las utilizadas en C++.
Esta clase tiene el sistema completo, pero la implementación se encuentra en los atributos.
Cada atributo puede modificarse en archivos separados, y luego en Sistema se llamarían a los métodos.

También tenemos la clase Menu, que se quiere utilizar para todas las clases con su propio menú.
Esta clase sistema se ejecutará en el Engine, se da la opción a que la aplicación pueda ejecutar más de un sistema
"""

# from modulos.menu import Menu


class SistemaHardVIU:
    """    
    La clase Sistema representa el sistema completo de componentes, equipos, distribuidores y despachos.

    Atributos:
        componentes (list): lista de objetos Componente.
        equipos (list): lista de objetos Equipo.
        distribuidores (list): lista de objetos Distribuidor.
        despachos (list): lista de objetos Despacho.
        historico (list): lista de objetos Despacho.
    """
    def __init__(self):
        self._menu = Menu([
            "Componentes",
            "Equipos",
            "Distribuidores",
            "Despachar",
            "Días",
            "Info sistema",
            "Ficheros"
        ])
        self.componentes = []
        self.equipos = []
        self.distribuidores = []
        self.despachos = []
        self.historico = []

    def run(self):
        while True :
            self._menu.display()
            option = self._menu.get_option()            
            if option == 1:                              
                #componentes.run()
                print("Option 1")
            elif option == 2:                
                #equipos.run()
                print("Option 2")
            elif option == 3:                
                #distribuidores.run()
                print("Option 3")
            elif option == 4:                
                #despachar.run()
                print("Option 4")
            elif option == 5:                
                #dias.run()
                print("Option 5")
            elif option == 6:                
                #info_sistema.run()
                print("Option 6")
            elif option == 7:                
                #ficheros.run()
                print("Option 7")
            elif option == 0:
                print("Saliendo...")
                break
            else:
                print("Opción no válida.")
                
"""
Proyecto: HardVIU
Created on Tue Mar 21 09:53:06 2023
Author: José Luis Rosa Maiques

la clase Engine que se encarga de gestionar y ejecutar cualquier sistema que se desee implementar,
en este caso, solo tenemos el sistema HardVIU.
Cada sistema que se implemente tendrá su propio menú. 
Del mismo modo, cada elemento o componente del sistema tendrá su propio menú si es necesario. 
Todos los menús son creados por la misma clase/modulo Menu.
"""

#from modulos.sistema import SistemaHardVIU
#from modulos.menu import Menu

class Engine:
    """
    La clase Engine se encarga de gestionar y ejecutar el sistema deseado.

    Atributos:
        _sistema (obj): objeto de la clase SistemaHardVIU que representa el sistema a ejecutar.
    """

    def __init__(self):
        self._sistema = SistemaHardVIU()
    
    def run(self):        
        self._sistema.run()
"""
Proyecto: HardVIU
Created on Tue Mar 21 09:53:06 2023
@author: José Luis Rosa Maiques

Este módulo implementa el punto de entrada del programa y se encarga de crear y 
ejecutar un objeto Engine, que a su vez ejecutará los sistemas del proyecto. 

Se busca seguir las convenciones de estilo en Python (PEP 8), 
que pueden consultarse en el siguiente enlace: 
    https://www.python.org/dev/peps/pep-0008/.

En este momento, el Engine solo se ha implementado para gestionar un sistema 'HardVIU'.
"""

#from engine import Engine

def main():
    """
    Punto de entrada del programa:
        Crea y ejecuta un objeto Engine para ejecutar los sistemas.    
    
    Aunque se ha llamado a la variable 'sistemas' en plural, 
    en este proyecto solo se ejecuta un sistema. 
    Sin embargo, se ha mantenido el nombre en plural 
    para mantener la coherencia con el propósito del diseño.
    """
    sistemas = Engine()
    sistemas.run()


if __name__ == '__main__':
    main()      
  