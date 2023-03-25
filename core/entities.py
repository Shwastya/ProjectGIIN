# -*- coding: utf-8 -*-
"""
Proyecto: HardVIU
Created on Tue Mar 24 19:28:54 2023
@author: José Luis Rosa Maiques

Entidades:
    La clases de este modulo representan la estructura de datos del sistema como entidades.
    La función to_string se usará para facilitar el guardado de ficheros con el separador ';'
"""


S = ';' # Definimos como constante el valor que queremos usar como separador.


# Entidad Componente ----------------------------------------------------------

from utils.logger import Logger
from core.constants import USER_CANCEL_MSG

from enum import Enum

class TipoComponente(Enum):
    
    FUENTE = "Fuente"
    PB     = "PB"
    TG     = "TG"
    CPU    = "CPU"
    RAM    = "RAM"
    DISCO  = "Disco"
    
    # metodo de clase para mostrar el listado
    @classmethod
    def display(cls):
        print("Tipos de componentes:")
        index = 1
        for tipo_componente in cls:
            print("\t" + str(index) + ". " + tipo_componente.value)            
            index += 1
            

class Componente:
    def __init__(self, id = None, tipo = None, peso = None, precio = None, cantidad = None):
        self.id = id        
        self.tipo = TipoComponente(tipo) if tipo else None
        self.peso = peso
        self.precio = precio
        self.cantidad = cantidad
        
    def set_values(self, id, tipo, peso, precio, cantidad):
        self.id = id        
        self.tipo = TipoComponente(tipo)
        self.peso = peso
        self.precio = precio
        self.cantidad = cantidad       
        
    def user_set_values(self, id):
        Logger.info("[saved]> ID de componente: " + id)                
        # Solicitamos el tipo de componente hasta que sea válido
        while True:
            TipoComponente.display()      
            cad = input("Seleccione número del tipo de componente = ")
            if cad == USER_CANCEL_MSG: return False
            elif cad.isdigit():
                index = int(cad) - 1          
                if index < 0 or index >= len(TipoComponente):
                    Logger.warn("El Tipo de componente no está en la lista. Inténtalo de nuevo.")
                    continue
            
                tipo = TipoComponente(list(TipoComponente)[index].value)
                Logger.info("[saved]> Tipo de componente: " + tipo.value)
                break
            else: 
                Logger.warn("Por favor, introduce un número entero válido.")
                continue
        
        peso = input("Peso en gramos del componente = ")
        if peso == USER_CANCEL_MSG: return False         
        peso = int(peso)

        precio = input("Precio en euros del componente = ")
        if precio == USER_CANCEL_MSG: return False         
        precio = float(precio)

        cantidad = input("Cantidad de componentes = ")
        if cantidad == USER_CANCEL_MSG: return False
        cantidad = int(cantidad)

        self.set_values(id, tipo.value, peso, precio, cantidad)
        return True
        
    def to_string(self):
        return f'{self.id};{self.nombre};{self.tipo.value};{self.peso};{self.precio};{self.cantidad}'
    
    
    
    #   return str(self.id) + S + self.nombre + S + self.marca + S + str(self.precio) + S + str(self.cantidad)
    
    
#class Componente:
#    def __init__(self, id, nombre, descripcion, precio, cantidad):
#        self.id = id
#        self.nombre = nombre
#        self.descripcion = descripcion
#        self.precio = precio
#        self.cantidad = cantidad

#    def to_string(self):
#        return str(self.id) + S + self.nombre + S + self.marca + S + str(self.precio) + S + str(self.cantidad)
    
    
    

# Entidad Equipo --------------------------------------------------------------
class Equipo:
    def __init__(self, id, nombre, descripcion, precio, componentes = []):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        
        # Equipo tiene como atributo una lista de componentes de la clase Componente
        self.componentes = componentes

    def to_string(self):        
        return f"ID: {self.id}, Nombre: {self.nombre}, Descripción: {self.descripcion}, Precio: {self.precio}, Componentes: {len(self.componentes)}"

    def agregar_componente(self, componente):
        self.componentes.append(componente)

    def eliminar_componente(self, componente_id):
        self.componentes = [componente for componente in self.componentes if componente.id != componente_id]
        
        
        
        
# Entidad Distribuidor --------------------------------------------------------
class Distribuidor:
    def __init__(self, id, nombre, direccion, telefono, correo_electronico):
        self.id = id
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.correo_electronico = correo_electronico

    def __str__(self):
        return f"ID: {self.id}, Nombre: {self.nombre}, Dirección: {self.direccion}, Teléfono: {self.telefono}, Correo electrónico: {self.correo_electronico}"
    
    


# Entitdad Despacho -----------------------------------------------------------
#import datetime
class Despacho:
    def __init__(self, id, equipo, distribuidor, fecha_despacho, cantidad):
        self.id = id
        self.equipo = equipo
        self.distribuidor = distribuidor
        self.fecha_despacho = fecha_despacho
        self.cantidad = cantidad

    def __str__(self):
        return f"ID: {self.id}, Equipo: {self.equipo}, Distribuidor: {self.distribuidor}, Fecha de despacho: {self.fecha_despacho}, Cantidad: {self.cantidad}"




# Entidad Dia -----------------------------------------------------------------
class Dia:
    def __init__(self, fecha, componentes, equipos, distribuidores, despachos):
        self.fecha = fecha
        self.componentes = componentes
        self.equipos = equipos
        self.distribuidores = distribuidores
        self.despachos = despachos

    def __str__(self):
        return f"Fecha: {self.fecha}, Componentes: {len(self.componentes)}, Equipos: {len(self.equipos)}, Distribuidores: {len(self.distribuidores)}, Despachos: {len(self.despachos)}"
    
    
    
    
    