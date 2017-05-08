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

class Consumo(object):
	"""docstring for Consumo"""
	def __init__(self):
		super(Consumo, self).__init__()

	def setHtmlContent( self, date ):
		headers = {
	                'Host'                      : 'www.ree.es',
	                'User-Agent'                : 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
	                'Accept'                    : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	                'Accept-Language'           : 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
	                'Accept-Encoding'           : 'gzip, deflate',
	                'Connection'                : 'keep-alive',
	                'Upgrade-Insecure-Requests' : '1'
	                }

		url = 'http://www.ree.es/es/balance-diario/nacional/'+date
		try:
			request  = urllib2.Request(url, headers = headers)
			response = urllib2.urlopen(request)

			# La respuesta llega comprimida por gzip
			if response.info().get('Content-Encoding') == 'gzip':
				buf = StringIO(response.read())
				f = gzip.GzipFile(fileobj=buf)
				self.html = f.read()

		except urllib2.HTTPError as err:
			print "Error capturado: "
			print err.read()
			print err.info()

	def getData( self ):
		soup = BeautifulSoup( self.html, 'html5lib')
		selector = soup.select('.datos')

		enlaces = []
		for item in selector:
			energias_renovables = [
				'Hidráulica',
				'Hidroeólica',
				'Eólica',
				'Solar fotovoltaica',
				'Solar térmica',
				'Otras renovables (5)'
			]
			excluir = [
				'Generación',
				'Consumo en bombeo',
				'Enlace Península-Baleares (7)',
				'Saldo intercambios internacionales (8)',
				'Demanda transporte(b.c.)',
				'Demanda corregida (9)',
				'Pérdidas en transporte',
				'Demanda distribución',
				'Total (10)'
			]
			if item.next_element.text.encode( 'utf-8' ) not in excluir:
				tipo    = item.next_element.text
				consumo = item.next_element.next_sibling.text

				enlaces.append({
					'Tipo'      : tipo,
					'Consumo'   : consumo,
					'Renovable' : 'true' if tipo.encode( 'utf-8' ) in energias_renovables else 'false'
					})

		return enlaces


