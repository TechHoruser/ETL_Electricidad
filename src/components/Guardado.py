#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

class Guardado(object):
	"""docstring for Guardado"""
	def __init__(self, direc, name, json):
		super(Guardado, self).__init__()
		self.direc = direc
		self.json = json
		self.name = name
		
	def saveFile( self ):
		os.chdir( self.direc )

		file = open( self.name, 'w' )

		file.write( self.json )