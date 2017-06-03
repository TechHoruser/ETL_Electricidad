#!/usr/bin/env python
# -*- coding: utf-8 -*-

from StringIO import StringIO
import time
import urllib
import urllib2
import gzip
import sys
import re
import json

class Precio(object):
	"""docstring for Precio"""
	def __init__(self):
		super(Precio, self).__init__()
		
	def getData( self, date_url, date_json, auth_key, rand_1, rand_2, cookie ):
		headers = {
		            'Host'                      : 'www.endesaclientes.com',
		            'User-Agent'                : 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
		            'Accept'                    : '*/*',
		            'Accept-Language'           : 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
		            'Accept-Encoding'           : 'gzip, deflate, br',
		            'Connection'                : 'keep-alive',
					'Content-Type'              : 'application/x-www-form-urlencoded; charset=UTF-8',
					'Content-Length'            : '145',
					'X-Requested-With'          : 'XMLHttpRequest',
					'Referer'                   : 'https://www.endesaclientes.com/precio-luz-pvpc.html',
					'Cookie'                    : cookie,
					'Pragma'                    : 'no-cache',
					'Cache-Control'             : 'max-age=0'
		            }

		values = { 'currentDate' : date_url,
		           'currentRate' : 'GEN',
		           '_authkey_'   : auth_key
		           }

		data = urllib.urlencode(values)

		url = 'https://www.endesaclientes.com/ss/Satellite?pagename=SiteEntry_IB_ES/LandingPrice/GetPrices&rand=' + rand_1 + '&rand=' + rand_2
		try:
			request  = urllib2.Request(url = url, data = data, headers = headers)
			response = urllib2.urlopen(request)

			# La respuesta llega comprimida por gzip
			if response.info().get('Content-Encoding') == 'gzip':
				buf = StringIO(response.read())
				f = gzip.GzipFile(fileobj=buf)
				result = f.read()
				regex = r"var objArray = (.*);"
				matches = re.finditer(regex, result)
				for matchNum, match in enumerate(matches):
					return self.getJson( json.loads( match.group(1) ), date_json )

		except urllib2.HTTPError as err:
			print "Error capturado: "
			print err.read()
			print err.info()

	def getJson( self, price_json, date ):
		json_return = {
			"Fecha"   : date,
			"Valores" : []
		}

		for val in price_json:
			json_return['Valores'].append({
				"Hora"   : val['Hora'],
				"Precio" : str( (float)( val['GEN'].replace( ',', '.' ) )/1000.0 )
			})

		return json_return


