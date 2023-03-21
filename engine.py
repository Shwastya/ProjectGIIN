# -*- coding: utf-8 -*-
"""
Proyecto: HardVIU
Created on Tue Mar 21 09:53:06 2023
@author: José Luis Rosa Maiques

Este módulo contiene la clase Engine que se encarga de gestionar y ejecutar
el menú interactivo, importando y ejecutando los módulos correspondientes
según la opción seleccionada.
"""

from hard_module.menu import Menu

class Engine:
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
    
    def run(self):
        while True :
            self._menu.display()
            option = self._menu.get_option()
            
            if option == 1:
                #import componentes
                #componentes.run()
                print("test opcion 1")
            elif option == 2:
                print("test opcion 2")
                #import equipos
                #equipos.run()
            elif option == 3:
                print("test opcion 3")
                #import distribuidores
                #distribuidores.run()
            elif option == 4:
                print("test opcion 4")
                #import despachar
                #despachar.run()
            elif option == 5:
                print("test opcion 5")
                #import dias
                #dias.run()
            elif option == 6:
                print("test opcion 6")
                #import info_sistema
                #info_sistema.run()
            elif option == 7:
                print("test opcion 7")
                #import ficheros
                #ficheros.run()
            elif option == 0:
                print("Saliendo...")
                break
            else:
                print("Opción no válida.")
