# -*- coding: utf-8 -*-
"""
Proyecto: HardVIU
Created on Fri Mar 24 16:18:11 2023
@author: José Luis Rosa Maiques
"""

from utils.menu import MenuDrawer
from utils.logger import Logger

from core.entities  import Componente, TipoComponente
from core.constants import USER_CANCEL_MSG

class ManagerComponentes:
    def __init__(self):
        self.componentes = []
        self.menu = MenuDrawer([
            "Alta", "Modificación"], "- HardVIU Menu -> 1) Componentes")
        self._logger = Logger()

    def agregar_componente(self, id, nombre, tipo, peso, precio, cantidad):
        componente = Componente(id, nombre, tipo, peso, precio, cantidad)
        self.componentes.append(componente)

    def to_string(self):
        componentes_str = []
        for componente in self.componentes:
            componentes_str.append(componente.to_string())
        return '\n'.join(componentes_str)

    def agregar_componente_desde_string(self, componente_str):
        id, nombre, tipo, peso, precio, cantidad = componente_str.split(';')
        self.agregar_componente(id, nombre, TipoComponente(tipo), int(peso), float(precio), int(cantidad))

    def cargar_datos(self, archivo_sistema):
        archivo_sistema.cargar_datos(self)

    def guardar_datos(self, archivo_sistema):
        archivo_sistema.guardar_datos(self)

    def componente_por_id(self, id):
        for componente in self.componentes:
            if componente.id == id:
                return componente
        return None

    def listar_componentes(self):
        if not self.componentes:
            print("No hay componentes para listar, debes de dar de alta algún componente primero.")
            return False
        else:
            for componente in self.componentes:
                print(componente.to_string())
                return True
          
    def register_quit(self):
        Logger.cancel_input()
        self.menu.scroll_screen()
        return
            
    def alta_componente(self):
        Logger.cian_bold("\n"+"1) Alta de un componente:")
        Logger.cancel_info()
        id = input("Identificador (nombre) del componente = ")
        if id == USER_CANCEL_MSG:
            Logger.cancel_input()
            self.menu.scroll_screen()
            return
        if self.componente_por_id(id):
            print("Ese identificador ya existe. Por favor, elija otro.")
            return
        
        componente = Componente()
        if not componente.user_set_values(id):
            Logger.cancel_input()
            self.menu.scroll_screen()
            return
            
        self.componentes.append(componente)
        Logger.info("Componente agregado con éxito.")
            

    def modificar_componente(self):
        id = input("Introduce el ID del componente o 'L' para listar todos los componentes: ")
        if id.lower() == 'l':
            if self.listar_componentes():
                id = input("Introduce el ID del componente que deseas modificar: ")
            else: return

        componente = self.componente_por_id(id)
        if componente is None:
            print("No se encontró ningún componente con ese ID.")
            return

        menu_modificacion = MenuDrawer([
            "Cambio Stock", 
            "Cambio información", 
            "Dar de baja"], "Menu Modificación Componente")
        
        #menu_modificacion.clear_screen()
        menu_modificacion.display()
        opcion_modificacion = menu_modificacion.get_option()

        if opcion_modificacion == 1:
            nueva_cantidad = int(input("Introduce la nueva cantidad: "))
            componente.cantidad = nueva_cantidad
            print("Cantidad actualizada con éxito.")
        elif opcion_modificacion == 2:
            nombre = input("Introduce el nuevo nombre del componente: ")
            tipo = input("Introduce el nuevo tipo de componente (Fuente, PB, TG, CPU, RAM, Disco): ")
            peso = int(input("Introduce el nuevo peso en gramos del componente: "))
            precio = float(input("Introduce el nuevo precio en euros del componente: "))
            cantidad = int(input("Introduce la nueva cantidad del componente: "))
            componente.nombre = nombre
            componente.tipo = TipoComponente(tipo)   
            componente.peso = peso
            componente.precio = precio
            componente.cantidad = cantidad
            print("Información actualizada con éxito.")
        elif opcion_modificacion == 3:
            self.componentes.remove(componente)
            print("Componente dado de baja con éxito.")
        else:
            print("Opción inválida. Por favor, elija una opción válida.")
            input("Presione ENTER para continuar...")
            
    def update(self):
        self.menu.scroll_screen(100)
        while True:            
            self.menu.display()
            opcion = self.menu.get_option()

            if opcion == 0:
                self.menu.scroll_screen(100)
                break
            elif opcion == 1:
                self.alta_componente()
            elif opcion == 2:
                self.modificar_componente()
            else:
                Logger.bad_option()
                self.menu.scroll_screen()
                
                
                
                
                
                
                
                
                
                
                
                
                
                