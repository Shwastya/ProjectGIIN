# -*- coding: utf-8 -*-
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

    def __init__(self, pOptions):
        """
        Inicializa un objeto Menu con una lista de opciones.

        Args:
            options (list): lista de cadenas con las opciones del menú.
        """
        self._options = pOptions

    def clear_screen(self):
        """
        Limpia la pantalla de la consola.
        Returns:
        bool: True si la limpieza se realiza con éxito, False en caso contrario.
        """
        limpia = False
        if os.name == 'nt':  # Para Windows
            os.system('cls')
            limpia = True
        else:                # Para Linux, macOS
            os.system('clear')
            limpia = True
        return limpia

    def display(self):
        """
        Dibuja el menú utilizando un bucle que recorre la lista de opciones.
        Muestra las opciones del menú numeradas y (0) para salir.
        """
        counter = 1
        for option in self._options:
            print(str(counter) + ") " + option)
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
