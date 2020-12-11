# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/archivostv/Modulos/ArchivostvModulos.py
# coding: utf-8
from xml.etree.cElementTree import fromstring, ElementTree
import urllib2
import urllib as ul
import os, re

def Excepcion(texto = '', donde = ''):
    print "Error: " + str(texto) + " " + str(donde)
    print "Error: " + str(texto) + " " + str(donde)
    print "Error: " + str(texto) + " " + str(donde)
    
def debug(texto = ''):
    print str(texto)
    
def CambiaTexto(texto):
    NN = texto
    NN = NN.replace("¡","")
    NN = NN.replace("¿","")
    NN = NN.replace("?","")
    NN = NN.replace(":","")
    NN = NN.replace("º","")
    NN = NN.replace("ª","")
    NN = NN.replace("\"","")
    NN = NN.replace("\'","")
    NN = NN.replace("(","")
    NN = NN.replace(")","")
    NN = NN.replace("á","a")
    NN = NN.replace("Á","A")
    NN = NN.replace("é","e")
    NN = NN.replace("É","E")
    NN = NN.replace("í","i")
    NN = NN.replace("Í","I")
    NN = NN.replace("ó","o")
    NN = NN.replace("Ó","O")
    NN = NN.replace("ú","u")
    NN = NN.replace("Ú","U")
    NN = NN.replace("ñ","n")
    NN = NN.replace("Ñ","N")
    NN = NN.replace("&ntilde;","n")
    NN = NN.replace("&quot;","")
    NN = NN.replace("&aacute;","a")
    NN = NN.replace("&eacute;","e")
    NN = NN.replace("&iacute;","i")
    NN = NN.replace("&oacute;","o")
    NN = NN.replace("&uacute;","u")
    NN = NN.replace("&laquo;","")
    NN = NN.replace("&raquo;","")
    NN = NN.replace("'","")
    NN = NN.replace("&#039;","")
    NN = NN.replace('\xc3\xb1','n')
    NN = NN.replace('\xc3\x81','A')
    NN = NN.replace('\xc3\xa1','a')
    NN = NN.replace('\xc3\x8d','I')
    NN = NN.replace('\xc3\xad','i')
    NN = NN.replace('\xc3\x89','E')
    NN = NN.replace('\xc3\xa9','e')
    NN = NN.replace('\xc3\x93','O')
    NN = NN.replace('\xc3\xb3','o')
    NN = NN.replace('\xc3\x9a','U')
    NN = NN.replace('\xc3\xba','u')
    return NN

def mod_request(url):
	url = 'http://' + url
	html = ''
	try:
		debug(url, 'MODUL REQUEST URL')
		req = urllib2.Request(url, None, {'User-agent': 'Mozilla/5.0 Archivostv 0.1', 'Connection': 'Close'})
		html = urllib2.urlopen(req).read() 
		#print html
	except Exception, ex:
		print ex
		print 'REQUEST Exception'
	return html
	    
class html_parser_moduls:
	
	def __init__(self):
		self.video_list = []
		self.next_page_url = ''
		self.next_page_text = ''
		self.prev_page_url = ''
		self.prev_page_text = ''
		self.search_text = ''
		self.search_on = ''
		self.active_site_url = ''
		self.playlistname = ''
		self.playlist_cat_name = ''
		self.kino_title = ''
		self.category_back_url = ''

	def reset_buttons(self):
		self.kino_title = ''
		self.next_page_url = None
		self.next_page_text = ''
		self.prev_page_url = None
		self.prev_page_text = ''
		self.search_text = ''
		self.search_on = None

	def get_list(self, url):
		debug(url, 'MODUL URL: ')
		self.reset_buttons() 