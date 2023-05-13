# -*- coding: utf-8 -*-
"""
Proyecto: HardVIU
Creado el miércoles 3 de mayo de 2023 a las 16:46:05
Autor: José Luis Rosa Maiques

La clase 'menu_management' se diferencia de las otras clases de menú, ya que 
no sólo gestiona un modelo con un posible controlador de otro modelo, 
sino que maneja varios elementos:
    
    -Su instancia en el controlador es Gestión de Distribuidores.
    -Adquiere el controlador de Equipos (Device).
    -Instancia en su controlador de distribuidores el controlador de despachos.
    -Se centra principalmente en Distribuidores, Despachos y Días.
"""

from core.views.drawer import MenuDrawer
from core.views.logger import Logger

from core.controllers.controller import Controller, ModelType, ModelFactory

class MenuManagament(Controller): # controller 1ª instancia 'Distributor'

    def __init__(self, menu_devices):
        
        """
        PROPIEDADES DISTRIBUIDOR
        """
        # FACTORY method: Instancia del controlador con modelo "COMPONENT"
        super().__init__(ModelType.DISTRIBUTOR)
        
        # Controlador de equipos a controlador de distribuidores (ctrl equipos)
        device_controller = menu_devices.get_controller()        
        self._controller.link_device_controller(device_controller)        

        # Menu principal. Mostramos al principio solo "Alta" ('max_options') 
        self._menu_distributor = MenuDrawer("HardVIU / 3) Distribuidores", [
            "Alta", "Modificar", "Listar Distribuidores"], max_options = 1)

        # Submenú nueva alta
        self._menu_add = MenuDrawer("HardVIU / 3) Distribuidores / 1) Alta")

        # Submenú modificación distribuidor
        self._menu_modi = MenuDrawer(
            "HardVIU / 3) Distribuidores / 2) Modificar", [
                "Cambiar información", "Dar de baja"])

        self._distribuidor_result = "dado de alta con éxito."
        
        """
        PROPIEDADES DESPACHO
        """       
        
        # Esta instancia es un poco rebuscada, pero 'DistributorController'
        # necesita de 'DispatchController' además de 'DeviceController'                
        dm = ModelType.DISPATCH
        dc = ModelFactory.create_controller(dm, self._controller._dispatch_dic)        
        self._controller.link_dispatch_controller(dc)
        
        # Menú único de despachos        
        self._menu_disp = MenuDrawer(3*' '+ "HardVIU / 4) Despachar" + ' '*3)
        
        self._depacho_result = "asignado con éxito."
        
        """
        PROPIEDADES DÍAS
        """
        # Menú único de días
        self._menu_days = MenuDrawer(3*' '+ "HardVIU / 4) Días" + ' '*3)
        
        
    """
    METODOS DISTRIBUIDOR (Distrubutors)
    """    
    def get_controller(self): return self._controller

    def add_distributor(self):  # Alta de distribuidor    
    
        self._id_config["question"] = "Nombre/ID de " + self._model._name
        self._id_config["rule"    ] = "alfanumérico, mínimo 3 caracteres" 
        
        id = True
        o  = "Nuevo Distribuidor"            
        while True:                        
            self._menu_add.display(True, False, True, obj = '"' + str(o) + '"')             
            if id == True:
                
                id = super().get_and_check_id(mode = "add", auxiliar_dic=None);
                if id is None: break
                elif id != True: o = id
                continue
            else:
                if super().new_model(id):                   
                    Logger.UI.success("Distribuidor", id, 
                                      self._distribuidor_result,
                                      pause = False, newline = False)                     
                    id = True
                    o  = "Nuevo Distribuidor"
                else: break            
                if not super().ask_this_question("Introducir otro Distribuidor"):                
                    break

    

    def modify_info(self, id):
        Logger.UI.cancel_info(n1 = '\n', level = 1)
        if super().modify_model_info(id):
            Logger.UI.success("Distribuidor", id, 
                              "ha finalizado el proceso de modificación.",
                              newline = False)

    def remove_distributor(self, id):        
        Logger.Core.action("Distribuidor a eliminar", id, pause = False)          
        question = "Seguro que desea eliminar este distribuidor del sistema"
        if self.ask_this_question(question): 
            if self._controller.remove(id):
                success = "eliminado del sistema."
                Logger.UI.success("Distribuidor", id, success, newline = False)  
                return True           
      
        
    def menu_distributor(self):
        while True:
            numero_opciones_visibles = 1
            if len(self._dic.items()) > 0: numero_opciones_visibles = 3 
            self._menu_distributor.set_max_options(numero_opciones_visibles)
            self._menu_distributor.display(zero = "Menú anterior")
            option = self._menu_distributor.get_option()

            if option == 1: # Alta distribuidor
                self.add_distributor()  
                
             # Submenú Modificación
            elif (option == 2 or option == 3) and numero_opciones_visibles > 1:
                
                p_list = False if option < 3 else True               
                
                args = [self._dic, "Distribuidor", p_list, False]
                id, user_cancel = self.select_model(*args)                 
                
                if not id: continue
                while True:                    
                    self._menu_modi.display(True, True, obj = '"' + id + '"', 
                                            zero = "Menú anterior")
                    option = self._menu_modi.get_option()
                    if option == 0:  # Salir de modificación
                        Logger.scroll_screen()
                        break
                    elif option == 1:  # Cambiar información
                        self.modify_info(id)
                        continue
                    elif option == 2:  # Dar de baja
                        if self.remove_distributor(id):
                            break
                        continue
                    else: Logger.UI.bad_option()
            elif option== 0:  # Salir del menú Distribuidores
                break
            else: Logger.UI.bad_option()
    """
    METODO GENERICO 'select_model':
        
        - Modelos escogibles: Distributor, Device y Dispatch
    """
    
    def select_model(self, model_dic, name, pre_list, info = True):   
        """
        Recordar que devuelve tupla (id, user_cancellation).
        user_cancellation es un bool para saber si es cancelación de usuario
        el None de los datos recibidos, o es por otro motivo.
        """
        self._id_config["question"] = "ID " + name + " o número de la lista"
        self._id_config["rule"    ] = "('l' para listar) = "
        if pre_list: super().list_models_from_dic(name, model_dic)
        if info: Logger.UI.cancel_info(level = 1)
        return super().select_model_from_dic(model_dic, name)      
            
    """
    METODOS DESPACHOS (Dispatchs)
    """    
    
    def select_dispatch(self, dispatch_dic):
        self._id_config["question"] = "ID Despacho o número de la lista"
        self._id_config["rule"    ] = "('l' para listar) = "
        return super().select_model_from_dic(dispatch_dic, "Equipo")  
    
    def add_dispatch(self): # Nuevo despacho        
        
        self._id_config["question"] = "Nombre/ID de " + self._model._name
        self._id_config["rule"] = "alfanumérico" 
            
        is_selected = False
        o  = "Selección de Distribuidor"               
        while True:                        
            self._menu_disp.display(True, False, True, obj ='"' + str(o) + '"')             
            
            # Aun no se ha selecciona un id (control de casos)
            if not is_selected:                 
                
                # Entradas de usuario (siempre en InputUser)
                args = [self._dic, "Distribuidor", False, False]
                # Desempaquetamos con operador * (idea de hacerlo en todo)
                id_distributor, user_cancel = self.select_model(*args)               
                
                # Registro 'Distribuidores' vacio
                if id_distributor is None and not user_cancel:
                    Logger.UI.emph("Necesita dar de alta algún distribuidor.")
                    Logger.pause() # A la espera de que el usuario lea mensaje
                    break 
                # El usuario ha cancelado  
                if user_cancel: break               
                 
                is_selected = True
                o = id_distributor
                Logger.UI.cancel_info(level = 1)
                continue
                
            
            # is_selected = True -> Tenemos distribuidor
            else:
                # Accedemos al 'controller' de Device
                device_ctrl = self._controller.get_device_controller()                
                
                # Nueva configuración para la petición del ID
                self._id_config["question"]= "Nombre/ID del Equipo a despachar"
                self._id_config["rule"]    = "alfanumérico"                 
                
                # Accedemos al diccionario de Device
                device_dic = device_ctrl.get_dic()
                
                # Entradas de usuario (InputUser)
                # Función generica para escoger un modelo (se pasa dic)               
                args = [device_dic,"Equipo", False, False]
                id_device,user_cancel = self.select_model(*args)
                
                # Registro 'Equipo' vacio
                if id_device is None and not user_cancel:
                    Logger.UI.emph("Ensamble algún equipo para asignarlo a " 
                                   + 'distribuidor "' + id_distributor + '".')
                    Logger.pause() # A la espera de que el usuario lea mensaje
                    break 
                # El usuario ha cancelado  
                if user_cancel: break    
            
                # print("En teoria aquí tenemos Distributor y Device.")
                # print("A partir de aqui usamos 'controller' Dispatch")                                
                # Accedemos al 'controller' de Dispatch
                dispatch_ctrl = self._controller.get_dispatch_controller()
                
                # Creando el modelo en la 'view' para enviarselo al 
                # 'controller' al que pertenece
                dispatch = ModelFactory.create_model(ModelType.DISPATCH)
                
                result = dispatch_ctrl.new_dispatch(dispatch, id_distributor,
                                                    id_device)               
                if result > 0:                   
                    Logger.UI.success("Despacho", '#'+str(result), 
                                      self._depacho_result,
                                      pause = False, newline = False)       
                    
                dic = dispatch_ctrl.get_dic()
                super().list_models_from_dic("Despachos", dic)          
                
                Logger.pause()
                break  
    
    def menu_dispatch(self): self.add_dispatch()
    
    """
    METODOS DÍAS (Days)
    """    
    
    
    def add_days(self): # Dias
    
        # Accedemos al 'controller' de Dispatch
        dispatch_ctrl = self._controller.get_dispatch_controller()
        
        # Accedemos al diccionario de Despachos 
        dispatch_dic = dispatch_ctrl.get_dic()
        
        # Nombre del tipo de modelo (nos salimos del diseño FACTORY method)
        model = "Despacho"    
        
        # ID Config
        self._id_config["question"] = "ID de " + model
        self._id_config["rule"    ] = "númerico" 
            
        is_selected = False
        o  = "Selección de " + model
        
        
        while True:                        
            self._menu_days.display(True, False, True, obj= '"' + str(o) + '"')
            
            # Aun no se ha selecciona un id (control de casos)
            if not is_selected:
                
                # Entradas de usuario (siempre en InputUser)
                args = [dispatch_dic, "Despachos", False, False]
                id_dispatch, user_cancel = self.select_model(*args)
                
                
                Logger.pause()
                
                
                
            
            
            
            
        
        
        
        
        
        
    
    
        
    def menu_days(self):
        Logger.UI.emph("Menu Días")
        Logger.pause()
        
    """  Función a llamar desde 'System' """
    def update(self, op):        
        if   op == 3: self.menu_distributor()
        elif op == 4: self.menu_dispatch()
        elif op == 5: self.menu_days()
        
