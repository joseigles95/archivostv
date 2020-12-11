# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/cosas/archivostv/hdfull.py
# coding: utf-8

import re, os, time, datetime, traceback, urllib, cookielib
import urllib2
import httplib, mimetypes
import shutil
import sys
import json
import hashlib
import Teclado
import jsontools
import scrapertools
import httptools
import base64
import urllib
import urlparse
from enigma import eTimer
from ArchivostvModulos import Excepcion as Log
from ArchivostvModulos import debug, CambiaTexto

RUTAPLUGIN = "/usr/lib/enigma2/python/Plugins/Extensions/archivostv/"
RUTACOOKIE = "/usr/lib/enigma2/python/Plugins/Extensions/archivostv/cookies/cookieshd.dat"
RutaTMP = "/tmp/archivostv/"
user_agent_default = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"

ARPORDEDE = RUTAPLUGIN+"/cosas/hdfull.py"
ARPORDEDEO = RUTAPLUGIN+"/cosas/hdfull.pyo"

TKN = ""
USR = ""
PSW = ""
Mediaitem = ""
Sesion = ""

OTRO = 0
host = 'https://hdfull.lv/'

cj = cookielib.MozillaCookieJar()

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
OP = opener.open

LogeadoDD = False

cookiepath = RutaTMP

def Crea_Archivo(nombreArchivo, nombreLista, nombreChanel, imagen, enlace, imgDefi, tipo, historial):

    Categ = nombreArchivo
    FF = open(Categ, 'w')
    FF.write('<?xml version="1.0" encoding="iso-8859-1"?>\n<items>\n<playlist_name><![CDATA[' + NN + ']]></playlist_name>\n\n')

def load_cookies():
    if os.path.isfile(RUTACOOKIE):
        
        try:
            debug("Cargando cookies")
            cj.load(RUTACOOKIE, ignore_discard=True)
        except:
            Log("No cargamos cookies, error", "Cookies de HDFULL")
            pass
    else:
        debug(RUTACOOKIE)
        cj.save(RUTACOOKIE, ignore_discard=True)
        debug("No existe el fichero de cookies megadede")
        
def save_cookies():
    cj.save(RUTACOOKIE, ignore_discard=True)
    debug("Guardando las cookies")

def Version():
    V = 101
    return V

def CompruebaLoginHD(self):
    load_cookies()
    url = 'https://hdfull.lv/'
    req = urllib2.Request(url)
    req.add_header('User-Agent', user_agent_default)
    Abrir = OP(req, timeout=20)
    data = Abrir.read()
    Abrir.close()
    
    if data.find('<a href="https://hdfull.lv/user/plugine2" class="tour-join2 join">Bienvenido plugine2</a>') != -1:
        #Lo encuentra, entonces estamos logeados.
        return True
    else:
        #print data
        #No lo encuentra, asi que estamos deslogeados.
        return False

def Logear(self, usuario, contra):
    try:
        global USR
        global PSW
        global TKN
        global Mediaitem
        global Sesion
        
        load_cookies()
        Sesion = self.session

        
        LOGIN = usuario
        PASSWORD = contra
        
        USR = LOGIN
        PSW = PASSWORD
        
        url_origen = 'https://hdfull.lv/'
        req = urllib2.Request(url_origen)
        req.add_header('User-Agent', user_agent_default)
        Abrir = OP(req, timeout=20)
        data = Abrir.read()
        Abrir.close()
        
        GetName = re.findall(r'login_form"><.+name=\'(.*?)\'', data)
        GetToken = re.findall(r'login_form">.+value="(.*?)"', data)

        
        NameToken = GetName[0]
        Token = GetToken[0]
        
        url = 'https://hdfull.lv/'
        post = str(NameToken) + '=' + str(Token) + '&username=' + USR + '&password=' + PSW + '&action=login'
        
        req = urllib2.Request(url)
        req.add_header('User-Agent', user_agent_default)
        req.add_header('Referer', 'https://hdfull.lv/')
        Abrir = OP(req, data=post)
        data = Abrir.read()
        Abrir.close()
        
        save_cookies()
        
        XXX = CompruebaLoginHD(self)
        
        return XXX
    except Exception as er:
        Log(str(er), "En Logear HDFULL")
        return [1, er]
        
def NavegarEstrenos(self, Nam, Pagina):
    try:
        global opener
        global OTRO
        
        NN = Nam
        NN = CambiaTexto(NN)
        PAG = Pagina
        PG = PAG
        
        Categ = RutaTMP + NN + str(PG) + ".xml"
        
        url = 'https://hdfull.lv/peliculas-estreno'
        PAG = int(PAG)
        
        req = urllib2.Request(url)
        req.add_header('User-Agent',user_agent_default)
        req.add_header('Referer','https://hdfull.lv/')
        Abrir = OP(req)
        data = Abrir.read()
        Abrir.close()
        
        Recopila = re.findall(r'href="(.*?)".+\s+.+src="(.*?)"\s.+title="(.*?)"\sst', data)
        IDS = re.findall(r'data-seen="(.*?)"', data)
        
        if PAG == 0:
            i = 1
        else:
            i = PAG+1
            
        FF = open(Categ, 'w')
        FF.write('<?xml version="1.0" encoding="iso-8859-1"?>\n<items>\n<playlist_name><![CDATA[' + NN + ']]></playlist_name>\n\n')
        
        Conteo = 0
        
        if Recopila == []:
            Mensaje = "Error","No hay mas resultados aqui."
            FF.close()
            return [1, Mensaje]
        else:
            for enlace,imagen,titulo in Recopila:
                ID = IDS[Conteo]
                Conteo = Conteo + 1
                ENLA = enlace
                if '/serie' in ENLA or "/tags-tv" in ENLA:
                    ENLA += "###" + ID + ";1"
                else:
                    ENLA += "###" + ID + ";2"
                NN = titulo.encode('utf8')
                NN = CambiaTexto(NN)
                IMAG = imagen
                
                ImgDefinitiva = ObtenImagenes(self, IMAG)
                
                #FF.write("type=poraa\nname=" + NN.encode('utf8') +"\nthumb=" + IMAG + "\nURL=" + ENLA + "\ndescription=./description\n\n")
                FF.write("<channel>\n")
                FF.write("    <title><![CDATA[" + NN.encode('utf8') + "]]></title>\n")
                FF.write('    <description><![CDATA[<img src="' + IMAG + '">]]></description>\n')
                FF.write('    <playlist_url><![CDATA[' + ENLA + ']]></playlist_url>\n')
                FF.write('    <img_src><![CDATA[' + ImgDefinitiva + ']]></img_src>\n')
                FF.write('    <tipo><![CDATA[hdfullEnlaces]]></tipo>\n')
                FF.write('    <historial><![CDATA[' + Categ +']]></historial>\n')
                FF.write('</channel>\n\n')
                
            
            if Conteo < 58:
                pass
            else:
                FF.write("<channel>\n")
                FF.write("    <title><![CDATA[Pagina Siguiente]]></title>\n")
                FF.write('    <description><![CDATA[<img src="http://ps3plusteam.ddns.net/ps3plus/images/letras/siguiente.png">]]>Avanza a la pagina siguiente para ver mas peliculas!</description>\n')
                FF.write('    <img_src><![CDATA[http://ps3plusteam.ddns.net/ps3plus/images/letras/siguiente.png]]></img_src>\n')
                FF.write('    <ts_stream><![CDATA[' + str(i) + ']]></ts_stream>\n')
                FF.write('    <tipo><![CDATA[hdfullEstrenos]]></tipo>\n')
                FF.write('    <historial><![CDATA[' + Categ +']]></historial>\n')
                FF.write('</channel>\n\n')
                
            
            if i == 1:
                FF.write('<prev_page_url text="CH- ATRAS"><![CDATA[/cosas/hdfull.xml]]></prev_page_url>\n</items>')
            if i == 2:
                FF.write('<prev_page_url text="CH- ATRAS"><![CDATA[/tmp/archivostv/Navegar en Estrenos0.xml]]></prev_page_url>\n</items>')
            if i > 2:
                i = i - 1
                FF.write('<prev_page_url text="CH- ATRAS"><![CDATA[/tmp/archivostv/Pagina Siguiente' + str(i - 1) + '.xml]]></prev_page_url>\n</items>')
            
            
            FF.close()
            
            return Categ
            
    except Exception as er:
        Log(str(er), "En NavegarEstrenos HDFULL")
        return [1, er]
        
def Enlaces(self, Nam, URLL = "", THUMB = "", historial = ""):

    NN = Nam
    NN = CambiaTexto(NN)
    ENN = URLL
    IMG = THUMB

    Categ = RutaTMP + NN + ".xml"
    
    if "###" in ENN:
        id = ENN.split("###")[1].split(";")[0]
        type = ENN.split("###")[1].split(";")[1]
        ENN = ENN.split("###")[0]
        
    
    itemlist = []
    it1 = []
    it2 = []
    
    url_targets = ENN

    data_js = httptools.downloadpage("http://ps3plusteam.ddns.net/hdfull/jquery.hdfull.view.min.js", headers={'referer': 'http://ps3plusteam.ddns.net/'}).data
    key = scrapertools.find_single_match(data_js, 'JSON.parse\(atob.*?substrings\((.*?)\)')

    data_js = httptools.downloadpage("http://ps3plusteam.ddns.net/hdfull/providers.js", headers={'referer': 'http://ps3plusteam.ddns.net/'}).data

    decoded = jhexdecode(data_js).replace("'", '"')
    providers_pattern = 'p\[(\d+)\]= {"t":"([^"]+)","d":".*?","e":.function.*?,"l":.function.*?return "([^"]+)".*?};'
    providers = scrapertools.find_multiple_matches (decoded, providers_pattern)
    provs = {}
    for provider, e, l in providers:
        provs[provider]=[e,l]

    data = agrupa_datos(ENN)
    
    Sinop = ""
    
    if ENN.find("pelicula") != -1:
        buscaSinopsis = re.findall(r'itemprop="description">(.*?)<br', data)
        Sinop = CambiaTexto(buscaSinopsis[0])
        
    if ENN.find("serie/") != -1:
        buscaSinopsis = re.findall(r'itemprop="description">(.*?)<br', data)
        Sinop = CambiaTexto(buscaSinopsis[0])
    
    data_obf = scrapertools.find_single_match(data, "var ad\s*=\s*'([^']+)'")

    data_decrypt = jsontools.load(obfs(base64.b64decode(data_obf), 126 - int(key)))
    
    FF = open(Categ, 'w')
    FF.write('<?xml version="1.0" encoding="iso-8859-1"?>\n<items>\n<playlist_name><![CDATA[' + NN + ']]></playlist_name>\n\n')
    
    Conteo = 0
    matches = []
    for match in data_decrypt:
        if match['provider'] in provs:
            try:
                embed = provs[match['provider']][0]
                url = provs[match['provider']][1]+match['code']
                matches.append([match['lang'], match['quality'], url, embed])
            except:
                pass
    
    for idioma, calidad, url, embed in matches:
        if embed == 'd':
            option = "Descargar"
            option1 = 2
            
            if idioma == "ESP":
                if url.find('uptobox') != -1:
                    Conteo = Conteo + 1
                    FF.write("<channel>\n")
                    FF.write("    <title><![CDATA[Ver en " + idioma + " " + NN.encode('utf8') + " " + calidad + "]]></title>\n")
                    FF.write('    <description><![CDATA[' + IMG + ']]>' + Sinop + '</description>\n')
                    FF.write('    <playlist_url><![CDATA[' + url + ']]></playlist_url>\n')
                    FF.write('    <stream_url><![CDATA[http://ps3plusteam.ddns.net/teamps3plus/pro/uptobox.txt]]></stream_url>\n')
                    FF.write('    <img_src><![CDATA[http://ps3plusteam.ddns.net/ps3plus/images/letras/uptobox.png]]></img_src>\n')
                    FF.write('    <tipo><![CDATA[hdfullLinks]]></tipo>\n')
                    FF.write('</channel>\n\n') 
        else:
            option = "Ver"
            option1 = 1
            
            if idioma == "ESP":
                Conteo = Conteo + 1
                print url
                if url.find('vidoza') != -1:
                    FF.write("<channel>\n")
                    FF.write("    <title><![CDATA[Ver en vidoza" + idioma + " " + NN.encode('utf8') + " " + calidad + "]]></title>\n")
                    FF.write('    <description><![CDATA[' + IMG + ']]>' + Sinop + '</description>\n')
                    FF.write('    <playlist_url><![CDATA[' + url + ']]></playlist_url>\n')
                    FF.write('    <stream_url><![CDATA[http://ps3plusteam.ddns.net/teamps3plus/pro/vidoza.txt]]></stream_url>\n')
                    FF.write('    <img_src><![CDATA[http://ps3plusteam.ddns.net/ps3plus/images/letras/vidoza.png]]></img_src>\n')
                    FF.write('    <tipo><![CDATA[hdfullLinks]]></tipo>\n')
                    FF.write('</channel>\n\n')   
                if url.find('vidia') != -1:
                    print "Entramos en vidia"
                    FF.write("<channel>\n")
                    FF.write("    <title><![CDATA[Ver en vidia " + idioma + " " + NN.encode('utf8') + " " + calidad + "]]></title>\n")
                    FF.write('    <description><![CDATA[' + IMG + ']]>' + Sinop + '</description>\n')
                    FF.write('    <playlist_url><![CDATA[' + url + ']]></playlist_url>\n')
                    FF.write('    <stream_url><![CDATA[http://ps3plusteam.ddns.net/teamps3plus/pro/vidia.txt]]></stream_url>\n')
                    FF.write('    <img_src><![CDATA[http://ps3plusteam.ddns.net/ps3plus/images/letras/vidia.png]]></img_src>\n')
                    FF.write('    <tipo><![CDATA[hdfullLinks]]></tipo>\n')
                    FF.write('</channel>\n\n')
                if url.find('vidtodo') != -1:
                    FF.write("<channel>\n")
                    FF.write("    <title><![CDATA[Ver en vidtodo " + idioma + " " + NN.encode('utf8') + " " + calidad + "]]></title>\n")
                    FF.write('    <description><![CDATA[' + IMG + ']]>' + Sinop + '</description>\n')
                    FF.write('    <playlist_url><![CDATA[' + url + ']]></playlist_url>\n')
                    FF.write('    <stream_url><![CDATA[http://ps3plusteam.ddns.net/teamps3plus/pro/vidtodo.txt]]></stream_url>\n')
                    FF.write('    <img_src><![CDATA[http://ps3plusteam.ddns.net/ps3plus/images/letras/vidtodo.png]]></img_src>\n')
                    FF.write('    <tipo><![CDATA[hdfullLinks]]></tipo>\n')
                    FF.write('</channel>\n\n')
                if url.find('clipwatching') != -1:
                    FF.write("<channel>\n")
                    FF.write("    <title><![CDATA[Ver en clipwatching " + idioma + " " + NN.encode('utf8') + " " + calidad + "]]></title>\n")
                    FF.write('    <description><![CDATA[' + IMG + ']]>' + Sinop + '</description>\n')
                    FF.write('    <playlist_url><![CDATA[' + url + ']]></playlist_url>\n')
                    FF.write('    <stream_url><![CDATA[http://ps3plusteam.ddns.net/teamps3plus/pro/clipwatching.txt]]></stream_url>\n')
                    FF.write('    <img_src><![CDATA[http://ps3plusteam.ddns.net/ps3plus/images/letras/clipwatching.png]]></img_src>\n')
                    FF.write('    <tipo><![CDATA[hdfullLinks]]></tipo>\n')
                    FF.write('</channel>\n\n')   
                if url.find('gamovideo') != -1:
                    Conteo = Conteo + 1
                    buscaID = re.findall(r'com/(.*)', url)
                    buscaID = buscaID[0]
                    FF.write("<channel>\n")
                    FF.write("    <title><![CDATA[Ver en gamovideo " + idioma + " " + NN.encode('utf8') + " " + calidad + "]]></title>\n")
                    FF.write('    <description><![CDATA[' + IMG + ']]>' + Sinop + '</description>\n')
                    FF.write('    <playlist_url><![CDATA[http://gamovideo.com/embed-' + buscaID + '-640x360.html]]></playlist_url>\n')
                    FF.write('    <stream_url><![CDATA[http://ps3plusteam.ddns.net/teamps3plus/props3/gamo.txt]]></stream_url>\n')
                    FF.write('    <img_src><![CDATA[http://ps3plusteam.ddns.net/ps3plus/images/letras/gamovideo.png]]></img_src>\n')
                    FF.write('    <tipo><![CDATA[hdfullLinks]]></tipo>\n')
                    FF.write('</channel>\n\n')
                     
    FF.write('<prev_page_url text="CH- ATRAS"><![CDATA[' + historial + ']]></prev_page_url>\n</items>')
    
    if Conteo == 0:
        return None
    
    return Categ

def jhexdecode(t):
    r = re.sub(r'_\d+x\w+x(\d+)', 'var_' + r'\1', t)
    r = re.sub(r'_\d+x\w+', 'var_0', r)
    def to_hx(c):
        h = int("%s" % c.groups(0), 16)
        if 19 < h < 160:
            return chr(h)
        else:
            return ""
    r = re.sub(r'(?:\\|)x(\w{2})', to_hx, r).replace('var ', '')
    f = eval(scrapertools.find_single_match(r, '\s*var_0\s*=\s*([^;]+);'))
    for i, v in enumerate(f):
        r = r.replace('[[var_0[%s]]' % i, "." + f[i])
        r = r.replace(':var_0[%s]' % i, ":\"" + f[i] + "\"")
        r = r.replace(' var_0[%s]' % i, " \"" + f[i] + "\"")
        r = r.replace('(var_0[%s]' % i, "(\"" + f[i] + "\"")
        r = r.replace('[var_0[%s]]' % i, "." + f[i])
        if v == "": r = r.replace('var_0[%s]' % i, '""')
    r = re.sub(r':(function.*?\})', r":'\g<1>'", r)
    r = re.sub(r':(var[^,]+),', r":'\g<1>',", r)
    return r
    
def obfs(data, key, n=126):
    #if PY3: data = "".join(chr(x) for x in bytes(data))
    chars = list(data)
    for i in range(0, len(chars)):
        c = ord(chars[i])
        if c <= n:
            number = (ord(chars[i]) + key) % n
            chars[i] = chr(number)
    return "".join(chars)
    
def agrupa_datos(url, post=None):
    req = urllib2.Request(url)
    req.add_header('User-Agent',user_agent_default)
    req.add_header('Referer','https://hdfull.lv/')
    Abrir = OP(req)
    data = Abrir.read()
    Abrir.close()
    
    ## Agrupa los datos
    data = re.sub(r'\n|\r|\t|&nbsp;|<br>|<!--.*?-->', '', data)
    data = re.sub(r'\s+', ' ', data)
    data = re.sub(r'>\s<', '><', data)
    return data
        
def ObtenImagenes(self, enlace):
    try:
        m = hashlib.md5()
        m.update(enlace)
        cover_md5 = m.hexdigest()
        
        req = urllib2.Request(enlace)
        req.add_header('User-Agent',user_agent_default)
        Abrir = OP(req, timeout=8)
        data = Abrir.read()
        Abrir.close()
        
        self.picfile = '%s%s.jpg' % (RutaTMP, cover_md5)
        FF = open(self.picfile, 'w')
        FF.write(data)
        FF.close()
        
        return self.picfile
        
    except Exception as err:
        print err
        print err
        print err
        if os.path.isfile(self.picfile):
            try:
                os.remove(self.picfile)
            except:
                pass
######################################################
def NavegarSeries(self, Nam, Pagina):
    try:
        global opener
        global OTRO
        
        NN = Nam
        NN = CambiaTexto(NN)
        PAG = Pagina
        PG = PAG
        
        Categ = RutaTMP + NN + str(PG) + ".xml"
        
        url = 'https://hdfull.lv/series'
        PAG = int(PAG)
        
        req = urllib2.Request(url)
        req.add_header('User-Agent',user_agent_default)
        req.add_header('Referer','https://hdfull.lv/')
        Abrir = OP(req)
        data = Abrir.read()
        Abrir.close()
        
        Recopila = re.findall(r'href="(.*?)".+\s+.+src="(.*?)"\s.+title="(.*?)"\s\/>\s+<\/a>', data)
        IDS = re.findall(r'setFavorite\(\d+, (.*?), \d', data)
        
        if PAG == 0:
            i = 1
        else:
            i = PAG+1
            
        FF = open(Categ, 'w')
        FF.write('<?xml version="1.0" encoding="iso-8859-1"?>\n<items>\n<playlist_name><![CDATA[' + NN + ']]></playlist_name>\n\n')
        
        Conteo = 0
        
        if Recopila == []:
            Mensaje = "Error","No hay mas resultados aqui."
            FF.close()
            return [1, Mensaje]
        else:
            for enlace,imagen,titulo in Recopila:
                ID = IDS[Conteo]
                Conteo = Conteo + 1
                ENLA = enlace
                if '/serie' in ENLA or "/tags-tv" in ENLA:
                    ENLA += "###" + ID + ";1"
                else:
                    ENLA += "###" + ID + ";2"
                NN = titulo
                NN = CambiaTexto(NN)
                IMAG = imagen
                
                ImgDefinitiva = ObtenImagenes(self, IMAG)
                
                #FF.write("type=poraa\nname=" + NN.encode('utf8') +"\nthumb=" + IMAG + "\nURL=" + ENLA + "\ndescription=./description\n\n")
                FF.write("<channel>\n")
                FF.write("    <title><![CDATA[" + NN.encode('utf8') + "]]></title>\n")
                FF.write('    <description><![CDATA[<img src="' + IMAG + '">]]></description>\n')
                FF.write('    <playlist_url><![CDATA[' + ENLA + ']]></playlist_url>\n')
                FF.write('    <img_src><![CDATA[' + ImgDefinitiva + ']]></img_src>\n')
                FF.write('    <tipo><![CDATA[hdfullCapitulos]]></tipo>\n')
                FF.write('    <historial><![CDATA[' + Categ +']]></historial>\n')
                FF.write('</channel>\n\n')
                
            
            FF.write('<prev_page_url text="CH- ATRAS"><![CDATA[/cosas/hdfull.xml]]></prev_page_url>\n</items>')
            FF.close()
            
            return Categ
            
    except Exception as er:
        Log(str(er), "En NavegarSeries HDFULL")
        return [1, er]
        
def NavegarAZ(self, Nam, URLL = "", Pagina = "", historial = ""):
    try:
        global opener
        global OTRO
        
        NN = Nam
        NN = CambiaTexto(NN)
        
        Categ = RutaTMP + NN + "1.xml"
        
        url = URLL
        req = urllib2.Request(url)
        req.add_header('User-Agent',user_agent_default)
        req.add_header('Referer','https://hdfull.lv/')
        Abrir = OP(req)
        data = Abrir.read()
        Abrir.close()
        
        Recopila = re.findall(r'href="(.*?)".+\s+.+src="(.*?)"\s.+title="(.*?)"\s\/>\s+<\/a>', data)
        IDS = re.findall(r'setFavorite\(\d+, (.*?), \d', data)
            
        FF = open(Categ, 'w')
        FF.write('<?xml version="1.0" encoding="iso-8859-1"?>\n<items>\n<playlist_name><![CDATA[' + NN + ']]></playlist_name>\n\n')
        
        Conteo = 0
        
        if Recopila == []:
            Mensaje = "Error","No hay mas resultados aqui."
            FF.close()
            return [1, Mensaje]
        else:
            for enlace,imagen,titulo in Recopila:
                ID = IDS[Conteo]
                Conteo = Conteo + 1
                ENLA = enlace
                if '/serie' in ENLA or "/tags-tv" in ENLA:
                    ENLA += "###" + ID + ";1"
                else:
                    ENLA += "###" + ID + ";2"
                NN = titulo
                NN = CambiaTexto(NN)
                IMAG = imagen
                
                ImgDefinitiva = ObtenImagenes(self, IMAG)
                
                #FF.write("type=poraa\nname=" + NN.encode('utf8') +"\nthumb=" + IMAG + "\nURL=" + ENLA + "\ndescription=./description\n\n")
                FF.write("<channel>\n")
                FF.write("    <title><![CDATA[" + NN.encode('utf8') + "]]></title>\n")
                FF.write('    <description><![CDATA[<img src="' + IMAG + '">]]></description>\n')
                FF.write('    <playlist_url><![CDATA[' + ENLA + ']]></playlist_url>\n')
                FF.write('    <img_src><![CDATA[' + ImgDefinitiva + ']]></img_src>\n')
                FF.write('    <tipo><![CDATA[hdfullCapitulos]]></tipo>\n')
                FF.write('    <historial><![CDATA[' + Categ +']]></historial>\n')
                FF.write('</channel>\n\n')
                
            
            FF.write('<prev_page_url text="CH- ATRAS"><![CDATA[/cosas/Series_AZ_HDFULL.xml]]></prev_page_url>\n</items>')
            FF.close()
            
            return Categ
            
    except Exception as er:
        Log(str(er), "En NavegarAZ HDFULL")
        return [1, er]
        
def Capitulos(self, Nam, URLL = "", THUMB = "", historial = "", temporada = ""):
    try:
        global opener
        global OTRO
        
        NN = Nam
        NN = CambiaTexto(NN)
        
        if "###" in URLL:
            idd = URLL.split("###")[1].split(";")[0]
            typee = URLL.split("###")[1].split(";")[1]
            URLL = URLL.split("###")[0]
        
        Categ = RutaTMP + NN.encode('utf8') + "_1.xml"
        
        
        url = 'https://hdfull.lv/a/episodes'
        post = "action=season&start=0&limit=0&show=%s&season=%s" % (idd, temporada)
        req = urllib2.Request(url)
        req.add_header('User-Agent',user_agent_default)
        req.add_header('Referer', URLL)
        Abrir = OP(req, data=post)
        data = jsontools.load(Abrir.read())
        Abrir.close()
        
        FF = open(Categ, 'w')
        
        for episode in data:

            language = episode['languages']
            tempo = episode['season']
            episodio = episode['episode']
            if "es" in episode['title']:
                titulo = str(episode['title']['es'].decode('utf8'))
            elif "en" in episode['title']:
                titulo = str(episode['title']['en'].decode('utf8'))
            else:
                titulo = ""
                
            titulo = CambiaTexto(titulo)
            
            if episodio == "1":
                FF.write('<?xml version="1.0" encoding="iso-8859-1"?>\n<items>\n<playlist_name><![CDATA[' + titulo + ']]></playlist_name>\n\n')
            
            FF.write("<channel>\n")
            FF.write("    <title><![CDATA[" + temporada + "x" + episodio + " " + titulo + "]]></title>\n")
            FF.write('    <description><![CDATA[]]></description>\n')
            FF.write('    <playlist_url><![CDATA[' + URLL + '/episodio-' + episodio + ']]></playlist_url>\n')
            FF.write('    <img_src><![CDATA[' + str(THUMB) + ']]></img_src>\n')
            FF.write('    <tipo><![CDATA[hdfullEnlaces]]></tipo>\n')
            FF.write('    <historial><![CDATA[' + Categ + ']]></historial>\n')
            FF.write('</channel>\n\n')
            
            
        FF.write('<prev_page_url text="CH- ATRAS"><![CDATA[' + historial + ']]></prev_page_url>\n</items>')
        FF.close()
        
        return Categ

            
    except Exception as er:
        Log(str(er), "En Capitulos HDFULL")
        return [1, er]
        
def Temporadas(self, Nam, URLL = "", THUMB = "", historial = ""):
    try:
        global opener
        global OTRO
        
        NN = Nam
        NN = CambiaTexto(NN)
        
        if "###" in URLL:
            idd = URLL.split("###")[1].split(";")[0]
            typee = URLL.split("###")[1].split(";")[1]
            URLL = URLL.split("###")[0]
        
        Categ = RutaTMP + NN + "1.xml"
        
        url = URLL
        data = agrupa_datos(url)
        
        buscaSinopsis = re.findall(r'itemprop="description">(.*?)<br', data)
        Sinop = CambiaTexto(buscaSinopsis[0])
        
        INDINI = data.find('Todas las temporadas')
        INDFIN = data.find('<div class="breakaway-wrapper-alt">')
        data = data[INDINI:INDFIN]
        
        Recopila = re.findall(r'href=\'(.*?)\'>(.*?)<', data)
            
        FF = open(Categ, 'w')
        FF.write('<?xml version="1.0" encoding="iso-8859-1"?>\n<items>\n<playlist_name><![CDATA[' + NN.encode('utf8') + ']]></playlist_name>\n\n')
        
        if Recopila == []:
            Mensaje = "Error","No hay mas resultados aqui."
            FF.close()
            return [1, Mensaje]
        else:
            for enlace,temporada in Recopila:
                ENLA = enlace
                if ENLA.find('temporada-0') != -1:
                    pass
                else:
                    ENLA += "###" + idd + ";1"
                    FF.write("<channel>\n")
                    FF.write("    <title><![CDATA[Temporada " + temporada + "]]></title>\n")
                    FF.write('    <description><![CDATA[<img src="' + THUMB + '">]]>' + Sinop + '</description>\n')
                    FF.write('    <playlist_url><![CDATA[' + ENLA + ']]></playlist_url>\n')
                    FF.write('    <img_src><![CDATA[' + THUMB + ']]></img_src>\n')
                    FF.write('    <tipo><![CDATA[hdfullCapitulos]]></tipo>\n')
                    FF.write('    <historial><![CDATA[' + Categ +']]></historial>\n')
                    FF.write('</channel>\n\n')
                
            
            FF.write('<prev_page_url text="CH- ATRAS"><![CDATA[' + historial + ']]></prev_page_url>\n</items>')
            FF.close()
            
            return Categ
            
    except Exception as er:
        Log(str(er), "En Temporadas HDFULL")
        return [1, er]
        
def Buscar(self, Nombre, Tipo):
    try:
        OPT = Tipo
        Categ = RutaTMP + Nombre + ".xml"
        Name = Nombre
        Name = Name.replace("/","")
        Name = Name.replace(":","")
        Name = Name.replace("á","a")
        Name = Name.replace("é","e")
        Name = Name.replace("í","i")
        Name = Name.replace("ó","o")
        Name = Name.replace("ú","u")
        Name = Name.replace("Á","A")
        Name = Name.replace("É","E")
        Name = Name.replace("Í","I")
        Name = Name.replace("Ó","O")
        Name = Name.replace("Ú","U")
        Name = Name.replace("&#039;","'")
        Name = Name.replace("&#39;","'")
        Name = Name.replace(" ", "+")
        
        url_origen = 'https://hdfull.lv/'
        req = urllib2.Request(url_origen)
        req.add_header('User-Agent', user_agent_default)
        Abrir = OP(req, timeout=20)
        data = Abrir.read()
        Abrir.close()
        
        GetName = re.findall(r'buscar.+name=\'(.*?)\'\s+value=', data)
        GetToken = re.findall(r'buscar.+value="(.*?)"', data)
        
        NameToken = GetName[0]
        Token = GetToken[0]
        
        if OPT == 0: # Pelis
            url = 'https://hdfull.lv/buscar'
            post = str(NameToken) + '=' + str(Token) + "&menu=search&query=" + Name
            req = urllib2.Request(url)
            req.add_header('User-Agent', user_agent_default)
            req.add_header('Referer', 'https://hdfull.lv/')
            Abrir = OP(req, data=post)
            data = Abrir.read()
            Abrir.close()
            
            INDINI = data.find('Resultados en pel')
            INDFIN = data.find('<div id="avatar_form" class="modal" style="display:none">')
            
            data = data[INDINI:INDFIN]
            
            Recopila = re.findall(r'href="(.*?)".+\s+.+src="(.*?)"\s.+title="(.*?)"\sst', data)
            IDS = re.findall(r'setFavorite\(\d+, (.*?), \d', data)
            
            Conteo = 0
            
            if Recopila == []:
                Mensaje = "Error","No hay mas resultados aqui."
                FF.close()
                return [1, Mensaje]
                
            FF = open(Categ, 'w')
            FF.write('<?xml version="1.0" encoding="iso-8859-1"?>\n<items>\n<playlist_name><![CDATA[Buscando ' + Nombre + ']]></playlist_name>\n\n')
            
            for enlace,imagen,titulo in Recopila:
                ID = IDS[Conteo]
                IMAG = imagen
                IMAG = IMAG.replace("130", "260")
                IMAG = IMAG.replace("190", "380")
                Conteo = Conteo + 1
                EN = enlace
                if '/serie' in EN or "/tags-tv" in EN:
                    EN += "###" + ID + ";1"
                else:
                    EN += "###" + ID + ";2"
                TI = titulo
                ImgDefinitiva = ObtenImagenes(self, IMAG)

                FF.write("<channel>\n")
                FF.write("    <title><![CDATA[" + TI.encode('utf8') + "]]></title>\n")
                FF.write('    <description><![CDATA[<img src="' + IMAG + '">]]></description>\n')
                FF.write('    <playlist_url><![CDATA[' + EN + ']]></playlist_url>\n')
                FF.write('    <img_src><![CDATA[' + ImgDefinitiva + ']]></img_src>\n')
                FF.write('    <tipo><![CDATA[hdfullEnlaces]]></tipo>\n')
                FF.write('    <historial><![CDATA[' + Categ + ']]></historial>\n')
                FF.write('</channel>\n\n')

            FF.write('<prev_page_url text="CH- ATRAS"><![CDATA[/cosas/hdfull.xml]]></prev_page_url>\n</items>')
            FF.close()
                
            return Categ
            
        elif OPT == 1: # Series
            url = 'https://hdfull.lv/buscar'
            post = str(NameToken) + '=' + str(Token) + "&menu=search&query=" + Name
            req = urllib2.Request(url)
            req.add_header('User-Agent', user_agent_default)
            req.add_header('Referer', 'https://hdfull.lv/')
            Abrir = OP(req, data=post)
            data = Abrir.read()
            Abrir.close()
            
            INDINI = data.find('Resultados en series para')
            if data.find('Resultados en pel') != -1:
                INDFIN = data.find('Resultados en pel')
            else:
                INDFIN = data.find('<div id="avatar_form" class="modal" style="display:none">')
            
            data = data[INDINI:INDFIN]
            
            Recopila = re.findall(r'"link" href="(.*?)" title="(.*?)">', data)
            Imagenes = re.findall(r'src="(.*?)"\salt=" ', data)
            IDS = re.findall(r'setFavorite\(\d+, (.*?), \d', data)
            
            Conteo = 0
            
            if Recopila == []:
                Mensaje = "Error","No hay mas resultados aqui."
                FF.close()
                return [1, Mensaje]
                
            FF = open(Categ, 'w')
            FF.write('<?xml version="1.0" encoding="iso-8859-1"?>\n<items>\n<playlist_name><![CDATA[Buscando ' + Nombre + ']]></playlist_name>\n\n')
            
            for enlace,titulo in Recopila:
                ID = IDS[Conteo]
                IMAG = Imagenes[Conteo]
                IMAG = IMAG.replace("130", "260")
                IMAG = IMAG.replace("190", "380")
                Conteo = Conteo + 1
                EN = enlace
                if '/serie' in EN or "/tags-tv" in EN:
                    EN += "###" + ID + ";1"
                else:
                    EN += "###" + ID + ";2"
                TI = titulo
                ImgDefinitiva = ObtenImagenes(self, IMAG)

                FF.write("<channel>\n")
                FF.write("    <title><![CDATA[" + TI.encode('utf8') + "]]></title>\n")
                FF.write('    <description><![CDATA[<img src="' + IMAG + '">]]></description>\n')
                FF.write('    <playlist_url><![CDATA[' + EN + ']]></playlist_url>\n')
                FF.write('    <img_src><![CDATA[' + ImgDefinitiva + ']]></img_src>\n')
                FF.write('    <tipo><![CDATA[hdfullCapitulos]]></tipo>\n')
                FF.write('    <historial><![CDATA[' + Categ + ']]></historial>\n')
                FF.write('</channel>\n\n')

            FF.write('<prev_page_url text="CH- ATRAS"><![CDATA[/cosas/hdfull.xml]]></prev_page_url>\n</items>')
            FF.close()
                
            return Categ
            
        else:
            pass
    except Exception as er:
        print "Error HDFULL en Busca: " + str(er)
        print "Error HDFULL en Busca: " + str(er)
        return [1, er]
