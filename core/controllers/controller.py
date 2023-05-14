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
        
        self._model     = model_type      
        self._controller= ModelFactory.create_controller(self._model,self._dic)   
        
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
            
    # nombre en plural y dic
    def list_models_from_dic(self, name = None, aux_dic = None, f = None): 
        """
        Lista el diccionario de modelos del tipo modelo instanciado.
        'enumerated' permite escoger entre un listado normal o enumerado.
        
        Devuelve 'False' si diccionario vacio, 'True' en caso contrario.
        """
        dic = self._dic
        plural_name = Logger.pluralize(self._model._name)
        if aux_dic is not None: 
            
            dic = aux_dic
            plural_name = Logger.pluralize(name)   
        
        if not dic: return False
        else:  
                     
            # f -> es el mensaje indicando los filtros aplicados
            t = "en el sistema"
            if f is not None: t = '[' + f + ']'
            
            title = "Registro de '"+ plural_name + "' " + t             
            Logger.box_title(title)                       
            
            total_models = len(dic)            
            
            # Buscamos la longitud del ID más largo. (por embellecer display)
            max_id_len = max(len(str(id)) for id in dic.keys())            
            
            for i, (id, model) in enumerate(dic.items()): 
                
                
           
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

    def filter_models(self, dic, filt):
        """
        Filtra los modelos en el diccionario 'dic' según el criterio 'filt'.
        Retorna un diccionario con los modelos filtrados.
        """
        filtered_dic = {}
        for id, model in dic.items():
            if model.get_status() in filt: filtered_dic[id] = model
        return filtered_dic
    
    
    def select_model_from_dic(self, aux_dic = None, model_name = None, 
                              need_list = True, f = None): 
        """        
        Permite al usuario ingresar un ID o un índice y se comprobará su 
        existencia. Se da opción a mostrar el listado.
        """                          
        
        dic   = self._dic.items()
        model = self._model._name
        
        if aux_dic is not None: 
            # VALE ya! me faltaba sacar los .items() que desastre!
            # No te olvides de esta experiencia, por poca cosa, el horror
            dic   = aux_dic.items()
            model = model_name
        
        plural_name = Logger.pluralize(model)  
        info = "Diccionario '" + plural_name + "' vacio.\n"
        warn = "No hay '" + plural_name + "' disponibles en el sistema."
        
        # El añadir user_cancellation es para poder recordar mejor 
        # la lógica de esta función en el futuro
        
        user_cancellation = False
        
        while True:   
            models = list(dic)       
            if not models:
                Logger.Core.info(info)
                Logger.Core.warn(warn)
                return None, user_cancellation                   
            
            id, m, l = InputUser.get_valid_model(self._id_config["question"],
                                                 self._id_config["rule"],
                                                 models, need_list = True,
                                                 has_shown_list = need_list)            
            # El usuario pide lista
            if l:
                need_list = True # Aqui tambien
                self.list_models_from_dic(plural_name, aux_dic, f)
                self._id_config["question"] = "Nombre/ID o número de la lista"
                self._id_config["rule"    ] = "('l' listar de nuevo) = "
                continue
            if id is None and m is None: 
                user_cancellation = True
                return None, user_cancellation
                                           
            return id, user_cancellation   
    
    def select_model(self, model_dic, name, pre_list, info = True, f = None):   
        """
        Recordar que devuelve tupla (id, user_cancellation).
        user_cancellation es un bool para saber si es cancelación de usuario
        el None de los datos recibidos, o es por otro motivo.
        
        Permite tambien pasar un filtro que hace una selección de los modelos
        a mostrar (de momento solo lo implementa el modelo Dispatch(Despacho))
        """
        self._id_config["question"] = "Nombre/ID de componente"        
        self._id_config["rule"] = "(o 'l' para mostrar lista) = " 
        
        if pre_list: 
            self._id_config["question"] = "Nombre/ID o número de la lista"
            self._id_config["rule"] = "('l' listar de nuevo) = "
            self.list_models_from_dic(name, model_dic, f)
            
        if info: Logger.UI.cancel_info(level = 1)        
        
        return self.select_model_from_dic(model_dic,name, pre_list, f)   
        
    def modify_model_info(self, id):
        data = self._controller.set_modify_data_from_user(id)
        if not data: return None      
        self._dic[id].set_from_user_data(data)
        return True
    
    def ask_this_question(self, question):
        return InputUser.ask_yes_no_question("¿" + question + "?")
        
            
 