#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from beautifulsoupselect import select
from flask import Flask
from StringIO import StringIO
import gzip
import time
import urllib2
import sys
import re
import json

app = Flask(__name__)

@app.route('/consumo/<anio>/<mes>/<dia>')
def getConsumo( anio, mes, dia ):
	html = getHtmlContent( anio, mes, dia )
	data = getData( html )
	return data

def getHtmlContent( anio, mes, dia ):
	headers = {
                'Host'                      : 'www.ree.es',
                'User-Agent'                : 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
                'Accept'                    : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language'           : 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
                'Accept-Encoding'           : 'gzip, deflate',
                'Connection'                : 'keep-alive',
                'Upgrade-Insecure-Requests' : '1'
                }

	url = 'http://www.ree.es/es/balance-diario/nacional/'+anio+'/'+mes+'/'+dia
	try:
		request  = urllib2.Request(url, headers = headers)
		response = urllib2.urlopen(request)

		# La respuesta llega comprimida por gzip
		if response.info().get('Content-Encoding') == 'gzip':
			buf = StringIO(response.read())
			f = gzip.GzipFile(fileobj=buf)
			return f.read()

	except urllib2.HTTPError as err:
		print "Error capturado: "
		print err.read()
		print err.info()

def getData( html ):
	soup = BeautifulSoup(html, 'html5lib')
	selector = soup.select('.datos')

	enlaces = []
	for item in selector:
		energias_renovables = [
			'Hidr\u00e1ulica',
			'Hidroeólica',
			'Eólica',
			'Solar fotovoltaica',
			'Solar térmica',
			'Otras renovables (5)'
		]
		excluir = [
			'Generación',
			'Demanda transporte(b.c.)',
			'Demanda corregida (9)',
			'Demanda distribución',
			'Total (10)'
		]
		# energias_renovables = [
		# 	'Hidráulica'.encode( 'utf-8' ),
		# 	'Hidroeólica'.encode( 'utf-8' ),
		# 	'Eólica'.encode( 'utf-8' ),
		# 	'Solar fotovoltaica'.encode( 'utf-8' ),
		# 	'Solar térmica'.encode( 'utf-8' ),
		# 	'Otras renovables (5)'.encode( 'utf-8' )
		# ]
		# excluir = [
		# 	'Generación'.encode( 'utf-8' ),
		# 	'Demanda transporte(b.c.)'.encode( 'utf-8' ),
		# 	'Demanda corregida (9)'.encode( 'utf-8' ),
		# 	'Demanda distribución'.encode( 'utf-8' ),
		# 	'Total (10)'.encode( 'utf-8' )
		# ]
		if item.next_element.text not in excluir:
			tipo    = item.next_element.text
			consumo = item.next_element.next_sibling.text

			enlaces.append({
				'Tipo'      : tipo,
				'Consumo'   : consumo,
				'Renovable' : 'true' if tipo in energias_renovables else 'false'
				})

	return json.dumps(enlaces)


if __name__ == '__main__':
    app.run()
