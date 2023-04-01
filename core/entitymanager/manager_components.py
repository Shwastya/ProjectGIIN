# -*- coding: utf-8 -*-
"""
Proyecto: HardVIU
Created on Fri Mar 24 16:18:11 2023
@author: José Luis Rosa Maiques

El ManagerComponent se encarga de gestionar los Componentes, proporcionando 
una lógica de menú. La estructura de datos y la funcionalidad de la entidad 
Componente se mantienen en la clase Componente, mientras que el Manager no 
necesita conocer su funcionamiento interno, puesto que tiene un Dic de 
componentes solo conoce y maneja su Identificador (ID) como Key del Dic.

En una primera versión, se implementó el atributo 'components' como una lista,
lo que requería que muchas funciones iteraran sobre ella para llevar a cabo su 
lógica. Estaba nanejando la lista como lo haría en C++.

Transformar 'components' en un diccionario lo hace más eficiente en este 
caso, ya que no es necesario iterar linealmente sobre él. El único listado 
que requerimos lineal se encuentra en los tipos de componentes, ubicados 
en un enum en el archivo component.py -> ComponentType (enum class)


List vs Tuples vs Sets vs Dictionaries: 
    https://realpython.com/python-data-structures/
    

En una decisión de diseño posterior, trasladamos las funcionalidades y el Dic
a una clase padre llamada EntityManager. El resto de entidades se heredarán 
de ella, utilizando métodos genéricos que a su vez emplearán clases de entidad 
específicas.    
"""


from utils.drawer import MenuDrawer
from utils.logger import Logger

from core.entitymanager.EntityManager import EntityType, EntityManager

# NOTA IMPORTANTE:
# Evaluamos Herencia (ahorro en código) frente a Composición (flexibilidad)
# La clase ManagerComponents hereda de la clase EntityManager e implementa sus 
# métodos, que tienen como objetivo ser genéricos para todas las entidades.

class ManagerComponents(EntityManager):

    def __init__(self):
        super().__init__(EntityType.COMPONENT)

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
        self._menu_info = MenuDrawer("HardVIU / 1) Componentes / 2) " + 
                                     "Modificación / 2) Cambiar información")            
       
    def get_components_dic(self): # Método get para acceso a componentes
        """ NOTA:
        se debe acceder directamente al atributo _entities_dic de la instancia 
        actual, ya que super() se utiliza para acceder a métodos y atributos
        """
        return self._entities_dic    
    
    def add_component(self, repeat = True): # Alta de componente
    
        p = {"menu"    : self._menu_add,                     # Menu de alta
             "question": "Nombre/ID componente:",            # Pregunta input
             "rule"    : "alfanumérico, mínimo 3 caracteres",# regla en input
             "minim"   : 3,                                  # min. chars
             "succes"  : "dado de alta con éxito",           # exito alta
             "repeat"  : repeat,                             # activa repetic
             "is_add"  : True }                              # llamada Alta    
         
        return super().add_entity(p)

    # Selecciona entidad = Component mediante input de usuario con controles
    def select_component(self):  
        p = {"Nombre/ID para acceder a menú Modificación","o 'L' para listar"}
        return super().select_entity(p)
    
    def modify_stock(self, id):
        prmtrs = {"stock": "Nueva cantidad"}
        super().modify_entity_stock(id, "stock actualizado", prmtrs)
        
    def modify_info(self, id):
        super().modify_entity_info(id, "Cantidad", "modificado con éxito")
        
    def remove_component(self, id):
        return super().remove_entity(id,
                                     "Seguro de que desea dar de baja este",
                                     "eliminado del sistema")
            
    """  Función a llamar desde sistema """
    def update(self): 
        while True:
            self._menu_comp.display()
            option = self._menu_comp.get_option()
            if option == 1: self.add_component() # Alta componente                    
            elif option == 2:                    # Sub Menú Modificación           
                id = self.select_component()
                if id is None: continue
                while True:
                    self._menu_modi.display(True, True, obj = id)
                    option = self._menu_modi.get_option()                    
                    if option == 0:                # Salir de modificación
                        Logger.scroll_screen()
                        break
                    elif option == 1:              # Cambiar stock            
                        self.modify_stock(id)
                        continue
                    elif option == 2:              # Cambiar información
                        self.modify_info(id)
                        continue
                    elif option == 3:              # Dar de baja                    
                        if self.remove_component(id): break
                        continue
                    else: Logger.bad_option()
            elif option == 0: break             # Salir de menu Componentes
            else: Logger.bad_option()           # Opción no encontrada
