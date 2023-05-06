# -*- coding: utf-8 -*-
"""
Proyecto: HardVIU
Created on Tue Mar 21 09:53:06 2023
@author: José Luis Rosa Maiques
"""

from config.settings   import K_USER_CANCEL
from core.views.logger import Logger
class MenuDrawer:
    def __init__(self, titulo, opciones = [""], max_options = None):
        
        self.opciones   = opciones
        self.titulo     = titulo
        self._first_init = False
        
        """
        Se quiere controlar el número de opciones a mostrar, evitando que
        aparezcan opciones que no son aplicables en ciertos momentos, 
        por ejemplo: si no se ha realizado ninguna alta previamente, 
        no aparecerá el menú correspondiente a la modificación     
        """
        self.max_options = max_options
        
    def set_first_init(self, value):
        self._first_init = value
        
    def set_max_options(self, num_options):
        self.max_options = num_options
        
    def draw_up(self, width):        
        print("┌" + "─" * width + "┐")  
        
    def draw_empty(self, width):
        print("│" + " " * width + "│")    

    def draw_title(self, width, obj = "", color = 1):
        """
        Los colores 2 y 3 son para los subtitulos, uno es verde y el otro es 
        un azul algo distinto al del titulo principal.
        """
        
        title_length = len(self.titulo)        
        padding = (width - title_length) // 2
        
        if color == 1:
            print("│\033[1;36m" + " " * padding + self.titulo + " " 
                  * (width - title_length - padding) + "\033[0m│")      
        elif color == 2:                
            title_length = len(str(obj))
            padding = (width -  title_length) // 2
            print("│\033[0;37m" + " " * padding + str(obj) + " " 
                  * (width -  title_length - padding) + "\033[0;m│")
        elif color == 3:                
            title_length = len(str(obj))
            padding = (width -  title_length) // 2
            print("│\033[1;34m" + " " * padding + str(obj) + " " 
                  * (width -  title_length - padding) + "\033[0;m│")            

        print("│" + " " * width + "│")        

    def draw_option(self, option_number, option_text, width):
        print("│ " + str(option_number) + ") " + option_text + " " 
              * (width - len(option_text) - 4) + "│")

    def draw_down(self, width):
        print("└" + "─" * width + "┘")
        
    def display(self, extra = False, show_options = True, show_info = "", 
                obj = "unknown", zero = "Salir", color = 1):
        
        # no quiero un scroll al iniciar la aplicación la primera vez        
        if not self._first_init: Logger.scroll_screen()        
        else: self._first_init = False        
        
        max_width = max(len(opcion) for opcion in self.opciones) 
        width     = max(len(self.titulo), max_width) + 4

        self.draw_up(width)
        self.draw_empty(width)
        self.draw_title(width, color=color)

        if extra: self.draw_title(width, obj, color = 3)

        if show_options:
            
            index = 1
            
            if self.max_options is not None:
                options_to_show = self.opciones[:self.max_options]
            else:
                options_to_show = self.opciones
                
            for opcion in options_to_show:
                self.draw_option(index, opcion, width)
                index += 1
               
            self.draw_option(0, zero, width)
           
        cancel = "Ingrese '" + K_USER_CANCEL + "' si desea cancelar"
        if show_info: self.draw_title(width, cancel, 2)
        else: self.draw_empty(width)
        self.draw_down(width)

    def get_option(self, inp = "Seleccione una opción"):
        
        op = input(inp + " = ")
        if op.isdigit(): return int(op)
        else: return -1
        



#from core.models.component import ComponentType
"""
TODO: Trabajo futuro
tanto la responsabilidad de mostrar la información de los modelos como el hecho
de que esta función se llama desde el mismo modelo no está demasiado correcto 
de esta forma. Se tiene que replantear a nivel de diseño.
"""
class Displayer:
    
    #def __init__(self, colored = True):
    #    self._colored = colored        
    def component(model, id, col, tab, p_l, max_id_len):        
        if col:
            id_color    = "\033[1;34m"
            value_color = "\033[1;32m"
            end_color   = "\033[0m"
        else:
            id_color = value_color = end_color = ""
    
        t = "\t- " if tab else ""
        quoted_id = '"' + id + '"'
        formatted_id = quoted_id.ljust(max_id_len + 2)
        
        print(t + id_color + formatted_id + ':' + end_color + " " + value_color
              + model._tipo.value    + ", "
              + str(model._peso)     + "g, "
              + str(model._precio)   + "€, "
              + str(model._cantidad) + " stock." + end_color)
        
    def device(model, id, col, tab, p_l, max_id_len):
        
        """
        Para mostrar de manera personalizada en consola (DISPLAY) sin tener
        que utilizar la clase Logger. Igual que se ha hecho en el modelo 
        'Component' pero para 'Device' (Equipo)
        """        
        if col:
            id_color      = "\033[1;34m"  # Azul en negrita
            info_color    = "\033[1;37m"  # Blanco en negrita
            comp_id_color = "\033[1;36m"  # Cian en negrita
            comp_color    = "\033[1;32m"  # Verde en negrita
            end_color     = "\033[0m"
        else:
            id_color = info_color = comp_id_color = comp_color = end_color = ""
        
        equipo      = info_color + "Equipo/ID = " + end_color 
        id_equipo   = id_color + "'" + id + "'" + end_color + "\n"        
        device_info = equipo + id_equipo
        
        comps_info = ""
        n_components = len(model._components)
        counter = 0
        max_width = max([len(comp_type.value) for comp_type in model._components])
        for comp_type, comp in model._components.items():
            counter += 1
            comp_type_padded = comp_type.value.ljust(max_width)
            comps_info += (comp_color + "\t- " + comp_type_padded + ": " 
                           + comp_id_color + '"' + comp["id"] + '", ' + end_color
                           + comp_color + str(comp["peso"]) + "g, "
                           + str(comp["precio"]) + "€" + end_color)
            if counter != n_components:
                comps_info += "\n"   
        
        print(device_info + comps_info)
        if p_l: Logger.print_line(50, color = True)
        
    def distributor(model, id, col, tab, p_l, max_id_len):
        name = id
        if col:
            name_color  = "\033[1;34m"
            value_color = "\033[1;32m"
            days_color  = "\033[1;33m"  # marillo en negrita
            end_color   = "\033[0m"
        else:
            name_color = value_color = end_color = ""
    
        t = "\t- " if tab else ""
        days = days_color + str(model._delivery_time) + end_color
        l_b = value_color + "(" + end_color
        r_b = value_color + ")" + end_color
        msg = value_color + " días desde fábrica" + end_color
        delivery_time = l_b + days + r_b +  msg
    
        print(t + name_color + 'Nombre   :' + end_color + value_color + ' "'
              + name + '"' + end_color)
        
        print(t + name_color + "Entrega  :" + end_color + " " + delivery_time)
        
        print(t + name_color + "Dirección:" + end_color + value_color + " "  
              + model._address + end_color)
    
        if p_l:
            Logger.print_line(50, color=True)
        
        
        
        
        
    
