# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 23:45:20 2023

@author: Jose

Con propositos de testeo y debug. Se debe habilitar desde las constantes en
settings.py
"""

from config.settings import K_DEBUG_ALL, K_DEBUG_TESTS_COMPONENTS

def debug_components(comp_dic):
    
    if K_DEBUG_TESTS_COMPONENTS or K_DEBUG_ALL:
        
        from core.models.component import Component, ComponentType
        
        comp1 = Component()
        comp1.set_from_user_data((ComponentType.FUENTE, 200, 159.99, 1))
        comp_dic["C0MP-i01"] = comp1
        comp2 = Component()
        comp2.set_from_user_data((ComponentType.FUENTE, 120, 120.99, 4))
        comp_dic["C0MP-i02"] = comp2
        comp3 = Component()
        comp3.set_from_user_data((ComponentType.FUENTE, 68, 100.99, 2))
        comp_dic["C0MP-i03"] = comp3
        
        comp4 = Component()
        comp4.set_from_user_data((ComponentType.PB, 38, 45.99, 2))
        comp_dic["C0MP-i04"] = comp4
        comp5 = Component()
        comp5.set_from_user_data((ComponentType.PB, 93, 75.99, 3))
        comp_dic["C0MP-i05"] = comp5
        
        comp6 = Component()
        comp6.set_from_user_data((ComponentType.TG, 110, 35.99, 1))
        comp_dic["C0MP-i06"] = comp6
        comp7 = Component()
        comp7.set_from_user_data((ComponentType.TG, 145, 99.99, 2))
        comp_dic["C0MP-i07"] = comp7
        
        comp8 = Component()
        comp8.set_from_user_data((ComponentType.CPU, 145, 99.99, 3))
        comp_dic["C0MP-i08"] = comp8        
        
        comp9 = Component()
        comp9.set_from_user_data((ComponentType.RAM, 33, 399.99, 3))
        comp_dic["C0MP-i09"] = comp9    

        comp10 = Component()
        comp10.set_from_user_data((ComponentType.DISCO, 24, 55.13, 3))
        comp_dic["C0MP-i10"] = comp10
    
    
    

