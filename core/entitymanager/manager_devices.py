# -*- coding: utf-8 -*-
"""
Proyecto: HardVIU
Created on Tue Mar 28 16:43:02 2023
@author: José Luis Rosa Maiques
"""

from core.kconfig import K_USER_CANCEL
from utils.drawer import MenuDrawer
from utils.logger import Logger
from utils.icheck import alfnum_check

from core.entity.device import Device


class ManagerDevices:

    def __init__(self):

        # Atributo Equipos (Devices) de tipo Dic
        self._devices = {}

        # Menu principal
        self._menu_devices = MenuDrawer("HardVIU / 2) Equipos", [
            "Alta", "Modificación"])

        # Submenu nueva alta
        self._menu_add = MenuDrawer("HardVIU / 2) Equipos / 1) Alta")

    # Devuelve la entidad Equipo(device) del Dic _devices mediante por ID
    def entity_by_id(self, id): return self._devices.get(id, None)

    # Lista todas entidades = Devices del Dic _devices
    def list_entities(self):
        if not self._devices:
            return False
        else:
            for device_id, device in self._devices.items():
                Logger.draw_list("\t-", device.display())
            return True
  
    # Selecciona entidad = Device mediante input de usuario con controles
    def select_device(self, entity="equipo", menu="Modificación"):
        if self._devices:
            Logger.cancel_info()
            while True:
                id = input("Identificador para acceder a "
                           + menu + " o 'L' para listar " + entity + "s = ")
                if id.lower() == K_USER_CANCEL.lower():
                    Logger.register_quit("Cancelado por usuario")
                    return None
                elif id.lower() == 'l':
                    self.list_devices()
                else:
                    device = self.entity_by_id(id)
                    if device:
                        Logger.scroll_screen()
                        return device
                    else:
                        Logger.warn(
                            "No se encontró " + entity
                            + " con ese identificador. Inténtelo de nuevo.")
                        continue
        else:
            Logger.register_quit("No existen " + entity + "s")
            return None
        
    # Pregunta por el id entidad = Device por input para registro
    def get_id_input(self, entity="equipo",
                     regla="(alfanumérico, mínimo 3 caracteres)"):
        while True:
            id = input("Identificador " + entity + " " + regla + " = ")
            if id.lower() == K_USER_CANCEL.lower():
                Logger.register_quit("Cancelado por usuario")
                return None
            if not alfnum_check(id, 3):
                continue
            if self.entity_by_id(id):
                Logger.warn(
                    "Ese identificador ya existe. Por favor, elija otro.")
                continue
            return id
        
    # Crea objeto entidad = Device() con input de clase Device para alta
    def add_entity(self, again=True):
        self._menu_add.display(True, show_options=False, show_info=True,
                           obj="Nuevo Equipo")

        id = self.get_id_input()
        if id is None: return
    
        self._menu_add.display(True, show_options=False, show_info=True,
                               obj=str(id))
    
        device = Device()
        if not device.user_set_values(id, self._components):
            Logger.register_quit("Cancelado por usuario")
            return
    
        for component in device.get_components().values():
            self._components.update_stock(component.get_id(), -1)
    
        Logger.succes("Equipo: ", device.display(), " dado de alta con éxito.")
        self._devices[id] = device    
    
        if Logger.there_is_the_question("\n¿Introducir otro equipo?"):
            self.add_entity() # add device (equipo)



    def modify_device(self):
        entity = "Equipo"
        menu = "Modificación"
        device = self.select_device(entity, menu)
        if not device:
            return
    
        while True:
            self._menu_modi.display(
                True, show_options=True, zero="Salir",
                obj=device.get_id())
            option = self._menu_modi.get_option()
            # Salir de Menu modificación
            if option == 0:
                Logger.scroll_screen()
                break
            # Cambiar configuración
            elif option == 1:
                # Add all components of the device back to stock
                for component in device.get_components():
                    self._components.update_stock(
                        component.get_id(), 1, 0, "Componente devuelto por desmonte de equipo")
                # Remove all components of the device
                device.clear_components()
                Logger.info(
                    "Introduce los componentes para la nueva configuración del equipo: ")
                if self.add_device_components(device):
                    # Update stock for all added components
                    for component in device.get_components():
                        self._components.update_stock(
                            component.get_id(), -1, 0, "Componente utilizado para creación de equipo")
                    Logger.succes("Configuración del equipo: ",
                                  device.display(), " actualizada con éxito.")
                    Logger.succes_pause(newline=True)
            # Dar de baja
            elif option == 2:
                if self.remove_device(device):
                    break
                continue
            # Opción no encontrada
            else:
                Logger.bad_option()
    
    
    def update(self):
        while True:
            self._menu_devices.display(zero="Salir")
            option = self._menu_devices.get_option()
            # Alta equipo
            if option == 1:
                self.add_entity()
            # Acceder a Menu Modificación
            elif option == 2:
                self.modify_entity()
            # Salir de menu Equipos
            elif option == 0:
                break
            # Opción no encontrada
            else:
                Logger.bad_option()
