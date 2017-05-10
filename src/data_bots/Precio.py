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
		
	def getData( self, date_url, date_json ):
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
					'Cookie'                    : 'path=/; path=/; idvis=2399765328746; browser=true; variant-ab=A; JSESSIONID=yuTzTaY_l5tSojFPvG5vMdivJmfISQ1TRq9447dS_vSAAeFqWmcy!980261269; SS_X_JSESSIONID=m6HzTaZAIfVs5rAXvAmJVvbRMBHFZI5luACTngbYXojijX3GRZII!-1698803091; AlteonP=Ag4lC9EDXgohEJYqJY+aVw$$; _ga=GA1.2.1081176522.1494435604; _gid=GA1.2.1371971358.1494435604; _gat=1; smvr=eyJ2aXNpdHMiOjEsInZpZXdzIjoxLCJ0cyI6MTQ5NDQzNTYwNTQ0MiwibnVtYmVyT2ZSZWplY3Rpb25CdXR0b25DbGljayI6MH0=; smuuid=15bf34dabc3-8270ba3f2152-e43d3412-24248cf2-63cc066a-cfa9391c1368; s_cc=true; s_fid=664EC68923E7B1DB-1482966A3DB6A985; s_ppn=hogares%3Aconoce%20la%20energ%C3%ADa%3Atarifa%20regulada%20pvpc%3Afacturaci%C3%B3n%20por%20horas%3Aprecio%20de%20la%20electricidad%20a%20tiempo%20real%20para%20tarifas%20pvpc; s_nr=1494435620374-New; s_sq=%5B%5BB%5D%5D',
					'Pragma'                    : 'no-cache',
					'Cache-Control'             : 'max-age=0'
		            }

		values = { 'currentDate' : date_url,
		           'currentRate' : 'GEN',
		           '_authkey_'   : '7B2E7B99C6F51180CF47AB7A923AC71F33E4D358A9D254D62850BAB7D1E65D7D34B0F9BDBAD1C23BA4D48110B058F04A' 
		           }

		data = urllib.urlencode(values)

		url = 'https://www.endesaclientes.com/ss/Satellite?pagename=SiteEntry_IB_ES/LandingPrice/GetPrices&rand=30501&rand=30167'
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


