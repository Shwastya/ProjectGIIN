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
from core.models.dispatch        import DispatchStatus
from core.models.device          import DeviceStatus

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
                "Cambiar Información", "Eliminar"])

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
        
        self._despacho_result = "asignado con éxito."
        
        """
        PROPIEDADES DÍAS
        """
        # Menú único de días
        self._menu_days = MenuDrawer(5*' '+ "HardVIU / 5) Días" + ' '*5)
        
        self._dias_result = "(PENDIENTE)."
        
        """
        PROPIEDADES INFO SISTEMA
        """
        self._menu_infosys = MenuDrawer("HardVIU / 6) Info sistema", [
            "Componentes", "Equipos", "Distribuidores", 
            "Histórico de Despachos", "Sistema Completo"])
        
        sub_menu_equipos_tit = "HardVIU / 6) Info sistema / 2) Equipos"
        self._sub_menu_equipos = MenuDrawer(sub_menu_equipos_tit, [
            "Equipos en Sistema", "Equipos Despachados"])
        
        self._sub_menu_historico = MenuDrawer(
            "HardVIU / 6) Info sistema / 4) Histórico de Despachos", [
                "Pendientes", "En tránsito", "Entregados", 
                "Devueltos", "Histórico Completo"])
        
        
    """
    METODOS DISTRIBUIDOR (Distributors)
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
        Logger.UI.cancel_info(level = 1)
        if super().modify_model_info(id):
            Logger.UI.success("Distribuidor", id, 
                              "modificado con éxito.",
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
                id, user_cancel = super().select_model(*args)                 
                
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
                id_distributor, user_cancel = super().select_model(*args)               
                
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
                
                # Que dispositivos se pueden escoger para Despacho
                # [NEW_DEVICE] y [RETURNED]
                filtro = [DeviceStatus.NEW_DEVICE, DeviceStatus.RETURNED]
                
                # filtramos modelos con la función 'controller' base                
                dic = super().filter_models(device_dic, filtro)               
                
                # Entradas de usuario (InputUser)
                # Función generica para escoger un modelo (se pasa dic)               
                args = [dic, "Equipo", False, False, "Nuevos, Devueltos"]
                id_device,user_cancel = super().select_model(*args)
                
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
                    id = 'D' + str(result) + '_' + id_device
                    Logger.UI.success("Despacho", id, self._despacho_result,
                                      pause = True, newline = False)       
                
                # # TODO: RECORDAR BORRAR ESTO
                # dic = dispatch_ctrl.get_dic()
                # super().list_models_from_dic("Despachos", dic)               
                # Logger.pause()
                # # 
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
                
                # Solo podemos modificar despachos pendientes o en transito
                filtro   = [DispatchStatus.PENDING, DispatchStatus.IN_TRANSIT]
                
                # filtramos modelos con la función 'controller' base                
                dic = super().filter_models(dispatch_dic, filtro)               
                
                args = [dic,"Despachos", False,False, "Pendiente; En transito"]
                
                id_dispatch, user_cancel = super().select_model(*args)                
                
                # Registro 'Equipo' vacio
                if id_dispatch is None and not user_cancel:
                    Logger.UI.emph("Asigne algún despacho en el menú Despachar.")
                    Logger.pause() # A la espera de que el usuario lea mensaje
                    break 
                # El usuario ha cancelado  
                if user_cancel: break    
            
            
                is_selected = True
                o = id_dispatch
                Logger.UI.cancel_info(level = 1)
                continue
            
            else:             
                
                result, days = dispatch_ctrl.advance_days(id_dispatch)
                
                if not result: break # Cancelación (esto lo veo arriesgado)
                elif result is None: continue # Fallo en la entrada (continue)
                else:                         # Dias restantes
                
                    dias = "(" + str(days) + ")"
                    if days > 0:           
                        msg = "Días estimados para la entrega:"
                        self._dias_result = "(EN TRANSITO)."
                    else:
                        msg = "Equipo llegó a destino. Días restantes:"
                        self._dias_result = "(ENTREGADO)."
                    
                Logger.UI.success(msg, dias, self._dias_result, pause = True, 
                                  newline = False)
                break
            
    def menu_days(self):
        self.add_days()
        
    
    """
    METODOS INFO SYSTEM
    """   
    
    def info_devices_in_system(self):
         device_dic = self._controller.get_device_controller().get_dic()
         if not super().list_models_from_dic("Equipo", device_dic):
             Logger.UI.emph("No hay equipos disponibles, consulte en despachados.")        
         Logger.print_line(50, color = True)
         
    
    def info_devices_delivered(self):
        device_ctrl = self._controller.get_device_controller()
        device_dic  = device_ctrl.get_delivered_devices_dic()         
        if not super().list_models_from_dic("Equipo", device_dic, "Entregados"):
            Logger.UI.emph("No hay hay histórico de equipos entregados.")
        Logger.print_line(50, color = True)  
        
        
        
    def sub_menu_equipos(self):
        
        while True:                         
            self._sub_menu_equipos.display(zero = "Menú anterior")           
            op = self._sub_menu_equipos.get_option()     
            
            if   op == 1: 
                self.info_devices_in_system()                
                Logger.pause() 
            elif op == 2: 
                self.info_devices_delivered()                           
                Logger.pause() 
                
            elif op == 0: break # Salir de menu Componentes
            else: Logger.UI.bad_option()
            
    def info_component(self):        
        component_dic = self._controller.get_device_controller().get_component_dic()
        if not super().list_models_from_dic("Componente", component_dic):            
            Logger.UI.emph("No hay componentes dados de alta en el sistema.")
        Logger.print_line(50, color = True)
          
        
    def info_distributors(self):
        distribut_dic = self._controller._distributor_dic
        if not super().list_models_from_dic("Distribuidor", distribut_dic):
            Logger.UI.emph("No hay distribuidores dados de alta en el sistema.")
        Logger.print_line(50, color = True)
        
    def info_dispatch(self, filtro = None, txt = None):
        dispatch_dic = self._controller.get_dispatch_controller().get_dic()
        dic = dispatch_dic
        
        if filtro is not None:
            dic = super().filter_models(dispatch_dic, filtro)
        
        t = ' ' + txt + ' ' if txt is not None else ' '
        
        if not super().list_models_from_dic("Despacho", dic, txt):
            Logger.UI.emph("No hay despachos" + t + "en el sistema.")
        Logger.print_line(50, color = True)       
    
    def sub_menu_dispatch(self):
        
        while True:                         
            self._sub_menu_historico.display(zero = "Menú anterior")           
            op = self._sub_menu_historico.get_option()     
            
            if   op == 1:
                args = [[DispatchStatus.PENDING], "Pendientes"]                
                self.info_dispatch(*args)
                Logger.pause() 
                
            elif op == 2:
                args = [[DispatchStatus.IN_TRANSIT], "En transito"]                
                self.info_dispatch(*args)
                Logger.pause() 
                
            elif op == 3:
                args = [[DispatchStatus.DELIVERED], "Entregados"]                
                self.info_dispatch(*args)
                Logger.pause() 
                
            elif op == 4:
                args = [[DispatchStatus.RETURNED], "Devueltos"]                
                self.info_dispatch(*args)
                Logger.pause() 
                
            elif op == 5:
                self.info_dispatch()
                Logger.pause() 
                
            elif op == 0: break # Salir de menu Componentes
            else: Logger.UI.bad_option()        
        
    def info_system(self):   
        
        while True:                         
                       
            self._menu_infosys.display(zero = "Menú anterior")           
            op = self._menu_infosys.get_option()     
            
            if   op == 1: 
                self.info_component()
                Logger.pause() 
            elif op == 2: 
                self.sub_menu_equipos()
            elif op == 3: 
                self.info_distributors()
                Logger.pause()
            elif op == 4:
                self.sub_menu_dispatch()
            elif op == 5:
                self.info_component()
                self.info_devices_in_system()
                self.info_devices_delivered()  
                self.info_distributors()
                self.info_dispatch()
                Logger.pause()               
                
            elif op == 0: break # Salir de menu Componentes
            else: Logger.UI.bad_option()           
        
        
    """  Función a llamar desde 'System' """
    def update(self, op):        
        if   op == 3: self.menu_distributor()
        elif op == 4: self.menu_dispatch()
        elif op == 5: self.menu_days()
        elif op == 6: self.info_system()
        



