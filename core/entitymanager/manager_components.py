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

En una decisión de diseño posterior, trasladamos las funcionalidades y el Dic
a una clase padre llamada EntityManager. El resto de entidades se heredarán 
de ella, utilizando métodos genéricos que a su vez emplearán clases de entidad 
específicas. 

En una primera versión, se implementó el atributo 'components' como una lista,
lo que requería que muchas funciones iteraran sobre ella para llevar a cabo su 
lógica. Estaba nanejando la lista como lo haría en C++. Transformar 
'components' en un diccionario lo hace más eficiente en este caso.

List vs Tuples vs Sets vs Dictionaries: 
    https://realpython.com/python-data-structures/   
"""

from utils.drawer import MenuDrawer
from utils.logger import Logger

from core.entitymanager.EntityManager import EntityType, EntityManager


# borrar solo es para pruebas ------------------
from core.entity.component import Component
# ----------------------------------------------

# La clase ManagerComponents hereda de la clase EntityManager e implementa sus 
# métodos, que tienen como objetivo ser genéricos para todas las entidades.
class ManagerComponents(EntityManager):

    def __init__(self):
        super().__init__(EntityType.COMPONENT)

        # Menu principal
        self._menu_comp = MenuDrawer("HardVIU / 1) Componentes", [
            "Alta", "Modificación", "Listar Componentes"], 1)

        # Submenu nueva alta
        self._menu_add = MenuDrawer("HardVIU / 1) Componentes / 1) Alta")

        # Submenu modificación componente
        self._menu_modi = MenuDrawer(
            "HardVIU / 1) Componentes / 2) Modificación", [
                "Cambiar stock", "Cambiar información", "Dar de baja"])

        # Submenu cambiar información
        self._menu_info = MenuDrawer("HardVIU / 1) Componentes / 2) " + 
                                     "Modificación / 2) Cambiar información")    
        
        
        c1 = Component()        
        c1.set_values("Fuente", 120, 85.0, 3)
        self._entities_dic["cp1"] = c1        
        c2 = Component()        
        c2.set_values("Fuente", 230, 110.0, 2)
        self._entities_dic["cp2"] = c2
        
        c3 = Component()        
        c3.set_values("PB", 123, 44.0, 1)
        self._entities_dic["cp3"] = c3
        c4 = Component()        
        c4.set_values("PB", 87, 23.0, 1)
        self._entities_dic["cp4"] = c4
        c5 = Component()        
        c5.set_values("PB", 302, 299.0, 1)
        self._entities_dic["cp5"] = c5
        
        c6 = Component()        
        c6.set_values("TG", 47, 13.0, 2)
        self._entities_dic["cp6"] = c6        
        c7 = Component()        
        c7.set_values("TG", 77, 21.0, 1)
        self._entities_dic["cp7"] = c7
        
        
        c8 = Component()        
        c8.set_values("CPU", 32, 220.0, 1)
        self._entities_dic["cp8"] = c8
        c9 = Component()        
        c9.set_values("CPU", 39, 250.0, 2)
        self._entities_dic["cp9"] = c9
        
        c10 = Component()        
        c10.set_values("RAM", 68, 120.0, 3)
        self._entities_dic["cp10"] = c10
        
        
        c11 = Component()        
        c11.set_values("Disco", 123, 110.0, 1)
        self._entities_dic["cp11"] = c11
        c12 = Component()        
        c12.set_values("Disco", 160, 159.0, 1)
        self._entities_dic["cp12"] = c12
        c13 = Component()        
        c13.set_values("Disco", 160, 159.0, 1)
        self._entities_dic["cp13"] = c13
    
    def add_component(self, repeat = True): # Alta de componente
    
        p = {"mode"     : "add", 
             "menu"     : self._menu_add,                      # Menu de alta
             "question" : "Nombre/ID de componente:",          # Pregunta input
             "rule"     : "alfanumérico, mínimo 3 caracteres", # regla en input
             "minim"    : 3,                                   # min. chars
             "success"  : "dado de alta con éxito",            # exito alta
             "repeat"   : repeat,                              # activa repetic
             "manager"  : None, 
             "fail"     : "Alta de componente cancelada" }         
        #return super().add_entity(p)   
        return super().manage_entity(p)   
    

    def select_component(self, pre_list):  
        p = {"question" : "Nombre/ID del componente a modificar",
             "rule"     : "o 'L' para listar", "minim": 3 }
        return super().select_entity(p, pre_list)
    
    def modify_stock(self, id):
        p = {"mode"     : "stock",
             "id"       : id,  
             "success"  : "Stock modificado con exito"}
        #super().update_entity_based_on_mode(p)   
        super().manage_entity(p)   
        
    def modify_info(self, id):
        p = {"mode"     : "modify", 
             "id"       : id, 
             "menu"     : self._menu_info,             
             "success"  : "modificado con exito"}
        #super().update_entity_based_on_mode(p)
        super().manage_entity(p)   
        
    def remove_component(self, id):        
        p = {"mode"     : "remove",
             "id"       : id ,
             "action"   : "Componente a dar de baja",
             "question" : "Seguro de que desea dar de baja este componente",
             "success"  : "eliminado del sistema"}
        #return super().update_entity_based_on_mode(p)
        return super().manage_entity(p)   
            
    def update_stock_by_component_list(self, component_list, increment): 
        """
        Por ejemplo, se ha guardado en una lista temporal de componentes
        al dar de baja un equipo, podemos usar esta función para actualizar
        el stock usando la función de la clase Component 'update_quantity'
        """
        for comp_id in component_list:
            updated = self._entities_dic[comp_id].update_quantity(increment)
            if not updated:
                Logger.warn("Stock de componente " + comp_id + " es menor a 0.")
            
    """  Función a llamar desde 'System' """
    def update(self): 
        
        atras = "Menú anterior"            
        while True:             
            self._menu_comp.set_max_options(super().dic_len_ctrl(1, 3))            
            self._menu_comp.display(zero = atras)            
            option = self._menu_comp.get_option()  
            
            if option == 1: self.add_component() # Alta componente   
                 
            elif option == 2 or option == 3:     # Sub Menú Modificación  
            
                id = self.select_component(False if option < 3 else True)
                if not id: continue
                while True:
                    self._menu_modi.display(True, True, obj=id, zero = atras)
                    option = self._menu_modi.get_option()    
                    
                    if option == 0:                  # Salir de modificación
                        Logger.scroll_screen()
                        break
                    elif option == 1:                # Cambiar stock            
                        self.modify_stock(id)
                        continue
                    elif option == 2:                # Cambiar información
                        self.modify_info(id)
                        continue
                    elif option == 3:                # Dar de baja                    
                        if self.remove_component(id): break
                        continue
                    else: Logger.bad_option()
            elif option == 0: break             # Salir de menu Componentes
            else: Logger.bad_option()           # Opción no encontrada
