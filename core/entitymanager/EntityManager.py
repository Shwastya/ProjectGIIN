# -*- coding: utf-8 -*-
"""
Proyecto: HardVIU
Created on Thu Mar 30 10:55:21 2023
@author: José Luis Rosa Maiques

Considerando que estamos haciendo la abstracción OOP considerando entidades,
Existe funcionalidad común entre ManagerComponents y ManagerDevices, sobre todo
en la gestión de entidades (Componentes, Equipos(devices), Distribuidores),
crear una clase base Manager con un atributo Dic Entities podría ser una buena 
idea para centralizar esta funcionalidad compartida con métodos genéricos.

OOP en Python:    
    https://j2logo.com/python/tutorial/programacion-orientada-a-objetos/
    
Clase base para los Managers de Entidades:
    - Componentes
    - Equipos(Devices)
    - Distribuidores    
"""

#from core.kconfig import K_USER_CANCEL
from utils.drawer import MenuDrawer
from utils.inputs import InputUser
from utils.logger import Logger

from core.entity.component import Component
from core.entity.device    import Device

from enum import Enum


# -----------------------------------------------------------------------------
class EntityType(Enum):
    """
    Este enumerado representa los diferentes tipos de entidades que se pueden 
    manejar en la aplicación. Para agregar nuevas entidades, simplemente hay 
    que añadir una nueva línea en este enumerado con su nombre para mostrar 
    y la clase correspondiente a instanciar. Hay que crear la correspondiente
    clase/módulo támbien, claro.
    """
    COMPONENT   = ("Componente", Component)
    DEVICE      = ("Equipo", Device)
    #DISTRIBUTOR = ("Distribuidor", Distributor)

    def __init__(self, display_name, entity_class):
        self._name = display_name
        self._class = entity_class

    def instance_entity(self): return self._class()

# -----------------------------------------------------------------------------


class EntityManager:

    def __init__(self, entity_type: EntityType):
        self._entities_dic = {}
        self._entity_type  = entity_type
        

    def add_entity(self, p = None):        
        """
        Crea un objeto de entidad según la instancia con 'enumerate'. 
        Utilizado en clases hijas a través de herencia para dar de alta con 
        input de usuario. El parámetro es un Dic. para hacer este método 
        lo más genérico posible.
        """
        o = self._entity_type._name # Entity Name in o
        
        if p is None: 
            Logger.error("Parámetro Dic.'p' vacio en add_entity. Entidad: "
                         + o + "\n")
            return
        
        while True:
            
            # Preguntamos a usuario por ID, mostramos -menu New Entity-
            p["menu"].display(True, False, True, obj = "Nuevo " + o)            
            id = self.set_id_from_user_input(p)           
            if id is None: 
                return
            
            # Tenemos ID, mostramos -menu 'Entity ID'-
            p["menu"].display(True, False, True, obj = str(id))
            
            # Preguntamos al usuario (llamadas InputUser). True si va bien.
            succes = self.set_data_from_user_input(id)
            if not succes:
                Logger.register_quit("Cancelado por usuario")
                return
                        
            # Mensaje de exito en la operación
            Logger.succes(o + ": ", id, " "+ p["succes"] + ".")                  
            
            # Si está activado el modo repetición
            if p["repeat"] and not Logger.there_is_the_question(
                    "\n¿Introducir otro/a "+o+"?"):
                break
            
        return id

    
    
    # Selecciona entidad mediante input de usuario. con controles
    def select_entity(self, question, tip):        
        o = self._entity_type._name  # Nombre de la entidad (Component, etc.)             
        if self._entities_dic:            
            Logger.cancel_info()            
            while True:                    
                r = question +" "+ o +"s" # Regla                                                
                c = True # comprueba no existencia (activado)                
                id = InputUser.get_alphanum(r,tip,3,o,self._entities_dic,c)                
                if id is None: break      # rompe este bucle                    
                elif id.lower() == 'l':   # haz un listado
                    self.list_entities()
                else:                     # devuelve el id
                    Logger.scroll_screen()                    
                    return id
        else:
            Logger.register_quit("No existen " + o + "s")
            return None


    # Lista todas entidades = Components del _entities_dic
    def list_entities(self, enumerated = False):        
        if not self._entities_dic:
            return False
        else:
            for i, (id, entity) in enumerate(self._entities_dic.items()):
                if enumerated:
                    Logger.draw_list(str(i + 1) + ". ", entity.display(id))
                else:
                    Logger.draw_list("\t-", entity.display(id))
            return True
        
    def modify_entity_stock(self, id, stock_order, stock_succes):        
        o = self._entity_type._name        
        Logger.cancel_info()
        if not self._entities_dic[id].user_set_values(id, stock_order):
            Logger.register_quit("Cancelado por usuario")
        else:
            Logger.success_pause(o + ": ", self._entities_dic[id].display(id),
                                 " " + stock_succes + ".", True) 

    def modify_entity_info(self, id, stock_order, modify_success):        
        o = self._entity_type._name        
        self._menu_info.display(
            True, show_options=False, show_info=True, obj=id)
        if not self._entities_dic[id].user_set_values(id, stock_order):
            Logger.register_quit("Cancelado por usuario")
        else:
            Logger.success_pause(o + ": ", self._entities_dic[id].display(id),
                                 " " + modify_success + ".", True) 

    def remove_entity(self, id, question, remove_succes):        
        o = self._entity_type._name        
        Logger.succes(o + " a dar de baja: ", id)
        if Logger.there_is_the_question(question + o.lower() + "?"): # Está seguro de que desea dar de baja este/a 
            Logger.success_pause(o +": ", id, " " + remove_succes + ".",True) # eliminado/a del sistema
            del self._entities_dic[id]
            return True
        else:
            Logger.register_quit("Cancelado por usuario")
            return False
        
        
        
        

    """ 
    Métodos auxiliares para EntityManager, no se invocan desde clases hijas 
    La responsabilidad para los inputs están todas en el archivo inputs.py
    clase 'InputUser'
    """  
    
    # Función usada en add_entity, se le pregunta al usuario por un ID
    def set_id_from_user_input(self, p):
        entity = self._entity_type._name
        id = InputUser.get_alphanum(p["question"], p["rule"], p["minim"],
                                      entity, self._entities_dic)
        return id
    
    # IMPORTANTE: La siguiente función, junto con las funciones de InputUser y
    # el enumerate EntityType, son clave, si se desea agregar más entidades.
    
    # Se cuenta con un ID y una instancia de 'entity'. Se le pregunta al 
    # usuario por todos los datos, dependiendo de la entidad instanciada y se 
    # llamará a un método específico de InputUser (separación respons.).
     
    def set_data_from_user_input(self, id):        
        
        entity = self._entity_type.instance_entity() 
        
        # Usuario define un componente
        if self._entity_type == EntityType.COMPONENT:
            entity.display_component_type_list()
            enum = entity.get_component_type_enum()
            data = InputUser.get_new_component(id, enum)
            
        if not data: return None        
        # Exito. Lo guardamos en el Diccionario de Entidades                
        self._entities_dic[id] = entity         
        return True
            

        
        