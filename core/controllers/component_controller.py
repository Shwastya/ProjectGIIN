# -*- coding: utf-8 -*-
"""
Proyecto: HardVIU
Created on Fri Apr 21 22:28:07 2023
@author: José Luis Rosa Maiques

Métodos específicos para el controlador del tipo de modelo 'Component'. 
La herencia del controlador se realiza sobre modelos específicos como 
'ComponentController' mediante composición, compartiendo el diccionario origen 
desde el controlador base.
"""
from config.DEBUG import debug_components # Debug y testeo

from core.controllers.inputs import InputUser
from core.models.component   import ComponentType
from core.views.logger       import Logger

# provisional
from core.models.component   import Component

class ComponentController:
    def __init__(self, component_dic):
        self._component_dic = component_dic      
        
        # Con propositos de testeo/debug. Se activa desde settings.py        
        debug_components(self._component_dic)        
       
        
    """
    Las siguiente funciones son privadas para uso de la misma clase
    """
    
    def __get_type_from_user(self, id):        
        
        ComponentType.display()        
        
        msg1 = "Elija un número de la lista para el tipo de componente = "
        msg2 = "El Tipo de componente no está en la lista."   
        
        tipo = InputUser.get_from_enum(ComponentType, msg1, msg2)
        if tipo is None    : return False
        temp = "<── (" + tipo.value + ":" + ' "' + id + '"'
        Logger.Core.info(temp + ")\n")          
        return tipo        
    
    def __get_weight_from_user(self, msg):
        peso = InputUser.get_uint("Peso en gramos del componente = ")
        if peso is None    : return False
        Logger.Core.info(msg + '. ' + str(peso) + ' gramos)\n') 
        return peso        
    
    def __get_price_from_user(self, msg):
        precio = InputUser.get_float("Precio en euros del componente = ")
        if precio  is None  : return False
        Logger.Core.info(msg  + '. ' + str(precio) + ' euros)\n')     
        return precio        
    
    def __get_quantity_from_user(self, msg):
        cantidad = InputUser.get_uint("Cantidad de componentes = ")
        if cantidad is None : return False           
        Logger.Core.info(msg + '. ' + str(cantidad) + ' stock)\n')
        return cantidad
    
    """
    A partir de aquí son funciones públicas.
    """
        
    def get_dic(self): 
        return self._component_dic            
    
    def there_are_components_in_system(self):
        """
        Esta función comprueba que existan componentes en el sistema.
        Informa y devuelve False si está vacio. 
        True si tenemos algún componente (aunque sea uno solo)
        """            
        if len(self._component_dic) == 0:
            warn  = "Agregue componentes desde el menú de Componentes."
            error = "¡Stock de componentes vacío! Registro cancelado..."
            Logger.Core.error_warn_pause(error, warn)
            return False    
        return True
    
    def check_at_least_one_of_each_type(self):
        """
        Comprueba si hay al menos un componente de cada tipo en el diccionario
        y si su cantidad es mayor que cero.
        Devuelve True o False.       
        """
        component_types = set()
        
        # Recorremos el diccionario de componentes
        for component in self._component_dic.values():
            
            # Verificamos si el componente tiene cantidad mayor a 0
            if component._cantidad > 0: component_types.add(component._tipo)
            
            # Si hemos encontrado un componente de cada tipo, rompemos bucle
            if len(component_types) == len(ComponentType): return True
    
        # Si no se encontró un componente de cada tipo con cantidad mayor a 0
        return False
        
    


    # ADD -COMPONENTS-
    def get_model_data_from_user(self, id):
        """
        La función pregunta al usuario por los datos del componente.    
        Devuelve 'False' si el usuario ha cancelado desde InputUser (None).
        Devuelve una tupla con los datos si todo ha ido correctamente para 
        guardar mediante método del model.        
        """       
        tipo = self.__get_type_from_user(id)
        if not tipo     : return False        
        msg = "<── (" + tipo.value + ":" + ' "' + id + '"'
        
        peso = self.__get_weight_from_user(msg)
        if not peso     : return False                   
        
        precio = self.__get_price_from_user(msg)
        if not precio   : return False
            
        cantidad = self.__get_quantity_from_user(msg)
        if not cantidad : return False   
        
        data = (tipo, peso, precio, cantidad)
        Logger.Core.info("Registrando Componente '"+id+"'...") 
        return data    
    
    # MODIFY -COMPONENTS-
    def set_modify_data_from_user(self, id):
        """
        Permite al usuario modificar un componente existente en función de su id.
        Pregunta al usuario si desea modificar cada elemento del componente,
        mostrando su id y su valor con la unidad o especificación correspondiente.
        Si el usuario dice que sí, se le permite modificarlo, si dice que no,
        pasa al siguiente elemento.
        """    
        # Componente actual (old)
        old_id = '"' + id + '"'        
        old    = self._component_dic.get(id)        
        
        is_modified = False
        
        if old is None:
            Logger.Core.warn(
                "Componente " + id + " no encontrado en el sistema.")
            return False
        
        # A partir de aqui se le pregunta al usuario si quiere modificar
        # cada elemento del componente (independientemente)
        
        # TIPO DE COMPONENTE
        Logger.Core.info("──> (" + old._tipo.value + ": " + old_id  + ")")        
        
        question = "¿Desea modificar el tipo del componente?"
        if InputUser.ask_yes_no_question(question):
            new_tipo = self.__get_type_from_user(id)
            if not new_tipo: return False            
            is_modified = True
        else: new_tipo = old._tipo
        
        t    = str(new_tipo.value)
        msg  = "<── (" + t + ": " + old_id
        info = "──> (" + t + ": " + old_id + ". "
        
        # PESO DEL COMPONENTE
        old_peso = str(old._peso)
        Logger.Core.info(info + old_peso + " gramos)")        
    
        question = "¿Desea modificar el peso del componente?"
        if InputUser.ask_yes_no_question(question):           
            new_peso = self.__get_weight_from_user(msg)
            if not new_peso: return False    
            is_modified = True            
        else: new_peso = old._peso
                
    
        # PRECIO DEL COMPONENTE
        old_precio = str(old._precio)
        Logger.Core.info(info + old_precio + " euros)")                
        
        question = "¿Desea modificar el precio del componente?"
        if InputUser.ask_yes_no_question(question):            
            new_precio = self.__get_price_from_user(msg)
            if not new_precio: return False                
            is_modified = True
        else: new_precio = old._precio
         
        
        # CANTIDAD DEL COMPONENTE
        old_stock = str(old._cantidad)
        Logger.Core.info(info + old_stock + " stock)")                
        
        question = "¿Desea modificar la cantidad del componente?"
        if InputUser.ask_yes_no_question(question):            
            new_cantidad = self.__get_quantity_from_user(msg)
            if not new_cantidad: return False     
            is_modified = True
        else: new_cantidad = old._cantidad
         
    
        # Si no se realizó ninguna modificación, informamos al usuario 
        # y devolvemos False
        if not is_modified:
            r ="No se realizaron modificaciones en el componente "+'"'+id+'"\n'
            Logger.Core.info(r)
            Logger.pause()
            return False
        
        # Aunque no se hayan modificado todos, pero por lo menos uno
        # se guardarán de nuevo los antiguos valores. 
        # (Debe seguir el diseño, igual es mejorable).
        Logger.Core.info("Registrando modificaciones de componente '"+id+"'...")   
        data = (new_tipo, new_peso, new_precio, new_cantidad)
        return data     
    
    def get_new_stock_from_user(self, id):
        """
        Pregunta al usuario por una cantidad de componentes. 
        Si devuelve 'False' es cancelación por parte del usuario.
        En caso de exito devuelve 'True'. Función propia del modelo 'Component'
        """                
        t = str(self._component_dic[id]._tipo.value) 
        
        q = "Nueva stock de componentes para " + id + " = "
        c = InputUser.get_uint(q)  
        
        if c is None: return False  
        
        self._component_dic[id].set_quantity(c)        
               
        info  = '<── (' + t + ': ' + '"' + id + '". ' + str(c) + ' stock)\n'
        Logger.Core.info(info) 
        
        return True
    
    def remove(self, id):
        """
        TODO: Empezamos a realizar cierta parte de la separación de
        responsabilidades 
        """
        Logger.Core.info('Eliminando "' + id + '"...') 
        del self._component_dic[id]  
        Logger.Core.info('"' + id + '" eliminado.\n' ) 
        
        return True
        
    def update_stock_by_component_list(self, increment, component_data = None): 
        """
        Podemos usar esta función para actualizar el stock usando la función 
        de la clase Component 'update_quantity'. Este método lo usará 
        principalmente el 'controller' de equipos que tiene enlace a este mismo
        controlador, de momento lo usa en lo siguientes casos:
            
            . Al dar de alta un equipo (se restan componentes)
            . Al modificar un equipo (componentes extraidos se devuelven)
            . Al eliminar un equipo (componentes extraidos se devuelven)
        
        En el caso de que se esté tratando de devolver un componente que se 
        haya eliminado del sistema, en lugar el método 'update_quantity()'
        se le preguntará al usuario qué quiere hacer:
            
            . Dar de alta de nuevo el componente al stock
            . Desechar ese componente
        """     
        
        for id, data in component_data.items():            
   
           id_ = '"' + id + '"'
           
           # Si el componente sigue existiendo en stock de componentes
           if id in self._component_dic:
               updated = self._component_dic[id].update_quantity(increment)
               if not updated:
                   Logger.Core.info('Stock Componente '+ id_ +' es menor a 0.')
   
           # Si el usuario eliminó anteriormente el componente del stock
           else:
               Logger.Core.info("No se encuentra componente " + id_ + ".")
               Logger.Core.warn(
                   "Componente "+ id_ +" ya no está registrado en el sistema.")               
               
               if InputUser.ask_yes_no_question(
                       "¿Quiere darlo de alta de nuevo o desecharlo?"):
   
                   tipo, peso, precio = data
                   new_comp = Component()
                   new_comp.set_from_user_data((tipo, peso, precio, increment))
                   self._component_dic[id] = new_comp
                   Logger.Core.info("Componente " + id_
                                    + " dado de alta en el stock.")   
                   
               else: Logger.Core.info("Componente " + id_ + " desechado.")
                
                
                
                
    
                
                
    
    
    
    