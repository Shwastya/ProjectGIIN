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

from core.kconfig import K_ALLOWED_CHARS, K_USER_CANCEL
#from core.entity.component import ComponentType
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
    
    def get_alphanum(question =" Nombre/ID entidad", # textos de ejemplo
                         regla="alfanumérico, mínimo 3 caracteres", l = 3,
                         obj = "Identificador", dic = None,
                         check_non_exist=False):

        
        warn = obj + " debe tener al menos (" + str(l) + ") caracteres."
        if check_non_exist: 
            l = 1
            warn = "Entrada vacia. Intenta de nuevo."
        
        while True:
            id = input(question + " (" + regla + ") = ")
            if id.lower() == K_USER_CANCEL.lower():
                Logger.register_quit("Cancelado por usuario")
                return None            
            
            if len(id) < l:                
                Logger.warn(warn)
                continue
    
            chars_are_valid = True
            # <-
            for char in id:
                if not (char.isalnum() or char in K_ALLOWED_CHARS):
                    Logger.warn(
                        "Solo se permiten caracteres alfanuméricos o los " +
                        "caracteres específicos (" + K_ALLOWED_CHARS + ").")
                    chars_are_valid = False
                    break
            # ->
            if not chars_are_valid: continue
    
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
    def get_enum(enum_class, msg1, msg2):
        """
        Se puede llamar a get_enum_input pasando el enumerado y dos cadenas 
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
    # NOTA:
    # Este método es específico y se utiliza en la clase entidad 'Component' 
    # en el método 'set_values'.
    
    def get_component_input(id, components_dic):
        
        id = InputUser.get_alphanum("Identificador del componente", "alfanumérico, mínimo 3 caracteres", 3, "Identificador", components_dic)
        if id is None: return False

        ComponentType.display()
        
        ti = InputUser.get_enum(ComponentType, 
                                "Elija un número de la lista para el tipo " +
                                "de componente = ", 
                                "El Tipo de componente no está en la lista.")
        if ti is None: return False
    
        pe = InputUser.get_int("Peso en gramos del componente = ")
        if pe is None: return False
    
        pr = InputUser.get_float("Precio en euros del componente = ")
        if pr is None: return False
    
        ca = InputUser.get_int("Cantidad de componentes = ")
        if ca is None: return False
    
        return id, ti.value, pe, pr, ca
    
    
    
    def get_component_input(id, stock): # stock = "Cantidad"
        
        stock_msg = "Nueva cantidad"
        
        if stock == "Cantidad":
            # Si no se trata de "Nueva cantidad", la función se llama para
            # registrar un nuevo componente. Primero, se muestra el listado
            # de componentes existentes,
            
            stock_msg = "Cantidad"            
            
            ComponentType.display()

            ti = InputUser.get_enum(ComponentType,
                "Elija un número de la lista para el tipo de componente = ",
                "El Tipo de componente no está en la lista.")
            if ti is None:
                return False
            Logger.info(ti.value + ' "' + id + '".')

            pe = InputUser.get_int("Peso en gramos del componente = ")
            if pe is None:
                return False
            Logger.info(ti.value + ' "' + id + '". ' + str(pe) + ' gramos.')

            pr = InputUser.get_float("Precio en euros del componente = ")
            if pr is None:
                return False
            Logger.info(ti.value + ' "' + id + '". ' + str(pr) + ' euros.')

            self.set_values(ti.value, pe, pr)

        ca = InputUser.get_int(stock_msg + " de componentes = ")
        if ca is None:
            return False
        Logger.info(self._tipo.value + ' "' + id +
                    '". ' + str(ca) + ' de stock.')
        self._cantidad = ca

        return True
        