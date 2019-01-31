# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 14:33:30 2018

@author: david
"""

from .Aerodynamic_surfaces import Aerodynamic_surfaces

class Wing(Aerodynamic_surfaces):
    def __init__(self, data):
        Aerodynamic_surfaces.__init__(self, data)

