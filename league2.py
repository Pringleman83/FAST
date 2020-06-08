# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 10:25:19 2019

@author: david
"""
import common_functions as c
class League(object):
    leagues = []
    def __init__ (self, name, season):
        self.leagues.append(self)
        self.league_name = name
        self.league_season = season