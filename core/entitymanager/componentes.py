# -*- coding: utf-8 -*-
"""
Proyecto: HardVIU
Created on Fri Mar 24 16:18:11 2023
@author: José Luis Rosa Maiques
"""

from utils.menu import MenuDrawer
from utils.logger import Logger
from utils.errorcheck import alnumcheck

from core.entity.componente  import Componente
from core.constants import USER_CANCEL_MSG

class ManagerComponentes:
    def __init__(self):
        self._componentes = []
        
        # Menu principal
        self._menu_componentes = MenuDrawer([
            "Alta", "Modificación"], "- HardVIU Menu -> 1) Componentes")
        
        # Submenu modificacion componente
        self._menu_modificacion = MenuDrawer([
            "Cambiar stock", "Cambiar información", "Dar de baja"], 
            "- HardVIU Menu -> 1) Componentes -> 2. Modificación")

    def componente_por_id(self, id):
        for componente in self._componentes:
            if componente.id == id: return componente
        return None

    def listar_componentes(self):
        if not self._componentes:
            print("No hay componentes para listar, debes de dar de alta algún componente primero.")
            return False
        else:
            for componente in self._componentes:
                print(componente.display_componente())
            return True
          
    def register_quit(self):
        Logger.cancel_input()
        self._menu_componentes.scroll_screen()
        return
            
    # submenu de componentes -> ALTA componente
    def alta_componente(self):
        Logger.cian_bold("\n" + "1) Alta de un componente:")
        Logger.cancel_info()

        while True: # Pide el nombre (id) hasta que sea valido
        
            id = input("Identificador (nombre) del componente (alfanumérico, mínimo 3 caracteres) = ")
            if id.lower() == USER_CANCEL_MSG.lower():
                return self.register_quit()
                
            if not alnumcheck(id, 3): continue
            if self.componente_por_id(id): Logger.warn("Ese identificador ya existe. Por favor, elija otro.")
                continue
            break

        component_to_add = Componente()
        if not component_to_add.user_set_values(id):
            return self.register_quit()

        self._componentes.append(component_to_add)
        Logger.info("Componente agregado con éxito.")        
            
    # submenu de componentes -> MODIFICAR componente
    def modificar_componente(self):
        Logger.cian_bold("\n" + "2) Modificación de un componente:")
        Logger.cancel_info()

        while True:
            id = input("Identificador (nombre) del componente que desea modificar o 'L' para listar componentes = ")
            if id.lower() == USER_CANCEL_MSG.lower():
                return self.register_quit()
            elif id.lower() == 'l':
                if not self.listar_componentes():
                    continue
            else:
                componente = self.componente_por_id(id)
                if componente:
                    break
                else:
                    Logger.warn("No se encontró el componente con ese identificador. Por favor, intente de nuevo.")
                    continue

        

        while True:
            self._menu_modificacion.display()
            opcion = self._menu_modificacion.get_option()

            if opcion == 0: return self.register_quit()
            elif opcion == 1:
                # Cambiar stock
                while True:
                    cantidad = input("Introduzca la nueva cantidad de componentes: ")
                    if cantidad.lower() == USER_CANCEL_MSG.lower():
                        return self.register_quit()
                    elif cantidad.isdigit() and int(cantidad) > 0:
                        componente.cantidad = int(cantidad)
                        Logger.info("Stock actualizado con éxito.")
                        break
                    else:
                        Logger.warn("Por favor, introduce un número entero mayor que 0.")
                break
            elif opcion == 2:
                # Cambiar información
                if not componente.user_set_values(id):
                    return self.register_quit()
                Logger.info("Información del componente actualizada con éxito.")
                break
            elif opcion == 3:
                # Dar de baja
                self._componentes.remove(componente)
                Logger.info("Componente dado de baja con éxito.")
                break
            else:
                Logger.bad_option()
                self._menu_modificacion.scroll_screen(100)
            
    def update(self):
        self._menu_componentes.scroll_screen(100)
        while True:            
            self._menu_componentes.display()
            opcion = self._menu_componentes.get_option()

            if opcion == 0:
                self._menu_componentes.scroll_screen(100)
                break
            elif opcion == 1:
                self.alta_componente()
            elif opcion == 2:
                self.modificar_componente()
            else:
                Logger.bad_option()
                self._menu_componentes.scroll_screen()
                
                
                
                
                
                
                
                
                
                
                
                
                
                