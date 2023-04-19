# -*- coding: utf-8 -*-
"""
Proyecto: HardVIU
Created on Thu Mar 30 10:55:21 2023
@author: José Luis Rosa Maiques

Considerando que estamos haciendo la abstracción OOP y considerando entidades,
Existe funcionalidad común entre ciertos managers, sobre todo en la gestión de 
entidades (Componentes, Equipos(devices), Distribuidores), crear una clase 
base Manager con un atributo Dic Entities en común podría ser una buena idea
para centralizar esta funcionalidad compartida con métodos genéricos.
Aunque seguramente sea complicarlo todo ya que estamos en Python no en C++.

Clase base para los Managers de Entidades:
    - Componentes
    - Equipos(Devices)
    - Distribuidores    
"""

#from core.kconfig import K_USER_CANCEL
from utils.drawer import MenuDrawer
from utils.inputs import InputUser
from utils.logger import Logger

from core.entity.component import ComponentType
from core.entity.component import Component
from core.entity.device    import Device

from enum import Enum
# -----------------------------------------------------------------------------
class EntityType(Enum):
    """
    Este enumerado representa los diferentes tipos de entidades que se pueden 
    manejar en la aplicación. Para agregar nuevas entidades, hay que añadir 
    una nueva línea en este enumerado con su nombre para mostrar y la clase 
    correspondiente a instanciar, más los siguientes 2 puntos:
    
        1. Hay que crear la correspondiente clase/módulo.
        2. Hay que crear la lógica de entrada de datos en InputUser
        
    """
    COMPONENT   = ("Componente", Component)
    DEVICE      = ("Equipo", Device)
    #DISTRIBUTOR = ("Distribuidor", Distributor)

    def __init__(self, display_name, entity_class):
        self._name  = display_name
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
        
        # if self.check_for_error(p): return
        name = self._entity_type._name
        
        while True:
            
            id = self.display_menu_and_check_id(p)        
            if id is None: 
                return
            
            # Tenemos ID, mostramos -menu 'Entity ID'-
            # NOTA: Usar aquí un menu de una clase hija creo que es un fallo
            # al repartir responsabilidades. Se debería intentar correguir
            p["menu"].display(True, False, True, obj = str(id)) 
            
            # Preguntamos al usuario (llamada a InputUser). True si va bien.
            data = self.set_data_from_user_input(id, p)
            if data is None:
                # None: es cuando cancela el usuario
                Logger.register_quit("Cancelado por usuario")
                return
            elif not data: 
                # Si no es None pero no llegan datos ha habido algún fallo
                Logger.register_quit(p["fail"])
                return False
                        
            # Exito! Guardamos valores y añadimos al diccionario de Entidades 
            # Cada diccionario pertenece a la instancia especifica en uso
            entity = self._entity_type.instance_entity() 
            entity.set_from_user_data(data)               
            self._entities_dic[id] = entity         
            
            # Mensaje de exito en la operación
            Logger.success(name + " ", id, " " + p["success"] + ".")                  
            
            # Si está activado el modo repetición, se pregunta si quiere
            # añadir otra entidad
            if p["repeat"] and not Logger.there_is_the_question(
                    "\n¿Introducir otro/a "+ name +"?"):
                break
            
    
    def select_entity(self, p, pre_list = False, op_list = 'l'):       
        """
        Utilizamos el mismo método para obtener el ID ingresado por el usuario,
        manejo de errores en InputUser, opción de listado o devuelve el ID.
        La devolución del ID es útil para acceder a otro menú en la clase hija.
        
        El parametro True actica el non_check para la función del InputUser,
        de ese modo cambiamos la búsqueda a comprobación de existencia.   
        """
        if self._entities_dic:             
                       
            if pre_list: self.list_entities() # Si se muestra lista antes
            while True:    
                Logger.cancel_info() 
                id = self.set_id_from_user_input(p, True)  
                if id is None: break               
                elif id.lower() == op_list:   # haz un listado
                    self.list_entities()
                else:                         # devuelve el id
                    Logger.scroll_screen()                    
                    return id
    
    
    def update_entity_based_on_mode(self, p):
        
        if "menu" in p: id = self.display_menu_and_check_id(p)
        else:
            Logger.cancel_info()
            id = p["id"] 
            
        mode = p["mode"]
        if mode == "remove":
            return self.remove(id, p)
        
        data = self.set_data_from_user_input(id, p)        
        if data is None: 
            Logger.register_quit("Cancelado por usuario")
            return    
        elif not data: 
            # Si no es None pero no llegan datos ha habido algún fallo
            Logger.register_quit(p["fail"])
            return False
            
        if   mode == "stock":
            self._entities_dic[id].set_quantity(data)
        elif mode == "modify":
            self._entities_dic[id].set_from_user_data(data)
        
            
        ent = self._entity_type._name    
        Logger.success_pause(ent + " ", id, " " + p["success"] + ".",True)    
    
        
    def dic_len_ctrl(self, mini, maxi):
        """
        Función para controlar el número de opciones a mostrar en un menu
        en la clase hija (mala asignación de responsabilidad)        
        """
        n_ops = mini
        if len(self._entities_dic.items()) > 0: n_ops = maxi                
        return n_ops
        
        
    """ 
    Métodos auxiliares para EntityManager, no se deben invocar desde hijos. 
    La responsabilidad para los inputs están todas en el archivo 'inputs.py'
    clase 'InputUser'
    """      
    
    def remove(self, id, p):        
        """
        Acciones a realizar antes de eliminar un entidad
        """
        action   = p["action"]
        question = p["question"]
        success  = p["success"]
        
        ent = self._entity_type._name  
        
        Logger.success(action + ": ", id)
  
        if Logger.there_is_the_question(question + "?"):
            
            Logger.success_pause(ent + " ", id, " " + success + ".", True) 
            
            if self._entity_type == EntityType.COMPONENT:             
                # no se necesita control alguno 
                # no lo elimino para que se entienda la lógica que aplico
                pass 
                
            if self._entity_type == EntityType.DEVICE:
                # necesitamos recuperar los componentes 
                # antes de eliminar el equipo
                comp_list = p["device"].get_components_list()               
                p["manager"].update_stock_by_component_list(comp_list, 1)
                    
            del self._entities_dic[id]
            return True
        else:
            Logger.register_quit("Cancelado por usuario")
            return False   
        
        
        
    def check_for_error(self, p):
        """
        Esta función es muy tonta, me complico la vida. Tanto control
        de errores, en errores que no pueden ocurrir al menos que se trabaje
        en la implementación, pierden sentido en un trabajo finito.        
        """
        if p is None: 
            Logger.error("Parámetro Dic.'p' vacio en EntityManager. Entidad: "
                         + self._entity_type._name + "\n")
            return True
        return False
    
    def display_menu_and_check_id(self, p):       
        
        if self.check_for_error(p): return
        
        if not 'id' in p: # Alta de una entidad, ya que no tenemos ID
        
            # Mostramos -menu New Entity-
            p["menu"].display(True, False, True, obj = "Nuevo " 
                         + self._entity_type._name)               
            # Preguntamos a usuario por ID,
            id = self.set_id_from_user_input(p)       
            return id
        
        # Si tenemos 'id' no es Alta, es modificación de Entidad
        id = p["id"]
        p["menu"].display(True, False, True, obj = str(id))
        return id  
    
    def list_entities(self, enumerated = False):        
        if not self._entities_dic:
            return False
        else:
            for i, (id, entity) in enumerate(self._entities_dic.items()):
                #if enumerated:
                #    Logger.draw_list(str(i + 1) + ". ", entity.display(id))
                #else:
                Logger.info_bold(entity.display(id))
            return True
        
    
    # Función usada en add_entity, se le pregunta al usuario por un ID
    def set_id_from_user_input(self, p, check_non = False):
        entity = self._entity_type._name
        id = InputUser.get_alphanum(p["question"], p["rule"], p["minim"],
                                      entity, self._entities_dic, check_non)
        return id    
    
    def set_data_from_user_input(self, id, p = None):    
        """
        IMPORTANTE: Esta función, junto con las funciones de InputUser y
        el enumerate EntityType son clave si se desea agregar más entidades.
        
        Se cuenta con un ID y una instancia de 'entity'. Se le pregunta al 
        usuario por todos los datos, dependiendo de la entidad instanciada y 
        se llamará a un método específico de InputUser.
        """ 
        mode = p["mode"]
        
        # Añadir o modificar Componente
        if self._entity_type == EntityType.COMPONENT:
            data = InputUser.get_new_component(id, ComponentType, mode)
        
        # Añadir o modificar Equipo
        elif self._entity_type == EntityType.DEVICE:
            data = InputUser.get_new_device(id, p, ComponentType)           
            
        return data
    
    
            

        
        