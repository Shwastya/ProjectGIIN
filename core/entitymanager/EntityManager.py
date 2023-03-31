# -*- coding: utf-8 -*-
"""
Proyecto: HardVIU
Created on Thu Mar 30 10:55:21 2023
@author: José Luis Rosa Maiques

Considerando que estamos haciendo la abstracción OOP considerando entidades,
Existe funcionalidad común entre ManagerComponents y ManagerDevices, sobre todo
en la gestión de entidades (Componentes, Equipos(devices), Distribuidores),
crear una clase base Manager con un atributo Entities podría ser una buena 
idea para centralizar esta funcionalidad compartida.

OOP en Python:    
    https://j2logo.com/python/tutorial/programacion-orientada-a-objetos/
    
Clase base para los Managers de Entidades:
    - Componentes
    - Equipos(Devices)
    - Distribuidores    
"""

from core.kconfig import K_USER_CANCEL
from utils.drawer import MenuDrawer
from utils.inputs import InputUser
from utils.logger import Logger

from core.entity.component import Component

from enum import Enum


# -----------------------------------------------------------------------------
class EntityType(Enum):
    """
    Este enumerado representa los diferentes tipos de entidades que se pueden 
    manejar en la aplicación. Para agregar nuevas entidades, simplemente hay 
    que añadir una nueva línea en este enumerado con su nombre para mostrar 
    y la clase correspondiente a instanciar.
    """
    COMPONENT = ("Componente", Component)
    #DEVICE      = ("Equipo", Device)
    #DISTRIBUTOR = ("Distribuidor", Distributor)

    def __init__(self, display_name, entity_class):
        self._name = display_name
        self._class = entity_class

    def instance_entity(self): return self._class()

# -----------------------------------------------------------------------------


class EntityManager:

    def __init__(self, entity_type: EntityType):
        self._entities_dic = {}
        self._entity_type = entity_type


    # Alta de entidad (add_entity):
    # Crea un objeto de entidad según la instancia con 'enumerate'. Usado por
    # herencia en las clases hijas para dar de alta con input de usuario.
    def add_entity(self, menu, question, rule, add_loop = True):

        o = self._entity_type._name  # Nombre de la entidad (Component, etc.)

        while True:

            menu.display(True, False, True, obj="Nuevo " + o)

            #q = "Nombre/ID " + o                     # Cuestión
            #r = "alfanumérico, mínimo 3 caracteres"  # Regla

            id = InputUser.get_alphanum(question,rule,3,o,self._entities_dic)
            if id is None:
                return

            menu.display(True, False, True, obj = str(id))

            # Nueva instancia de la entidad que hereda
            entity = self._entity_type()
            
            if not entity.user_set_values(id):
                Logger.register_quit("Cancelado por usuario")
                return

            # Se procede a añadir la entidad:
            Logger.succes(o + ": ", id, " dado de alta con éxito.")
            self._entities_dic[id] = entity

            if add_loop and not Logger.there_is_the_question(
                    "\n¿Introducir otro/a "+o+"?"):
                break
        return id

    
    # Selecciona entidad mediante input de usuario. con controles
    def select_entity(self, question, rule):        
        
        o = self._entity_type._name  # Nombre de la entidad (Component, etc.)     
        
        if self._components:
            
            Logger.cancel_info()
            
            while True:               
                
                q = "Nombre/ID para acceder a menú Modificación"  # Cuestión
                r = "o 'L' para listar "+ o +"s"                  # Regla                
                
                # comprueba no existencia (activado)
                c = True 
                
                id = InputUser.get_alphanum(q, r, 3, o , self._entities_dic, c)
                
                if id is None:            # rompe este menú bucle
                    break 
                elif id.lower() == 'l':   # haz un listado
                    self.list_entities()
                else:                     # devuelve el id
                    Logger.scroll_screen()                    
                    return id
        else:
            Logger.register_quit("No existen "+ o +"s")
            return None
