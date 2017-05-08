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
	def __init__(self, arg):
		super(Precio, self).__init__()
		
	def getData( self, anio, mes, dia ):
		headers = {
		            'Host'                      : 'www.endesaclientes.com',
		            'User-Agent'                : 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
		            'Accept'                    : '*/*',
		            'Accept-Language'           : 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
		            'Accept-Encoding'           : 'gzip, deflate, br',
		            'Connection'                : 'keep-alive',
					'Content-Type'              : 'application/x-www-form-urlencoded; charset=UTF-8',
					'X-Requested-With'          : 'XMLHttpRequest',
					'Referer'                   : 'https://www.endesaclientes.com/precio-luz-pvpc.html',
					'Content-Length'            : '145',
					'Cookie'                    : 'path=/; _ga=GA1.2.1969013905.1490631616; variant-ab=A; idvis=2399743913468; smvr=eyJ2aXNpdHMiOjIsInZpZXdzIjo1LCJ0cyI6MTQ5MTI0MTA1MjE4MSwibnVtYmVyT2ZSZWplY3Rpb25CdXR0b25DbGljayI6MH0=; smuuid=15b10916e07-3f51b4928f58-cfc2cdf7-d402d3a2-edd37c1c-84b159099b6a; s_fid=6C7B4CD94E372B0D-11962E1D613DF644; s_nr=1491241089447-Repeat; _webo=jQeQdqI6CSWN45; privPol=1; JSESSIONID=RZQ05LALMtCmggziOHuDiCp_i5Bp_G0dQavcix-cbDIBxBEWVppt!-1349006667; path=/; browser=true; SS_X_JSESSIONID=sr805LnvZUBoyrpS7G88HpSHGn41v80s6SpoBTu-OW4ZuQYmcf_B!1999005620; AlteonP=Ag21C9EDXgrgWFdqKgtJGw$$; _gat=1; s_cc=true; s_ppn=hogares%3Aconoce%20la%20energ%C3%ADa%3Atarifa%20regulada%20pvpc%3Afacturaci%C3%B3n%20por%20horas%3Aprecio%20de%20la%20electricidad%20a%20tiempo%20real%20para%20tarifas%20pvpc; s_sq=%5B%5BB%5D%5D',
					'Connection'                : 'keep-alive',
					'Pragma'                    : 'no-cache',
					'Cache-Control'             : 'no-cache',
		            'Upgrade-Insecure-Requests' : '1'
		            }

		values = { 'currentDate' : anio+'-'+mes+'-'+dia,
		           'currentRate' : 'GEN',
		           '_authkey_'   : 'B1A8BA205BB494C5588AD0117E11F4C1D8669B06D9D818A348BC6C935EFB03AC057E4EF385DF4BE09A0C8930BDE0F11E' 
		           }

		data = urllib.urlencode(values)

		url = 'https://www.endesaclientes.com/ss/Satellite?pagename=SiteEntry_IB_ES/LandingPrice/GetPrices&rand=19251&rand=29253'
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
					print (match.group(1))

		except urllib2.HTTPError as err:
			print "Error capturado: "
			print err.read()
			print err.info()

