#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys,inspect
import json
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from datetime import datetime, timedelta

from src.components.Guardado import Guardado

from src.data_bots.Consumo import Consumo
from src.data_bots.Precio import Precio

from config.Params import Params

start_date = raw_input("Fecha Inicio: ")
end_date = raw_input("Fecha Fin: ")

file_name = raw_input("Nombre de fichero: ")

format = '%d/%m/%Y'
date = datetime.strptime( start_date, format )
end_date = datetime.strptime( end_date, format )

consum = Consumo()

row = {}
while (date <= end_date):
	print( 'Generando datos, día: ' + date.strftime("%d/%m/%Y") )
	# Carga del html en el objeto consum
	consum.setHtmlContent( date.strftime("%Y/%m/%d") )

	row[ date.strftime("%Y/%m/%d") ] = consum.getData()
	date = date + timedelta(days=1)

gdd = Guardado( Params.tmp_directory, file_name + 'consumo.json', json.dumps( row ) )
gdd.saveFile()