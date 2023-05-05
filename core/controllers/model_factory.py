# -*- coding: utf-8 -*-
"""
Project: HardVIU
Created on Wed Apr 19 22:05:31 2023
@author: José Luis Rosa Maiques

Vamos a implementar el patrón de diseño Factory Method. Este patrón se utiliza 
para tratar a objetos abstractos que representan diferentes tipos de modelos
dentro de nuestro sistema. Estos modelos serán almacenadas en diccionarios y 
gestionadas de manera unificada. Algunas de los modelos consideradas en el 
sistema incluyen:
    
    - Componentes (Components)
    - Equipos     (Devices)
    - Etc..

El objetivo de aplicar el patrón Factory Method es separar la lógica de 
creación de estos modelos de las clases que las manejan, permitiendo mayor 
flexibilidad y escalabilidad para posibles ampliciones.
"""

from enum import Enum

from core.models.component   import Component
from core.models.device      import Device
from core.models.distributor import Distributor
from core.models.dispatch    import Dispatch

from core.controllers.component_controller   import ComponentController
from core.controllers.device_controller      import DeviceController
from core.controllers.distributor_controller import DistributorController
from core.controllers.dispatcher_controller  import DispatcherController

class ModelType(Enum):
    
    COMPONENT   = ("Componente"  , Component   , ComponentController)
    DEVICE      = ("Equipo"      , Device      , DeviceController)
    DISTRIBUTOR = ("Distribuidor", Distributor , DistributorController)
    DISPATCH    = ("Despachos"   , Dispatch    , DispatcherController)

    def __init__(self, display_name, model_class, controller_class):
        
        self._name             = display_name
        self._model_class      = model_class 
        self._controller_class = controller_class 

    def instance_model(self):
        return self._model_class()
    
    def instance_controller(self, dic):
        return self._controller_class(dic)

class ModelFactory:  
    
    @staticmethod
    def create_model(model_type: ModelType):
        model = model_type.instance_model()        
        return model

    @staticmethod
    def create_controller(model_type: ModelType, dic):
        controller = model_type.instance_controller(dic)
        return controller
    
    
    
