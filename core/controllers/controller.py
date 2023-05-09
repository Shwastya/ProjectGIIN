# -*- coding: utf-8 -*-
"""
Proyecto: HardVIU
Creado el viernes 24 de marzo a las 16:18:11, 2023
Autor: José Luis Rosa Maiques

EL Controlador se encarga de gestionar la lógica de negocio de los modelos:
Componentes (Components)
Equipos (Devices)
Etc.

Esta clase actúa como clase base para los diferentes menús, que se definen como
clases derivadas de ella. La clase se implementa siguiendo el patrón de diseño 
Factory Method. Dependiendo del tipo de modelo, se instancia también un 
controlador con métodos específicos para dicho modelo. Tambien, esta clase
cuenta ya con métodos definidos que son genericos a todos los modelos
"""

from core.views.logger import Logger
from core.views.drawer import Displayer

from core.controllers.model_factory import ModelFactory, ModelType  
from core.controllers.inputs        import InputUser, K_LIST

class Controller:

    def __init__(self, model_type: ModelType):     
        
        self._dic        = {} # Dic. base que heredan todos los modelos
        
        self._model      = model_type      
        self._controller = ModelFactory.create_controller(self._model, 
                                                          self._dic)   
        
        self._id_config = {"question": "Nombre/ID de " + self._model._name,
                           "rule"    : "alfanumérico, mínimo 3 caracteres", 
                           "minim"   : 3,   # caracteres mínimos por defecto
                           "maxim"   : 100} # caracteres máximos por defecto
    
    def get_id(self, need_list = False):        
        """
        Función que pregunta al usuario por un ID para el modelo.
        """        
        return InputUser.get_str(self._id_config["question"], 
                                 self._id_config["rule"    ], 
                                 self._id_config["minim"   ],
                                 self._id_config["maxim"   ], need_list)       
    
    def check_id(self, id, auxiliar_dic = None):   
        """
        Función que comprueba si el id está en el diccionario. Podría darse 
        el caso que no se quiera comprobar el diccionario propio del 
        controlador especifico, en se esa caso se puede pasar un 
        diccionario auxiliar
        """
        dic = auxiliar_dic if auxiliar_dic is not None else self._dic        
        if id in dic: return True
        return False
    
    def get_and_check_id(self, mode = "", auxiliar_dic = None):
        
        id = self.get_id()
        if id is None: return None
        result = self.check_id(id)
        
        if result:
            if mode == "add":
                warn = "El identificador ya existe. Inténtelo de nuevo."
                Logger.Core.warn(warn)
                Logger.pause()
                return result       
        return id
            
    
    def new_model(self, id): 
        """
        Crea una instancia del modelo (FACTORY method)
        Usa la función del controller instanciado para invocar 
        los inputs al usario.        
        
        Devuelve 'None'  Si el usuario ha cancelado desde 'InputUser'
        Devuelve 'True'  Si el alta se ha hecho correctamente        
        
        Hay que asegurarse que todos los 'controllers' implementen está función.        
        """    
        data  = self._controller.get_model_data_from_user(id)            
        if not data: return None      
        
        # FACTORY method y metodo del modelo para guardar datos
        model = ModelFactory.create_model(self._model)
        model.set_from_user_data(data)        
        self._dic[id] = model
        return True    
            
    def list_models_from_dic(self): 
        """
        Lista el diccionario de modelos del tipo modelo instanciado.
        'enumerated' permite escoger entre un listado normal o enumerado.
        
        Devuelve 'False' si diccionario vacio, 'True' en caso contrario.
        """
        if not self._dic: return False
        else:
            
            plural_name = Logger.pluralize(self._model._name)            
            title = "Registro de '" + plural_name.upper() + "' en el sistema"            
            Logger.box_title(title)                       
            
            total_models = len(self._dic)
            
            # Buscamos la longitud del ID más largo. (por embellecer display)
            max_id_len = max(len(id) for id in self._dic.keys())
            
            for i, (id, model) in enumerate(self._dic.items()):
                is_last_model = i == total_models - 1
                
                # Todos los modelos usan la misma definición de función.
                # Hay que tener en cuenta que los modelos llaman a sus 
                # respectivas versiones de esta función en Drawer.Displayer
                
                # TODO: Hay un pequeño error de diseño, no todas las funciones
                # necesitan los mismo parametros (pequeñas diferencias). Pero
                # al querer hacerlo generico, todas necesitan la misma estruct.
                
                model.display(id, 
                              col        = True,              # Coloreado
                              tab        = True,              # Tabulado
                              p_l        = not is_last_model, # Sep. con lineas
                              max_id_len = max_id_len,        # el ID más largo
                              idx        = i + 1)             # valor enum
            return True


    def select_model_from_dic(self): 
        """        
        Permite al usuario ingresar un ID o un índice y se comprobará su 
        existencia. Se da opción a mostrar el listado.
        """                          
        while True:   
            models = list(self._dic.items())       
            if not models:
                Logger.Core.warn("No hay modelos disponibles en la lista.")
                return None
                
            self._id_config["question"] = "Ingrese ID o número de lista"
            self._id_config["rule"    ] = "('l' para listar) = "            
            
            id, m, l = InputUser.get_valid_model(self._id_config["question"],
                                                 self._id_config["rule"],
                                                 models, need_list = True)            
            # El usuario pide lista
            if l:
                self.list_models_from_dic()
                continue
            if id is None and m is None: return None

            #Logger.scroll_screen()                                    
            return id  
        
        
    def modify_model_info(self, id):
        data = self._controller.set_modify_data_from_user(id)
        if not data: return None      
        self._dic[id].set_from_user_data(data)
        return True
    
    def ask_this_question(self, question):
        return InputUser.ask_yes_no_question("\n¿" + question + "?")
        
            
 