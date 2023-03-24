
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 19:54:47 2023
@author: Jose

La clase Sistema tiene como objetivo crear un sistema de gestión de:
    componentes, equipos, distribuidores y despachos.
    
Se busca simular técnicas de puntero a implementación similares a las utilizadas en C++.
Esta clase tiene el sistema completo, pero la implementación se encuentra en los atributos.
Cada atributo puede modificarse en archivos separados, y luego en Sistema se llamarían a los métodos.

También tenemos la clase Menu, que se quiere utilizar para todas las clases con su propio menú.
Esta clase sistema se ejecutará en el Engine, se da la opción a que la aplicación pueda ejecutar más de un sistema
"""

#from utils.menu import Menu
from utils.menu import MenuDrawer
from core.entitymanager.componentes import ManagerComponentes

class Sistema:
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
        
        self._menu = MenuDrawer([
            "Componentes",
            "Equipos",
            "Distribuidores",
            "Despachar",
            "Días",
            "Info sistema",
            "Ficheros"
        ], "Menu Sistema HardVIU")
        
        self._componentes = ManagerComponentes()
        #self.componentes = []
        #self.equipos = []
        #self.distribuidores = []
        #self.despachos = []
        #self.historico = []

    def run(self):     
        while True :
            
            self._menu.display()
            option = self._menu.get_option()
            
            if option == 1:
                self._componentes.run()
            elif option == 2:
                #import equipos
                #equipos.run()
                print("Option 2")
            elif option == 3:
                #import distribuidores
                #distribuidores.run()
                print("Option 3")
            elif option == 4:
                #import despachar
                #despachar.run()
                print("Option 4")
            elif option == 5:
                #import dias
                #dias.run()
                print("Option 5")
            elif option == 6:
                #import info_sistema
                #info_sistema.run()
                print("Option 6")
            elif option == 7:
                #import ficheros
                #ficheros.run()
                print("Option 7")
            elif option == 0:
                print("Saliendo...")
                break
            else:
                print("Opción no válida.")
    
