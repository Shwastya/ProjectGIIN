# -*- coding: utf-8 -*-
"""
Project: HardVIU
Created on Sat Mar 25 10:16:27 2023
@author: José Luis Rosa Maiques

Clase 'InputUser', métodos input personalizados y lógica de usuario.

En esta clase de métodos estáticos, separamos las interacciones del usuario
de la lógica principal del programa. En lugar de solicitar y validar la
entrada del usuario dentro de las clases del programa, utilizamos funciones
separadas que manejan la entrada y validación del usuario, y luego pasamos
los valores ingresados a las clases correspondientes.

Se definen métodos genéricos como pedir un input int, float, o que elija de un 
Enum, y luego métodos específicos para las clases Entity que vamos definiendo.
"""

#from core.kconfig import K_ALLOWED_CHARS, K_USER_CANCEL
#from core.entity.component import ComponentType
from core.kconfig import K_USER_CANCEL
from utils.logger import Logger

class InputUser:   

    # Pide un número entero
    def get_int(msg):
        while True:
            i = input(msg)
            if i.lower() == K_USER_CANCEL.lower():
                return None
            elif i.isdigit() and int(i) > 0:
                return int(i)
            else: Logger.warn("El número debe ser entero y mayor que 0.")

    # Pide un número real
    def get_float(msg):
        while True:
            r = input(msg)
            if r.lower() == K_USER_CANCEL.lower():
                return None
            elif r.replace('.', '', 1).isdigit() and float(r) > 0:
                return float(r)
            else:
                Logger.warn("Introduce un número real mayor que 0.")
                
                
    # Pide un alfanúmerico, verificará si el ID existe o no en función del 
    # valor del parámetro check_non_existence. Si es True, buscará un ID que 
    # no exista en el diccionario; si es False, buscará uno que exista.   
    # Para que se use esta funcionalidad hay que pasarle un Dic    
    def get_alphanum(question, regla, l, obj, dic=None, check_non_exist=False):
        
        warn = obj + " debe tener al menos (" + str(l) + ") caracteres."
        
        if check_non_exist: 
            l = 1
            warn = "Entrada vacía. Intenta de nuevo."
        
        while True:
            id = input(question + " (" + regla + ") = ")
            if id.lower() == K_USER_CANCEL.lower():
                Logger.register_quit("Cancelado por usuario")
                return None
            
            id_stripped = id.strip()  # Elimina espacios en blanco al inicio y al final del string
            if len(id_stripped) < l:                
                Logger.warn(warn)
                continue
    
            if dic is not None:
                if check_non_exist and id not in dic:
                    if id == 'l' or id == 'L': return id
                    Logger.warn(obj + " no se encuentra. Elija otro.")                    
                    continue
                elif not check_non_exist and id in dic:
                    Logger.warn(obj + " ya existe. Elija otro.")
                    continue
    
            return id

        
    # Permite escoger al usuario de un enumerado pasado como parametro
    def get_from_enum(enum_class, msg1, msg2):
        """
        Se puede llamar a get_from_enum pasando el enumerado y dos cadenas 
        que describa el tipo de elemento que se selecciona. Por ejemplo, para 
        seleccionar un tipo de componente, llamarías a la función de la 
        siguiente manera:

            tipo = self.get_enum_input(ComponentType, "msg1", "msg2")        
        """
        while True:
            cad = input(msg1)
            if cad.lower() == K_USER_CANCEL.lower():
                return None
            elif cad.isdigit():
                index = int(cad) - 1
                if index < 0 or index >= len(enum_class):
                    Logger.warn(msg2)
                else:
                    return enum_class(list(enum_class)[index].value)
            else:
                Logger.warn("Introduce un número válido de la lista.")
    
    
    
    """ Métodos específicos para las clases de tipo Entity: """
    
    # ---> Alta de Componente
    # Este método es específico y se utiliza en la clase entidad 'Component' 
    # en el método 'set_values'. Devuelve una tupla con lo valores o None.    
    def get_new_component(id, ComponentType, mode = None):      
       
        if mode == "add" or mode == "modify":
            ComponentType.display()
            msg1 = "Elija un número de la lista para el tipo de componente = "
            msg2 = "El Tipo de componente no está en la lista."
            tipo = InputUser.get_from_enum(ComponentType, msg1, msg2)
            if tipo is None: return None
            Logger.info(tipo.value +' "'+ id +'".')
        
            peso = InputUser.get_int("Peso en gramos del componente = ")        
            if peso is None: return None
            Logger.info(tipo.value +' "'+ id +'". '+ str(peso)+ ' gramos.')
        
            precio = InputUser.get_float("Precio en euros del componente = ")
            if precio is None: return None
            Logger.info(tipo.value +' "'+ id +'". '+ str(precio) +' euros.')
        
            cantidad = InputUser.get_int("Cantidad de componentes = ")
            if cantidad is None: return None
            Logger.info(tipo.value+' "'+ id +'". '+str(cantidad)+' de stock.')            
            
            # Creamos una tupla
            component_data = tipo.value, peso, precio, cantidad
            return component_data
        
        elif mode == "stock":
            
            # En caso de que solo se deseer modificar el 'Stock'
            cantidad = InputUser.get_int("Nueva cantidad de componentes = ")
            if cantidad is None: return None
            Logger.info('El nuevo stock de "' + id +'" modificado a '
                        + str(cantidad) +'.')
            #Logger.info(tipo.value+' "'+ id +'". '+str(cantidad)+' de stock.')   
            return cantidad
          
    # -- Alta de Equipos
    # Este método es específico y se utiliza en la clase entidad 'Device'
    def get_new_device(id, p, component_types_enum):
        """
        Permite al usuario ingresar información para configurar o modificar el dispositivo.
        ManagerComponent tiene el acceso al Dic. de componentes.
        component_types_enum (Enum) enumerado con los tipos de componentes.
        Devuelve una tupla con el id y una lista de los componentes selecci..
        """
    
        # Accedemos al diccionario de componentes directamente del manager
        comp_dic = p["manager"]._entities_dic
        mode = p["mode"]
    
        if len(comp_dic) == 0:
            Logger.error("¡Stock de componentes vacío!")            
            return False
    
        device_components = {}
        disassembled_components = []  # Lista temporal para almacenar componentes desmontados
        for component_type in component_types_enum:
    
            if mode == "modify" and component_type in p["device"]._components:
                old_comp_id = p["device"]._components[component_type]["id"]
                disassembled_components.append(old_comp_id)  
                Logger.info_m("Sustituir", component_type.value,
                              "'"+old_comp_id+"'", "por:")
    
            disp_components = []
            for comp_id, comp in comp_dic.items():
                if comp._tipo == component_type and comp._cantidad > 0:
                    disp_components.append((comp_id, comp))
    
            if not disp_components:
                Logger.error("No hay componentes disponibles de tipo "
                             + component_type.value + ".")
                return False
    
            for index, (comp_id, component) in enumerate(disp_components,
                                                         start=1):
                Logger.success("\t" + str(index) + ". " 
                               + component.display(comp_id))
    
            while True:
                selected_comp_index = InputUser.get_int(
                    "Seleccione " + component_type.value + " (número) o '"
                    + K_USER_CANCEL + "' para cancelar: ")
    
                if selected_comp_index is None:
                    return None
    
                if 1 <= selected_comp_index <= len(disp_components):
                    break
                else:
                    Logger.warn("Introduce un número válido o '"
                                + K_USER_CANCEL + "' para cancelar.")
    
            selected_comp_id, selected_comp = disp_components[
                selected_comp_index - 1]
    
            # Crear un diccionario solo con la información necesaria
            compact_component = {
                "id": selected_comp_id,
                "peso": selected_comp._peso,
                "precio": selected_comp._precio
            }
    
            # Guardar el diccionario compacto en device_components
            device_components[component_type] = compact_component
    
            Logger.info("Ensamblando en " + id + ": "
                        + selected_comp._tipo.value
                        + " " + selected_comp_id)

    
        # Agregamos los componentes desmontados al stock solo después de 
        # seleccionar todos los componentes nuevos
        if mode == "modify":
            Logger.info_m("Devolviendo componentes desmontados al stock.")
            p["manager"].update_stock_by_component_list(disassembled_components, 1)            
        
        # Actualizamos el stock una vez que se hayan seleccionado todos 
        # los componentes correctamente
        for component_type, compact_component in device_components.items():
            p["manager"].update_stock_by_component_list([compact_component["id"]], -1)            
    
        return device_components


    



    
    
  
    
    
        