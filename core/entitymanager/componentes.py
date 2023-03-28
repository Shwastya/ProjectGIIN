# -*- coding: utf-8 -*-
"""
Proyecto: HardVIU
Created on Fri Mar 24 16:18:11 2023
@author: José Luis Rosa Maiques
"""

from core.kconfig import K_USER_CANCEL
from utils.drawer import MenuDrawer
from utils.logger import Logger
from utils.icheck import alnumcheck

from core.entity.componente import Componente

class ManagerComponentes:
    
    def __init__(self):
        self._componentes = []
        
        # Menu principal
        self._menu_comp = MenuDrawer("HardVIU / 1) Componentes",[
            "Alta", "Modificación"])
        
        # Submenu nueva alta
        self._menu_alta = MenuDrawer("HardVIU / 1) Componentes / 1) Alta")
        
        # Submenu modificación componente
        self._menu_modi = MenuDrawer("HardVIU / 1) Componentes / 2) Modificación",[
            "Cambiar stock", "Cambiar información", "Dar de baja"])
        
        # Submenu cambiar información
        self._menu_info = MenuDrawer("HardVIU / 1) Componentes / 2) Modificación / 2) Cambiar información")        
        
        
    def entidad_por_id(self, id):
        for entity in self._componentes:
            if entity._id == id: return entity
        return None
    

    def listar_entidades(self):
        if not self._componentes: return False
        else:
            for entity in self._componentes:
                Logger.draw_list("\t-", entity.display())
            return True
        

    def register_quit(self, msg):        
        Logger.cancel_input_by_user(msg)       
        self._menu_comp.scroll_screen()         
        
        
    def seleccionar_componente(self, entity = "componente", menu = "Modificación"):
        if self._componentes:            
            Logger.cancel_info()               
            while True:
                id = input("Nombre/ID para acceder a " + menu +" o 'L' para listar " + entity + "s = ")
                if id.lower() == K_USER_CANCEL.lower():
                    self.register_quit("Cancelado por usuario")
                    return None
                elif id.lower() == 'l': self.listar_entidades()
                else:
                    componente = self.componente_por_id(id)
                    if componente:
                        self._menu_comp.scroll_screen()
                        return componente
                    else:
                        Logger.warn("No se encontró " + entity + " con ese identificador. Intentelo de nuevo.")
                        continue
        else: 
            self.register_quit("No existen "+ entity +"s")           
            return None 
        
        
    def obtener_id(self, entity = "componente", regla = "(alfanumérico, mínimo 3 caracteres)"):
        while True:
            id = input("Nombre/ID " + entity + " " + regla +  " = ")
            if id.lower() == K_USER_CANCEL.lower():
                self.register_quit("Cancelado por usuario")
                return None
            if not alnumcheck(id, 3): continue
            if self.entidad_por_id(id):
                Logger.warn("Ese identificador ya existe. Por favor, elija otro.")
                continue
            return id
        
    
    def alta_componente(self, again = True):                
        self._menu_alta.display(True, show_options = False, show_info = True, obj = "Nuevo Componente")
        
        id = self.obtener_id()
        if id is None:
            return
        
        self._menu_alta.display(True, show_options = False, show_info = True,obj = str(id))        
        
        componente = Componente()
        if not componente.user_set_values(id):
            self.register_quit("Cancelado por usuario")
            return
        
        Logger.succes("Componente: ", componente.display(), " dado de alta con éxito.")
        self._componentes.append(componente)
        
        if again: # pesando por si se pasa a metodos generales para entidades
            if Logger.there_is_the_question("\n¿Introducir otro componente?"): 
                self.alta_componente()    
            
    def cambiar_stock(self, componente):
        Logger.cancel_info()
        if not componente.user_set_values(componente._id, "Nueva cantidad"): 
            self.register_quit("Cancelado por usuario")
        else:
            Logger.succes("Componente: ", componente.display(), " stock actualizado.")
            Logger.succes_pause(newline = True)          
            
            
    def cambiar_informacion(self, componente):
        self._menu_info.display(True, show_options = False, show_info = True, obj = componente._id )
        if not componente.user_set_values(componente._id):
            self.register_quit("Cancelado por usuario")
        else: 
            Logger.succes("Componente: ", componente.display(), " modificado con éxito.")
            Logger.succes_pause(newline = True)             
            
    def dar_de_baja(self, componente):        
        Logger.succes("Componente a dar de baja: ", componente._id)
        if Logger.there_is_the_question("¿Está seguro de que desea dar de baja este componente?"):
            self._componentes.remove(componente)
            Logger.succes("Componente: ", componente._id, " eliminado del sistema.")
            Logger.succes_pause(newline = True)
            return True
        else:
            self.register_quit("Cancelado por usuario")
            return False            
            
    def update(self):
        self._menu_comp.scroll_screen()
        while True:
            self._menu_comp.display(False, True, "Salir")
            opcion = self._menu_comp.get_option()
            # Alta componente
            if opcion == 1: self.alta_componente()                
            # Acceder a Menu Modificación
            elif opcion == 2:              
                componente = self.seleccionar_componente()
                if componente is None: continue
                while True:
                    self._menu_modi.display(True, show_options = True, zero = "Salir", obj = componente._id)
                    opcion = self._menu_modi.get_option()
                    # Salir de Menu modificación
                    if opcion == 0:   
                        self._menu_comp.scroll_screen()
                        break
                    # Cambiar stock
                    elif opcion == 1: 
                        self.cambiar_stock(componente)
                        continue
                    # Cambiar información
                    elif opcion == 2: 
                        self.cambiar_informacion(componente)         
                        continue
                    # Dar de baja
                    elif opcion == 3: 
                        if self.dar_de_baja(componente): break
                        continue
                    # Opción no encontrada
                    else: Logger.bad_option() 
            # Salir de menu Componentes
            elif opcion == 0: break
            # Opción no encontrada
            else: Logger.bad_option() 
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                