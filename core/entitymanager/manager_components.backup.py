# -*- coding: utf-8 -*-
"""
Proyecto: HardVIU
Created on Fri Mar 24 16:18:11 2023
@author: José Luis Rosa Maiques

El ManagerComponent se encarga de gestionar los Componentes, proporcionando 
una lógica de menú. La estructura de datos y la funcionalidad de la entidad 
Componente se mantienen en la clase Componente, mientras que el Manager no 
necesita conocer su funcionamiento interno, solo debe conservar el ID como 
atributo relacional.

En una primera versión, se implementó el atributo 'components' como una lista,
lo que requería que muchas funciones iteraran sobre ella para llevar a cabo su 
lógica. Estaba nanejando la lista como lo haría en C++.

Transformar 'components' en un diccionario lo hace más eficiente en este 
caso, ya que no es necesario iterar linealmente sobre él. El único listado 
que requerimos lineal se encuentra en los tipos de componentes, ubicados 
en un enum en el archivo component.py -> ComponentType (enum class)


List vs Tuples vs Sets vs Dictionaries: 
    https://realpython.com/python-data-structures/
    
"""

from core.kconfig import K_USER_CANCEL
from utils.drawer import MenuDrawer
from utils.logger import Logger
from utils.icheck import alfnum_check

from core.entity.component import Component


class ManagerComponents:

    def __init__(self):

        # Atributo Componentes de tipo Dic
        self._components = {}

        # Menu principal
        self._menu_comp = MenuDrawer("HardVIU / 1) Componentes", [
            "Alta", "Modificación"])

        # Submenu nueva alta
        self._menu_add = MenuDrawer("HardVIU / 1) Componentes / 1) Alta")

        # Submenu modificación componente
        self._menu_modi = MenuDrawer(
            "HardVIU / 1) Componentes / 2) Modificación", [
                "Cambiar stock", "Cambiar información", "Dar de baja"])

        # Submenu cambiar información
        self._menu_info = MenuDrawer(
            "HardVIU / 1) Componentes / 2) Modificación / 2) Cambiar información")

    # Crea objeto entidad = Component() con input de clase Component para alta

    def add_entity(self, again=True):
        self._menu_add.display(True, show_options=False, show_info=True,
                               obj="Nuevo Componente")
        id = self.get_entity_id_input()
        if id is None:
            return
        self._menu_add.display(True, show_options=False, show_info=True,
                               obj=str(id))
        component = Component()
        if not component.user_set_values(id):
            Logger.register_quit("Cancelado por usuario")
            return
        Logger.succes("Componente: ", id, " dado de alta con éxito.")
        self._components[id] = component
        if Logger.there_is_the_question("\n¿Introducir otro componente?"):
            self.add_entity()

    # Lista todas entidades = Components del Dic _components
    def list_entities(self):
        if not self._components:
            return False
        else:
            for id, component in self._components.items():
                Logger.draw_list("\t-", component.display(id))
            return True

    # Selecciona entidad = Component mediante input de usuario con controles
    def input_select_entity(self, entity="componente", menu="Modificación"):
        if self._components:
            Logger.cancel_info()
            while True:
                id = input("Nombre/ID para acceder a " + menu +
                           " o 'L' para listar " + entity + "s = ")
                if id.lower() == K_USER_CANCEL.lower():
                    Logger.register_quit("Cancelado por usuario")
                    return None
                elif id.lower() == 'l':
                    self.list_entities()
                else:
                    # Verifica si el ID ingresado por el usuario
                    # está en el  diccionario de entidades
                    if id in self._components:
                        Logger.scroll_screen()
                        return id  # Devuelve el ID ingresado por el usuario
                    else:
                        Logger.warn(
                            "No se encontró " + entity
                            + " con ese identificador. Intentelo de nuevo.")
                        continue
        else:
            Logger.register_quit("No existen " + entity + "s")
            return None

    # Pregunta por el id entidad = Component por input para registro
    def get_entity_id_input(self, entity="componente",
                            regla="(alfanumérico, mínimo 3 caracteres)"):
        while True:
            id = input("Nombre/ID " + entity + " " + regla + " = ")
            if id.lower() == K_USER_CANCEL.lower():
                Logger.register_quit("Cancelado por usuario")
                return None
            if not alfnum_check(id, 3):
                continue
            if id in self._components:
                Logger.warn("Ese identificador ya existe. Elija otro.")
                continue
            return id

    # Crea objeto entidad = Component() con input de clase Component para alta
    def add_entity(self, again=True):
        self._menu_add.display(True, show_options=False, show_info=True,
                               obj="Nuevo Componente")

        id = self.get_entity_id_input()
        if id is None:
            return

        self._menu_add.display(True, show_options=False,
                               show_info=True, obj=id)

        component = Component()
        if not component.user_set_values(id):
            Logger.register_quit("Cancelado por usuario")
            return

        Logger.succes("Componente: ", id, " dado de alta con éxito.")
        self._components[id] = component

        if Logger.there_is_the_question("\n¿Introducir otro componente?"):
            self.add_entity()

    def modify_entity_stock(self, id):
        Logger.cancel_info()
        if not self._components[id].user_set_values(id, "Nueva cantidad"):
            Logger.register_quit("Cancelado por usuario")
        else:
            Logger.success_pause("Componente: ", self._components[id].display(id),
                                 " stock actualizado.", True)

    def modify_entity_info(self, id):
        self._menu_info.display(
            True, show_options=False, show_info=True, obj=id)
        if not self._components[id].user_set_values(id):
            Logger.register_quit("Cancelado por usuario")
        else:
            Logger.success_pause("Componente: ", self._components[id].display(id),
                                 " modificado con éxito.", True)

    def remove_entity(self, id):
        Logger.succes("Componente a dar de baja: ", id)
        if Logger.there_is_the_question(
                "¿Está seguro de que desea dar de baja este componente?"):
            Logger.success_pause("Componente: ", id,
                                 " eliminado del sistema.", True)
            del self._components[id]
            return True
        else:
            Logger.register_quit("Cancelado por usuario")
            return False

    def update(self):
        while True:
            self._menu_comp.display(zero="Salir")
            option = self._menu_comp.get_option()
            # Alta componente
            if option == 1:
                self.add_entity()
            # Acceder a Menu Modificación
            elif option == 2:
                id = self.input_select_entity()
                if id is None:
                    continue
                while True:
                    print(id)
                    self._menu_modi.display(
                        True, show_options=True, zero="Salir", obj=id)
                    option = self._menu_modi.get_option()
                    # Salir de Menu modificación
                    if option == 0:
                        Logger.scroll_screen()
                        break
                    # Cambiar stock
                    elif option == 1:
                        self.modify_entity_stock(id)
                        continue
                    # Cambiar información
                    elif option == 2:
                        self.modify_entity_info(id)
                        continue
                    # Dar de baja
                    elif option == 3:
                        if self.remove_entity(id):
                            break
                        continue
                    # Opción no encontrada
                    else:
                        Logger.bad_option()
            # Salir de menu Componentes
            elif option == 0:
                break
            # Opción no encontrada
            else:
                Logger.bad_option()
