# -*- coding: utf-8 -*-
"""
Proyecto: HardVIU
Created on Fri Mar 24 16:18:11 2023
@author: José Luis Rosa Maiques
"""
from core.constsk import K_USER_CANCEL_MSG
from utils.drawer import MenuDrawer
from utils.logger import Logger
from utils.icheck import alnumcheck

from core.entity.componente import Componente

class ManagerComponentes:
    def __init__(self):
        self._componentes = []
        
        # Menu principal
        self._menu_componentes = MenuDrawer([
            "Alta", "Modificación"], "- HardVIU -> 1) Componentes")
        
        # Submenu modificacion componente
        self._menu_modificacion = MenuDrawer([
            "Cambiar stock", "Cambiar información", "Dar de baja"], 
            "- HardVIU -> 1) Componentes -> 2. Modificación")
        
    def componente_por_id(self, id):
        for componente in self._componentes:
            if componente._id == id: return componente
        return None

    def listar_componentes(self):
        if not self._componentes:
            return False
        else:
            for componente in self._componentes:
                Logger.draw_list("\t-", componente.display_componente())
            return True

    def register_quit(self):        
        Logger.cancel_input_by_user()       
        self._menu_componentes.scroll_screen() 

    def obtener_id(self):
        while True:
            id = input("Nombre/ID del componente (alfanumérico, mínimo 3 caracteres) = ")
            if id.lower() == K_USER_CANCEL_MSG.lower():
                self.register_quit()
                return None
            if not alnumcheck(id, 3): continue
            if self.componente_por_id(id):
                Logger.warn("Ese identificador ya existe. Por favor, elija otro.")
                continue
            return id
    
    def alta_componente(self):
        self._menu_componentes.scroll_screen()
        Logger.cian_bold("\n" + "1) Alta de nuevo componente:")
        Logger.cancel_info()

        id = self.obtener_id()
        if id is None:
            return

        component_to_add = Componente()
        if not component_to_add.user_set_values(id):
            self.register_quit()
            return

        self._componentes.append(component_to_add)
        if Logger.there_is_the_question("Introducir otro componente"): 
            self.alta_componente()
        
        self._menu_componentes.scroll_screen()

    def seleccionar_componente(self):
        if self._componentes:
            self._menu_componentes.scroll_screen()
            Logger.cian_bold("\n" + "2) Se requiere el Nombre/ID de componente para acceder al menú de modificación:")
            Logger.cancel_info()

            while True:
                id = input("Nombre/ID o 'L' para listar componentes = ")
                if id.lower() == K_USER_CANCEL_MSG.lower():
                    self.register_quit()
                    return None
                elif id.lower() == 'l': self.listar_componentes()
                else:
                    componente = self.componente_por_id(id)
                    if componente:
                        self._menu_componentes.scroll_screen()
                        return componente
                    else:
                        Logger.warn("No se encontró el componente con ese identificador. Por favor, intente de nuevo.")
                        continue
        else:
            Logger.warn("No hay componentes para modificar.\nAcceda al menú de Alta para registrar nuevos componentes.")
            input("\nPresione [ENTER] para continuar...")
            self._menu_modificacion.scroll_screen()
            return None 
                    
    def modificar_componente(self):
        componente = self.seleccionar_componente()
        if componente is None:
            return

        while True:
            self._menu_modificacion.display(True, "Menú Componentes", "->  " + componente._id + "  <-")
            opcion = self._menu_modificacion.get_option()

            if opcion == 0:   # Salir
                self._menu_componentes.scroll_screen()
                break
            elif opcion == 1: # Cambiar stock
                Logger.cian_bold("\n" + "1) Cambiar stock de componente '" + componente._id + "':")
                Logger.cancel_info()
                if not componente.user_set_new_stock(): self.register_quit()
                self._menu_componentes.scroll_screen()
                continue
            elif opcion == 2: # Cambiar información
                Logger.cian_bold("\n" + "2) Cambiar información de componente '" + componente._id + "':")
                Logger.cancel_info(n2='')
                if not componente.user_set_values(componente._id):self.register_quit()
                else:
                    input("\nPresione [ENTER] para continuar...")
                    self._menu_componentes.scroll_screen()
                continue
            elif opcion == 3: # Dar de baja
                self._componentes.remove(componente)
                break
            else:
                Logger.bad_option()
                self._menu_modificacion.scroll_screen(100)

    def update(self):
        self._menu_componentes.scroll_screen(100)
        while True:
            self._menu_componentes.display(False, "Menú principal")
            opcion = self._menu_componentes.get_option()

            if opcion == 1:    # Alta componente
                self.alta_componente()
            elif opcion == 2:  # Modificar componente
                self.modificar_componente()
            elif opcion == 0:  # Salir
                self._menu_componentes.scroll_screen(100)
                break
            else:  # Opción no encontrada
                Logger.bad_option()
                self._menu_componentes.scroll_screen()
                
                
                
                
                
                
                
                
                
                
                
                
                
                