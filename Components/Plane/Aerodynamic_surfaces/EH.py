# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 21:48:21 2018

@author: david
"""
from .Aerodynamic_surfaces import Aerodynamic_surfaces

class EH(Aerodynamic_surfaces):
    def __init__(self, data):
        Aerodynamic_surfaces.__init__(self, data)
