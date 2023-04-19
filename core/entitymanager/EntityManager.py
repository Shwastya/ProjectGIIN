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
#from utils.drawer import MenuDrawer
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
            
    def manage_entity(self, p):

        # Controles básicos de los parametros pasados en el Dic. p
        mode = p["mode"]
        name = self._entity_type._name    
        if "repeat" in p: repeat = p["repeat"]
        else: repeat = False
        
        # En caso de querer mostrar un menu personalizado más comprobación ID
        if "menu" in p:         
            id = self.display_menu_and_check_id(p)
            p["menu"].display(True, False, True, obj = str(id))
        else:
            Logger.cancel_info()
            id = p["id"]
        if id is None: return
        
        # Si tan solo se pretende borrar. Llamamos a función: return remove(..) 
        if mode == "remove": return self.remove(id, p)        
        
        # Si el modo es    "add" -> Se crea una nueva instancia de entidad
        # Si el modo no es "add" -> Estamos accediendo a una entidad existente
        
        if mode == "add": entity = self._entity_type.instance_entity()        
        else: entity = self._entities_dic[id]        

        # Invocación InputUser. Preguntamos a usuario lo necesario en este caso
        data = self.set_data_from_user_input(id, p)
        
        # None: es cancelación del usuario 
        if data is None:            
            Logger.register_quit("Cancelado por usuario")
            return
        # False: es que no llegan datos. Ha habido algún fallo            
        elif not data: 
            Logger.register_quit(p["fail"])
            return False

        # Dependiendo del "modo", la lógica correspondiente a cada entidad 
        # debe implementarse en las diferentes entidades, manteniendo 
        # nombres de métodos iguales en todas ellas. 
       
        if   mode == "add":
            entity.set_from_user_data(data)
            self._entities_dic[id] = entity
        elif mode == "stock" : entity.set_quantity(data)
        elif mode == "modify": entity.set_from_user_data(data)
        
        
        # Pause en la siguiente función es "Presione [ENTER] para continuar".
        # Si está activado el modo repetición, no queremos esa pausa.
        Logger.success_pause(name + " ", id, " " 
                             + p["success"] + ".", True, no_pause = repeat)

        # Si está activado el modo repetición, preguntará si quiere realizar
        # de nuevo la acción -llamada recurrente-
        if repeat and Logger.there_is_the_question(
                "\n¿Introducir otro/a " + name + "?"):
            self.manage_entity(p)
            return

    def select_entity(self, p, pre_list = False, op_list = 'l'):       
        """        
        El parametro True actica el non_check para la función del InputUser,
        de ese modo cambiamos de pregunta a comprobación de existencia.   
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
    
    def display_menu_and_check_id(self, p):  
        
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
        
        if not self._entities_dic: return False
        else:
            for i, (id, entity) in enumerate(self._entities_dic.items()):
                if enumerated:
                    Logger.draw_list(str(i + 1) + ". ", entity.display(id))
                else:
                    Logger.info_bold(entity.display(id))
            return True
        
    
    
    def set_id_from_user_input(self, p, check_non = False):
        """
        Función que pregunta al usuario por un ID. Con non_check 
        cambiamos de pregunta a comprobación de existencia.
        """
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
                # no se necesita control alguno, se mantiene como pista de log.
                pass 
                
            if self._entity_type == EntityType.DEVICE:
                # necesitamos recuperar los componentes al desmontar equipo
                comp_list = p["device"].get_components_list()               
                p["manager"].update_stock_by_component_list(comp_list, 1)
                    
            del self._entities_dic[id]
            return True
        else:
            Logger.register_quit("Cancelado por usuario")
            return False   
    
    
            

        
        