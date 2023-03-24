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

from enum import Enum

class TipoComponente(Enum):
    FUENTE = "Fuente"
    PB = "PB"
    TG = "TG"
    CPU = "CPU"
    RAM = "RAM"
    DISCO = "Disco"

class Componente:
    def __init__(self, id, nombre, tipo, peso, precio, cantidad):
        self.id = id
        self.nombre = nombre
        self.tipo = TipoComponente(tipo)
        self.peso = peso
        self.precio = precio
        self.cantidad = cantidad
        
        
    def to_string(self):
        return f'{self.id};{self.nombre};{self.tipo.value};{self.peso};{self.precio};{self.cantidad}'
    
    
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
    
    
    
    
    