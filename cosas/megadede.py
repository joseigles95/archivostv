# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/archivostv/cosas/megadede.py
# coding: utf-8

import re, os, time, datetime, traceback, urllib, cookielib
import urllib2
import httplib, mimetypes
import shutil
import sys
import json
import hashlib
import Teclado
from enigma import eTimer

RUTAPLUGIN = "/usr/lib/enigma2/python/Plugins/Extensions/archivostv/"
RUTACOOKIE = "/usr/lib/enigma2/python/Plugins/Extensions/archivostv/cookies/cookies.dat"
RutaTMP = "/tmp/archivostv/"
user_agent_default = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"

ARPORDEDE = RUTAPLUGIN+"/cosas/megadede.py"
ARPORDEDEO = RUTAPLUGIN+"/cosas/megadede.pyo"

TKN = ""
USR = ""
PSW = ""
Mediaitem = ""
Sesion = ""

OTRO = 0

cj = cookielib.MozillaCookieJar()

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
OP = opener.open

LogeadoDD = False

cookiepath = RutaTMP

def load_cookies():
    if os.path.isfile(RUTACOOKIE):
        
        try:
            print "Cargando cookies"
            cj.load(RUTACOOKIE, ignore_discard=True)
        except:
            print "No cargamos cookies, error"
            pass
    else:
        print RUTACOOKIE
        print "No existe el fichero de cookies megadede"
        
def save_cookies():
    cj.save(RUTACOOKIE, ignore_discard=True)
    print "Guardando las cookies"

def Version():
    V = 100
    return V
    
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
    NN = NN.replace("&amp;","y")
    NN = NN.replace("&ntilde;","n")
    NN = NN.replace("&quot;","")
    NN = NN.replace("&aacute;","a")
    NN = NN.replace("&eacute;","e")
    NN = NN.replace("&iacute;","i")
    NN = NN.replace("&oacute;","o")
    NN = NN.replace("&uacute;","u")
    NN = NN.replace("&laquo;","")
    NN = NN.replace("&raquo;","")
    NN = NN.replace("</p>","")
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

def CompruebaLogin(self):
    load_cookies()
    url = 'https://www.megadede.com/login?popup=1'
    req = urllib2.Request(url)
    req.add_header('User-Agent', user_agent_default)
    Abrir = OP(req, timeout=20)
    data = Abrir.read()
    Abrir.close()
    
    if data.find('Escribe los números de la imagen') == -1:
        #No lo encuentra, asi que estamos logeados.
        return False
    else:
        print data
        #Si lo encuentra, asi que estamos deslogeados.
        return True

def Recap(self, usuario, contra, deslogeo, item):
    try:
        global USR
        global PSW
        global TKN
        global Mediaitem
        global Sesion
        
        load_cookies()
        
        
        
        Sesion = self.session
        
        Mediaitem = [1, 2, 3]
        
        cookiepath = RutaTMP
        
        if item[1].find('Navegar en Estrenos') != -1:
            Mediaitem[0] = 'https://www.megadede.com/pelis/index/' + item[10] + '?quality=2&year=2017%3B2020'
        
        if item[1].find('Navegar en Peliculas') != -1:
            Mediaitem[0] = 'https://www.megadede.com/pelis/index/' + item[10] + '?quality=2&year=1990%3B2020'
        
        if item[1].find('Navegar en Series') != -1:
            Mediaitem[0] = 'https://www.megadede.com/series/index/' + item[10] + '?quality=2&year=1990%3B2020'

        if item[1].find('Navegar en Listas') != -1:
            Mediaitem[0] = 'https://www.megadede.com/listas/index/' + item[10] + '?quality=2&year=1990%3B2020'
        
        if item[1].find('Navegar en La Unidad') != -1:
            Mediaitem[0] = 'https://www.megadede.com/serie/la-unidad' + item[10] + '?quality=2&year=1990%3B2020'            

            
        
        if not os.path.isfile(cookiepath):
            cookiepath = os.path.join(cookiepath,'cookies.lwp')
            
        Mediaitem[1] = item[1]
        Mediaitem[2] = item[10]
            
        try:
            os.remove(cookiepath)
        except:
            pass
        
        LOGIN = usuario
        PASSWORD = contra
        
        USR = LOGIN
        PSW = PASSWORD
        
        if deslogeo == 0:
            LogeadoDD = False
        elif deslogeo == 1:
            LogeadoDD = True
        
        if LogeadoDD == False:
        
            url_origen = 'https://www.megadede.com/login?popup=1'
            req = urllib2.Request(url_origen)
            req.add_header('User-Agent', user_agent_default)
            Abrir = OP(req, timeout=20)
            data = Abrir.read()
            Abrir.close()
            
            GetToken = re.findall(r'_token" content="(.*?)"', data)
            GetVersion = re.findall(r'_version" content="(.*?)"', data)
            GetCaptcha = re.findall(r'src="(.+?)" alt="captcha">', data)
            
            Token = GetToken[0]
            TKN = Token
            Version = GetVersion[0]
            Captcha = GetCaptcha[0]
            
            if re.search('Escribe los números de la imagen', data):
                url_origen = Captcha
                req = urllib2.Request(url_origen)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0')
                Abrir = OP(req, timeout=20)
                imagen_data = Abrir.read()
                Abrir.close()

                ficheropng = RutaTMP + "captcha_plusdede.png"
                outfile=open(ficheropng,'wb')
                outfile.write(imagen_data)
                outfile.close()

                #self.pausetimer = eTimer()
                #self.pausetimer.start(5000, True)

                Testt = self.session.openWithCallback(Recap2, Teclado.TecladoVirtualPlusdede, title="Escribe los Numeros: ", text="", imagen=ficheropng)
                return

            else:
                print 'No encuentra lo del captcha.'
        else:
            pass
        
    except Exception as er:
        print "Error: "+ str(er) + " En Recap"
        print "Error: "+ str(er) + " En Recap"
        print "Error: "+ str(er) + " En Recap"
        return [1, er]
        
def Recap2(respuesta):
    try:
        global LogeadoDD
        global USR
        global PSW
        global TKN
        global Mediaitem
        global Sesion
        global OTRO
        
        url = 'https://www.megadede.com/login'
        post = '_token='+ TKN + '&email=' + USR + '&password=' + PSW + '&captcha=' + respuesta + '&popup=1'
        
        req = urllib2.Request(url)
        req.add_header('User-Agent', user_agent_default)
        #req.add_header('Accept', '*/*')
        req.add_header('Referer', 'https://www.megadede.com/')
        req.add_header('X-Requested-With', 'XMLHttpRequest')
        req.add_header('X-CSRF-TOKEN', TKN)
        Abrir = OP(req, data=post)
        data = Abrir.read()
        Abrir.close()
        
        save_cookies()

        
        #self.pausetimer = eTimer()
        #self.pausetimer.start(10000, True)
        
        if "redirect" in data:
            print "Login Correcto"
            LogeadoDD = True
            
            if Mediaitem[1].find('Navegar en Estrenos') != -1:
                OTRO = 1
                Testt = NavegarEstrenos(Sesion, Mediaitem[1], Mediaitem[2])
                
            if Mediaitem[1].find('Navegar en Peliculas') != -1:
                OTRO = 1
                Testt = NavegarPeliculas(Sesion, Mediaitem[1], Mediaitem[2])
                
            if Mediaitem[1].find('Navegar en Series') != -1:
                OTRO = 1
                Testt = NavegarSeries(Sesion, Mediaitem[1], Mediaitem[2])
            
            if Mediaitem[1].find('Navegar en Listas') != -1:
                OTRO = 1
                Testt = NavegarListas(Sesion, Mediaitem[1], Mediaitem[2])
                
            if Mediaitem[1].find('La Unidad') != -1:
                OTRO = 1
                Testt = launidad(Sesion, Mediaitem[1], Mediaitem[2])                

                
            return True
        else:
            print "Login no correcto"
            LogeadoDD = False
            return False
    except Exception as err:
        try:
            print err
            print err
            print err
            
            global LogeadoDD
            global USR
            global PSW
            global TKN
            global Mediaitem
            global Sesion
            global OTRO
            
            url = 'https://www.megadede.com/login'
            post = '_token='+ TKN + '&email=' + USR + '&password=' + PSW + '&captcha=' + respuesta
            
            req = urllib2.Request(url)
            req.add_header('User-Agent', user_agent_default)
            req.add_header('Referer', 'https://www.megadede.com/')
            req.add_header('X-Requested-With', 'XMLHttpRequest')
            req.add_header('X-CSRF-TOKEN', TKN)
            Abrir = OP(req, data=post, timeout=20)
            data = Abrir.read()
            Abrir.close()
            
            if "redirect" in data:
                print "Login Correcto"
                LogeadoDD = True
                
                if Mediaitem[1].find('Navegar en Estrenos') != -1:
                    OTRO = 1
                    Testt = NavegarEstrenos(Sesion, Mediaitem[1], Mediaitem[2])
                    
                if Mediaitem[1].find('Navegar en Peliculas') != -1:
                    OTRO = 1
                    Testt = NavegarPeliculas(Sesion, Mediaitem[1], Mediaitem[2])
                    
                if Mediaitem[1].find('Navegar en Series') != -1:
                    OTRO = 1
                    Testt = NavegarSeries(Sesion, Mediaitem[1], Mediaitem[2])

                if Mediaitem[1].find('Navegar en Listas') != -1:
                    OTRO = 1
                    Testt = Navegarlistas(Sesion, Mediaitem[1], Mediaitem[2])
                    
                if Mediaitem[1].find('La Unidad') != -1:
                    OTRO = 1
                    Testt = launidad(Sesion, Mediaitem[1], Mediaitem[2])                   

                
                
                #Testt = Sesion.open(inavi.Principal, Mediaitem.URL, Mediaitem.name)
                return True
            else:
                print "Login no correcto"
                LogeadoDD = False
                return False

        except Exception as err:
            print "Error: "+ str(err) + " En Recap2"
            print "Error: "+ str(err) + " En Recap2"
            print "Error: "+ str(err) + " En Recap2"

def LoginPordede(self, usuario, contra):
    cookiepath = RutaTMP
        
def Enlaces1(self, enlace):
    ENN = enlace
    url = ENN
    req = urllib2.Request(url)
    req.add_header('User-Agent', user_agent_default)
    req.add_header('Referer', ENN)
    Abrir = OP(req)
    data = Abrir.read()
    Abrir.close()
    
    BuscaEN = re.findall(r'visit-buttons">\n.+href="(.*?)" tar', data)
    
    if BuscaEN != []:
        BuscaEN = "https://www.megadede.com" + BuscaEN[0]
        
    url = BuscaEN
    req = urllib2.Request(url)
    req.add_header('User-Agent', user_agent_default)
    #req.add_header('Referer', ENN)
    Abrir = OP(req)
    data = Abrir.read()
    Abrir.close()
    
    Devuelve = Abrir.geturl()
    
    #print "Este es el geturl: " + Devuelve
    
    if Abrir.geturl().find("gamovideo") != -1:
        CC = re.findall(r'(\.html)', Abrir.geturl())
        if CC == []:
            CogeENlace = re.findall(r'\.com\/(.*)', Abrir.geturl())
            CogeENlace = CogeENlace[0]
            Devuelve = "http://gamovideo.com/embed-" + CogeENlace + "-640x360.html"
        else:
            TT = re.findall(r'embed-(.*?)-', Abrir.geturl())
            TT = TT[0]
            CogeENlace = TT
            Devuelve = "http://gamovideo.com/embed-" + CogeENlace + "-640x360.html"
    
    return Devuelve
        
def Enlaces(self, Nam, URLL, THUMB, historial):
    try:
        NN = Nam
        NN = CambiaTexto(NN)
        ENN = URLL
        IMG = THUMB

        Categ = RutaTMP + NN + ".xml"
        
        url = ENN
        req = urllib2.Request(url)
        req.add_header('User-Agent',user_agent_default)
        req.add_header('Referer','https://www.megadede.com/pelis')
        Abrir = OP(req)
        data = Abrir.read()
        Abrir.close()
        
        if ENN.find('peli') != -1:
            SINOP = re.findall(r'themoviedb\.png\">.+ref=\"(.*?)"', data)
            SINOP = SacaSinopsis("Pelicula", SINOP[0])
            SINOP = CambiaTexto(SINOP)
        else:
            SINOP = ""
        
        Buscabtnenlaces = ""
        
        if IMG.find('peli') != -1:
            Buscabtnenlaces = re.findall(r'peli-link\s+">\n\s+.+data-href="(.*?)">ver', data)
            if Buscabtnenlaces != []:
                BotonEnlaces = "https://www.megadede.com" + Buscabtnenlaces[0]
            else:
                print "NO encuentra nada? :SSSS"
            
        else:
            if IMG.find('serie') != -1:
                BotonEnlaces = url
        
        req = urllib2.Request(BotonEnlaces)
        req.add_header('User-Agent', user_agent_default)
        req.add_header('Referer', url)
        Abrir = OP(req)
        data = Abrir.read()
        Abrir.close()
        
        INDINI = data.find('<h4>De tus hosts favoritos</h4>')
        INDFIN = data.find('<h4>De otros hosts</h4>')
        
        data = data[INDINI:INDFIN]

        patron = '<div class="right(.*?)<div class="audioquality">'
        resultados = re.compile(patron, re.DOTALL).findall(data)

        FF = open(Categ, 'w')
        FF.write('<?xml version="1.0" encoding="iso-8859-1"?>\n<items>\n<playlist_name><![CDATA[' + NN + ']]></playlist_name>\n\n')
        Conteo = 0
        
        for match in resultados:
            idioma = re.findall(r'<img src="https://cdn\d+.megadede.com/images/flags/(.*?)\.png"', match)
            calidad = re.findall(r'fa-video-camera"></span>\n\s+(.*?)\n\s', match)
            imag = re.findall(r'<div class="host">\n.+c="(.*?)">', match)
            Enlace = re.findall(r'<a  data.+href="(.*?)"\sclass="apo', match)
            idioma = idioma[0]
            calidad = calidad[0]
            imag = imag[0]
            Enlace = Enlace[0]
            Procesador = ""
            
            if idioma.find("") != -1:
                Conteo = Conteo + 1
            
                FF.write("<channel>\n")
                FF.write("    <title><![CDATA[Ver en " + idioma.encode('utf8') + " " + calidad + "]]></title>\n")
                FF.write('    <description><![CDATA[<img src="' + imag.encode("utf8") + '">]]>' + SINOP + '</description>\n')
                FF.write('    <playlist_url><![CDATA[' + Enlace + ']]></playlist_url>\n')
            
                if imag.find("vidoza") != -1:
                    Procesador = "http://ps3plusteam.ddns.net/teamps3plus/pro/vidoza.txt"
                    FF.write('    <stream_url><![CDATA[' + Procesador + ']]></stream_url>\n')
                    FF.write('    <img_src><![CDATA[http://ps3plusteam.ddns.net/ps3plus/images/letras/vidoza.png]]></img_src>\n')
                elif imag.find("nowvideo") != -1:
                    Procesador = "http://ps3plusteam.ddns.net/teamps3plus/pro/nowvideo.txt"
                    FF.write('    <stream_url><![CDATA[' + Procesador + ']]></stream_url>\n')
                    FF.write('    <img_src><![CDATA[http://ps3plusteam.ddns.net/ps3plus/images/letras/nowvideo.png]]></img_src>\n')
                elif imag.find("gamo") != -1:
                    Procesador = "http://ps3plusteam.ddns.net/teamps3plus/props3/gamo.txt"
                    FF.write('    <stream_url><![CDATA[' + Procesador + ']]></stream_url>\n')
                    FF.write('    <img_src><![CDATA[http://ps3plusteam.ddns.net/ps3plus/images/letras/gamovideo.png]]></img_src>\n')
                elif imag.find("youtube") != -1:
                    Procesador = "http://ps3plusteam.ddns.net/teamps3plus/pro/youtube"
                    FF.write('    <stream_url><![CDATA[' + Procesador + ']]></stream_url>\n')
                    FF.write('    <img_src><![CDATA[http://ps3plusteam.ddns.net/ps3plus/images/letras/youtube.png]]></img_src>\n')
                else:
                    pass
                    
                FF.write('    <tipo><![CDATA[megadedeLinks]]></tipo>\n')
                FF.write('</channel>\n\n')
                    
            else:
                pass

        FF.write('<prev_page_url text="CH- ATRAS"><![CDATA[' + historial + ']]></prev_page_url>\n</items>')
        FF.close()
        
        if Conteo == 0:
            return None
            

        return Categ
        
    except Exception as er:
        print "Error: "+ str(er) + " En Enlaces MEGADEDE"
        print "Error: "+ str(er) + " En Enlaces MEGADEDE"
        print "Error: "+ str(er) + " En Enlaces MEGADEDE"
        return [1, er]
    
def Capitulos(self, Nam, URLL, THUMB, historial):
    try:
        ArchivoLog = RutaTMP + "Log.txt"
        NN = Nam
        NN = CambiaTexto(NN)
        ENN = URLL
        IMG = THUMB


        Categ = RutaTMP + NN + "1.xml"
        
        url = ENN
        req = urllib2.Request(url)
        req.add_header('User-Agent',user_agent_default)
        req.add_header('Referer','https://www.megadede.com/series')
        Abrir = OP(req)
        data = Abrir.read()
        Abrir.close()
        
        SINOP = re.findall(r'thetvdb\.png\">.+ref=\"(.*?)"', data)
        SINOP = SacaSinopsis("Serie", SINOP[0])
        SINOP = CambiaTexto(SINOP)
        
        FF = open(Categ, 'w')
        FF.write('<?xml version="1.0" encoding="iso-8859-1"?>\n<items>\n<playlist_name><![CDATA[' + NN + ']]></playlist_name>\n\n')
        
        BuscaTemporadas = re.findall(r'-header" > Temporada (.*?) <div class="check-season', data)
        
        for cuantas in BuscaTemporadas:
            if cuantas == len(BuscaTemporadas):
                INDINI = data.find('season-header" > Temporada ' + cuantas)
                INDFIN = data.find('class="comments-container')
                source = data[INDINI:INDFIN]
                
                BuscaTodo = re.findall(r'episode model.*href="(.*?)">\s+.+\s+.+class="num">(\d+)</span>\n\s+(.*?)\n', source)
                
                for enlace,episodio,nombre in BuscaTodo:
                    FF.write("<channel>\n")
                    FF.write("    <title><![CDATA[" + cuantas + "x" + episodio +"- " + nombre + "]]></title>\n")
                    FF.write('    <description><![CDATA[' + str(IMG[1]) + ']]>' + SINOP + '</description>\n')
                    FF.write('    <playlist_url><![CDATA[https://www.megadede.com' + enlace + ']]></playlist_url>\n')
                    FF.write('    <img_src><![CDATA[' + str(IMG[0]) + ']]></img_src>\n')
                    FF.write('    <tipo><![CDATA[megadedeEnlaces]]></tipo>\n')
                    FF.write('    <historial><![CDATA[' + Categ + ']]></historial>\n')
                    FF.write('</channel>\n\n')
                
            else:
                tot = int(cuantas)
                tot = tot+1
                INDINI = data.find('season-header" > Temporada ' + cuantas)
                INDFIN = data.find('season-header" > Temporada ' + str(tot))
                source = data[INDINI:INDFIN]
                
                BuscaTodo = re.findall(r'episode model.*href="(.*?)">\s+.+\s+.+class="num">(\d+)</span>\n\s+(.*?)\n', source)
                
                for enlace,episodio,nombre in BuscaTodo:
                    FF.write("<channel>\n")
                    FF.write("    <title><![CDATA[" + cuantas + "x" + episodio +"- " + nombre + "]]></title>\n")
                    FF.write('    <description><![CDATA[' + str(IMG[1]) + ']]>' + SINOP + '</description>\n')
                    FF.write('    <playlist_url><![CDATA[https://www.megadede.com' + enlace + ']]></playlist_url>\n')
                    FF.write('    <img_src><![CDATA[' + str(IMG[0]) + ']]></img_src>\n')
                    FF.write('    <tipo><![CDATA[megadedeEnlaces]]></tipo>\n')
                    FF.write('    <historial><![CDATA[' + Categ + ']]></historial>\n')
                    FF.write('</channel>\n\n')
                    
        FF.write('<prev_page_url text="CH- ATRAS"><![CDATA[' + historial + ']]></prev_page_url>\n</items>')
        FF.close()
        #ArLog.close()
        
        return Categ
        
    except Exception as er:
        print "Error: "+ str(er) + " En Capitulos"
        print "Error: "+ str(er) + " En Capitulos"
        print "Error: "+ str(er) + " En Capitulos"
        return [1, er]


def NavegarListas(self, Nam, Pagina):
    try:
        global opener
        global OTRO
        
        NN = Nam
        NN = CambiaTexto(NN)
        PAG = Pagina
        PG = PAG
        
        Categ = RutaTMP + NN + str(PG) + ".xml"
        
        url = 'https://www.megadede.com/listas/index/' + PAG + '?quality=2&year=1990%3B2020'
        PAG = int(PAG)
        
        req = urllib2.Request(url)
        req.add_header('User-Agent',user_agent_default)
        req.add_header('Referer','https://www.megadede.com/listas')
        Abrir = OP(req)
        data = Abrir.read()
        Abrir.close()
        
        Recopila = re.findall(r'href="(.*?)".+title="(.*?)".+\n.+\n.+\n.+src="(.*?)\?v', data)
        
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
            for enlace,titulo,imagen in Recopila:
                Conteo = Conteo + 1
                ENLA = enlace
                NN = titulo
                NN = CambiaTexto(NN)
                IMAG = imagen
                
                ImgDefinitiva = ObtenImagenes(self, IMAG)
                
                FF.write("<channel>\n")
                FF.write("    <title><![CDATA[" + NN.encode('utf8') + "]]></title>\n")
                FF.write('    <description><![CDATA[<img src="' + IMAG + '">]]></description>\n')
                FF.write('    <playlist_url><![CDATA[' + ENLA + ']]></playlist_url>\n')
                FF.write('    <img_src><![CDATA[' + ImgDefinitiva + ']]></img_src>\n')
                FF.write('    <tipo><![CDATA[megadedeEnlaces]]></tipo>\n')
                FF.write('    <historial><![CDATA[' + Categ + ']]></historial>\n')
                FF.write('</channel>\n\n')
                
            
            if Conteo < 58:
                pass
            else:
                FF.write("<channel>\n")
                FF.write("    <title><![CDATA[Pagina Siguiente]]></title>\n")
                FF.write('    <description><![CDATA[<img src="http://ps3plusteam.ddns.net/ps3plus/images/letras/siguiente.png">]]>Avanza a la pagina siguiente para ver mas peliculas!</description>\n')
                FF.write('    <img_src><![CDATA[http://ps3plusteam.ddns.net/ps3plus/images/letras/siguiente.png]]></img_src>\n')
                FF.write('    <ts_stream><![CDATA[' + str(i) + ']]></ts_stream>\n')
                FF.write('    <tipo><![CDATA[megadedeListas]]></tipo>\n')
                FF.write('</channel>\n\n')
                
            if i == 1:
                FF.write('<prev_page_url text="CH- ATRAS"><![CDATA[/cosas/megadede.xml]]></prev_page_url>\n</items>')
            if i == 2:
                FF.write('<prev_page_url text="CH- ATRAS"><![CDATA[/tmp/archivostv/Navegar en Peliculas0.xml]]></prev_page_url>\n</items>')
            if i > 2:
                i = i - 1
                FF.write('<prev_page_url text="CH- ATRAS"><![CDATA[/tmp/archivostv/Pagina Siguiente' + str(i - 1) + '.xml]]></prev_page_url>\n</items>')
                
            FF.close()
            
            return Categ
                
    except Exception as er:
        print "Error: "+ str(er) + " En NavegarListas"
        print "Error: "+ str(er) + " En NavegarListas"
        print "Error: "+ str(er) + " En NavegarListas"
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
        
        url = 'https://www.megadede.com/pelis/index/' + PAG + '?quality=2&year=2020%3B2020&first_filters=1'
        PAG = int(PAG)
        
        req = urllib2.Request(url)
        req.add_header('User-Agent',user_agent_default)
        req.add_header('Referer','https://www.megadede.com/pelis')
        Abrir = OP(req)
        data = Abrir.read()
        Abrir.close()
        
        Recopila = re.findall(r'href="(.*?)".+title="(.*?)".+\n.+\n.+\n.+src="(.*?)\?v', data)
        
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
            for enlace,titulo,imagen in Recopila:
                Conteo = Conteo + 1
                ENLA = enlace
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
                FF.write('    <tipo><![CDATA[megadedeEnlaces]]></tipo>\n')
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
                FF.write('    <tipo><![CDATA[megadedeEstrenos]]></tipo>\n')
                FF.write('</channel>\n\n')
                
            
            if i == 1:
                FF.write('<prev_page_url text="CH- ATRAS"><![CDATA[/cosas/megadede.xml]]></prev_page_url>\n</items>')
            if i == 2:
                FF.write('<prev_page_url text="CH- ATRAS"><![CDATA[/tmp/archivostv/Navegar en Estrenos0.xml]]></prev_page_url>\n</items>')
            if i > 2:
                i = i - 1
                FF.write('<prev_page_url text="CH- ATRAS"><![CDATA[/tmp/archivostv/Pagina Siguiente' + str(i - 1) + '.xml]]></prev_page_url>\n</items>')
            
            
            FF.close()
            
            return Categ
            
    except Exception as er:
        print "Error: "+ str(er) + " En NavegarEstrenos"
        print "Error: "+ str(er) + " En NavegarEstrenos"
        print "Error: "+ str(er) + " En NavegarEstrenos"
        return [1, er]
    
def NavegarPeliculas(self, Nam, Pagina):
    try:
        global opener
        global OTRO
        
        NN = Nam
        NN = CambiaTexto(NN)
        PAG = Pagina
        PG = PAG
        
        Categ = RutaTMP + NN + str(PG) + ".xml"
        
        url = 'https://www.megadede.com/pelis/index/' + PAG + '?quality=2&year=1990%3B2020'
        PAG = int(PAG)
        
        req = urllib2.Request(url)
        req.add_header('User-Agent',user_agent_default)
        req.add_header('Referer','https://www.megadede.com/pelis')
        Abrir = OP(req)
        data = Abrir.read()
        Abrir.close()
        
        Recopila = re.findall(r'href="(.*?)".+title="(.*?)".+\n.+\n.+\n.+src="(.*?)\?v', data)
        
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
            for enlace,titulo,imagen in Recopila:
                Conteo = Conteo + 1
                ENLA = enlace
                NN = titulo
                NN = CambiaTexto(NN)
                IMAG = imagen
                
                ImgDefinitiva = ObtenImagenes(self, IMAG)
                
                FF.write("<channel>\n")
                FF.write("    <title><![CDATA[" + NN.encode('utf8') + "]]></title>\n")
                FF.write('    <description><![CDATA[<img src="' + IMAG + '">]]></description>\n')
                FF.write('    <playlist_url><![CDATA[' + ENLA + ']]></playlist_url>\n')
                FF.write('    <img_src><![CDATA[' + ImgDefinitiva + ']]></img_src>\n')
                FF.write('    <tipo><![CDATA[megadedeEnlaces]]></tipo>\n')
                FF.write('    <historial><![CDATA[' + Categ + ']]></historial>\n')
                FF.write('</channel>\n\n')
                
            
            if Conteo < 58:
                pass
            else:
                FF.write("<channel>\n")
                FF.write("    <title><![CDATA[Pagina Siguiente]]></title>\n")
                FF.write('    <description><![CDATA[<img src="http://ps3plusteam.ddns.net/ps3plus/images/letras/siguiente.png">]]>Avanza a la pagina siguiente para ver mas peliculas!</description>\n')
                FF.write('    <img_src><![CDATA[http://ps3plusteam.ddns.net/ps3plus/images/letras/siguiente.png]]></img_src>\n')
                FF.write('    <ts_stream><![CDATA[' + str(i) + ']]></ts_stream>\n')
                FF.write('    <tipo><![CDATA[megadedePelis]]></tipo>\n')
                FF.write('</channel>\n\n')
                
            if i == 1:
                FF.write('<prev_page_url text="CH- ATRAS"><![CDATA[/cosas/megadede.xml]]></prev_page_url>\n</items>')
            if i == 2:
                FF.write('<prev_page_url text="CH- ATRAS"><![CDATA[/tmp/archivostv/Navegar en Peliculas0.xml]]></prev_page_url>\n</items>')
            if i > 2:
                i = i - 1
                FF.write('<prev_page_url text="CH- ATRAS"><![CDATA[/tmp/archivostv/Pagina Siguiente' + str(i - 1) + '.xml]]></prev_page_url>\n</items>')
                
            FF.close()
            
            return Categ
                
    except Exception as er:
        print "Error: "+ str(er) + " En NavegarPeliculas"
        print "Error: "+ str(er) + " En NavegarPeliculas"
        print "Error: "+ str(er) + " En NavegarPeliculas"
        return [1, er]
        
def NavegarSeries(self, Nam, Pagina):
    try:
        global OTRO
        
        NN = Nam
        NN = CambiaTexto(NN)
        PAG = Pagina
        PG = PAG
        Categ = RutaTMP + NN + str(PG) + ".xml"
        
        url='https://www.megadede.com/series/index/' + PAG + '?quality=2&year=1990%3B2020'
        PAG = int(PAG)
        
        req = urllib2.Request(url)
        req.add_header('User-Agent',user_agent_default)
        req.add_header('Referer','https://www.megadede.com/series')
        Abrir = OP(req)
        data = Abrir.read()
        Abrir.close()
        
        Recopila = re.findall(r'href="(.*?)"\s.*title=".+\d\s+(.*?)"\s.+\n.+\n.+\n.+src="(.*?)"\s', data)
        
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
            for enlace,titulo,imagen in Recopila:
                Conteo = Conteo + 1
                ENLA = enlace
                NN = titulo
                NN = CambiaTexto(NN)
                IMAG = imagen
                ImgDefinitiva = ObtenImagenes(self, IMAG)

                if ImgDefinitiva == None:
                    ImgDefinitiva = ObtenImagenes(self, 'http://www.index-dvd.com/covers/600/elcuriosocasodebenjamin-600a.jpg')
                
                FF.write("<channel>\n")
                FF.write("    <title><![CDATA[" + NN.encode('utf8') + "]]></title>\n")
                FF.write('    <description><![CDATA[<img src="' + IMAG + '">]]></description>\n')
                FF.write('    <playlist_url><![CDATA[' + ENLA + ']]></playlist_url>\n')
                FF.write('    <img_src><![CDATA[' + ImgDefinitiva + ']]></img_src>\n')
                FF.write('    <tipo><![CDATA[megadedeCapitulos]]></tipo>\n')
                FF.write('    <historial><![CDATA[' + Categ + ']]></historial>\n')
                FF.write('</channel>\n\n')
                
                
            if Conteo < 58:
                pass
            else:
                FF.write("<channel>\n")
                FF.write("    <title><![CDATA[Pagina Siguiente]]></title>\n")
                FF.write('    <description><![CDATA[<img src="http://ps3plusteam.ddns.net/ps3plus/images/letras/siguiente.png">]]>Avanza a la pagina siguiente para ver mas Series!</description>\n')
                FF.write('    <img_src><![CDATA[http://ps3plusteam.ddns.net/ps3plus/images/letras/siguiente.png]]></img_src>\n')
                FF.write('    <ts_stream><![CDATA[' + str(i) + ']]></ts_stream>\n')
                FF.write('    <tipo><![CDATA[megadedeSeries]]></tipo>\n')
                FF.write('</channel>\n\n')
                
            if i == 1:
                FF.write('<prev_page_url text="CH- ATRAS"><![CDATA[/cosas/megadede.xml]]></prev_page_url>\n</items>')
            if i == 2:
                FF.write('<prev_page_url text="CH- ATRAS"><![CDATA[/tmp/archivostv/Navegar en Series0.xml]]></prev_page_url>\n</items>')
            if i > 2:
                i = i - 1
                FF.write('<prev_page_url text="CH- ATRAS"><![CDATA[/tmp/archivostv/Pagina Siguiente' + str(i - 1) + '.xml]]></prev_page_url>\n</items>')
            
            FF.close()
            return Categ
            
    except Exception as er:
        print "Error: "+ str(er) + " En NavegarSeries"
        print "Error: "+ str(er) + " En NavegarSeries"
        print "Error: "+ str(er) + " En NavegarSeries"
        return [1, er]
        
def launidad(self, Nam, URLL, THUMB, historial):
    try:
        global OTRO
        
        NN = Nam
        NN = CambiaTexto(NN)
        PAG = Pagina
        PG = PAG
        Categ = RutaTMP + NN + str(PG) + ".xml"
        
        url='https://www.megadede.com/serie/call-me-bruna' + PAG + '?quality=2&year=1990%3B2020'
        PAG = int(PAG)
        
        req = urllib2.Request(url)
        req.add_header('User-Agent',user_agent_default)
        req.add_header('Referer','https://www.megadede.com/serie/call-me-bruna')
        Abrir = OP(req)
        data = Abrir.read()
        Abrir.close()
        
        Recopila = re.findall(r'href="(.*?)"\s.*title=".+\d\s+(.*?)"\s.+\n.+\n.+\n.+src="(.*?)"\s', data)
        
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
            for enlace,titulo,imagen in Recopila:
                Conteo = Conteo + 1
                ENLA = enlace
                NN = titulo
                NN = CambiaTexto(NN)
                IMAG = imagen
                ImgDefinitiva = ObtenImagenes(self, IMAG)

                if ImgDefinitiva == None:
                    ImgDefinitiva = ObtenImagenes(self, 'http://www.index-dvd.com/covers/600/elcuriosocasodebenjamin-600a.jpg')
                
                FF.write("<channel>\n")
                FF.write("    <title><![CDATA[" + NN.encode('utf8') + "]]></title>\n")
                FF.write('    <description><![CDATA[<img src="' + IMAG + '">]]></description>\n')
                FF.write('    <playlist_url><![CDATA[' + ENLA + ']]></playlist_url>\n')
                FF.write('    <img_src><![CDATA[' + ImgDefinitiva + ']]></img_src>\n')
                FF.write('    <tipo><![CDATA[megadedeCapitulos]]></tipo>\n')
                FF.write('    <historial><![CDATA[' + Categ + ']]></historial>\n')
                FF.write('</channel>\n\n')
                
                
            if Conteo < 58:
                pass
            else:
                FF.write("<channel>\n")
                FF.write("    <title><![CDATA[Pagina Siguiente]]></title>\n")
                FF.write('    <description><![CDATA[<img src="http://ps3plusteam.ddns.net/ps3plus/images/letras/siguiente.png">]]>Avanza a la pagina siguiente para ver mas Series!</description>\n')
                FF.write('    <img_src><![CDATA[http://ps3plusteam.ddns.net/ps3plus/images/letras/siguiente.png]]></img_src>\n')
                FF.write('    <ts_stream><![CDATA[' + str(i) + ']]></ts_stream>\n')
                FF.write('    <tipo><![CDATA[megadedeunidad]]></tipo>\n')
                FF.write('</channel>\n\n')
                
            if i == 1:
                FF.write('<prev_page_url text="CH- ATRAS"><![CDATA[/cosas/megadede.xml]]></prev_page_url>\n</items>')
            if i == 2:
                FF.write('<prev_page_url text="CH- ATRAS"><![CDATA[/tmp/archivostv/Navegar en Series0.xml]]></prev_page_url>\n</items>')
            if i > 2:
                i = i - 1
                FF.write('<prev_page_url text="CH- ATRAS"><![CDATA[/tmp/archivostv/Pagina Siguiente' + str(i - 1) + '.xml]]></prev_page_url>\n</items>')
            
            FF.close()
            return Categ
            
    except Exception as er:
        print "Error: "+ str(er) + " En NavegarSeries"
        print "Error: "+ str(er) + " En NavegarSeries"
        print "Error: "+ str(er) + " En NavegarSeries"
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
        Name = Name.replace(" ", "-")

        
        if OPT == 1: # Series
            url = 'http://www.megadede.com/search/' + Name
            
            req = urllib2.Request(url)
            req.add_header('User-Agent', user_agent_default)
            req.add_header('Referer', 'http://www.megadede.com/')
            Abrir = OP(req)
            data = Abrir.read()
            Abrir.close()
            
            Resultados = re.findall(r'href="(.*?)".+title="(.*?)".+\n.+\n.+\n.+src="(.*?)"', data)
        elif OPT == 0: # Peliculas
            url = 'http://www.megadede.com/search/' + Name
            
            req = urllib2.Request(url)
            req.add_header('User-Agent', user_agent_default)
            req.add_header('Referer', 'http://www.megadede.com/')
            Abrir = OP(req)
            data = Abrir.read()
            Abrir.close()
            
            Resultados = re.findall(r'href="(.*?)".+title="(.*?)".+\n.+\n.+\n.+src="(.*?)"', data)

        elif OPT == 2: # Documentales
            url = 'http://www.pordede.com/search/' + Name
            
            req = urllib2.Request(url)
            req.add_header('User-Agent', user_agent_default)
            req.add_header('Referer', 'http://www.pordede.com/index2.php')
            Abrir = OP(req)
            data = Abrir.read()
            Abrir.close()
            
            INI = data.find("<section id=\"page\"")
            FIN = data.find("<div class=\"footerTitle\">")
            
            data = data[INI:FIN]
            
            Resultados = re.findall(r'defaultLink extended" href="/docu/(.*?)">\s+.+title="(.*?)">\s+.+src="(.*?)"/', data)
        elif OPT == 3: # TVSHOWS
            url = 'http://www.pordede.com/search/' + Name
            
            req = urllib2.Request(url)
            req.add_header('User-Agent', user_agent_default)
            req.add_header('Referer', 'http://www.pordede.com/index2.php')
            Abrir = OP(req)
            data = Abrir.read()
            Abrir.close()
            
            INI = data.find("<section id=\"page\"")
            FIN = data.find("<div class=\"footerTitle\">")
            
            data = data[INI:FIN]
            
            Resultados = re.findall(r'defaultLink extended" href="/tvshow/(.*?)">\s+.+title="(.*?)">\s+.+src="(.*?)"/', data)
        else:
            pass
        
        if Resultados == []:
            Mensaje = "Error","No hay mas resultados aqui."
            FF.close()
            return [1, Mensaje]
            
        FF = open(Categ, 'w')
        FF.write('<?xml version="1.0" encoding="iso-8859-1"?>\n<items>\n<playlist_name><![CDATA[Buscando ' + Nombre + ']]></playlist_name>\n\n')
        
        for enlace,titulo,imagen in Resultados:
            EN = enlace
            TI = titulo
            IMAG = imagen
            ImgDefinitiva = ObtenImagenes(self, IMAG)
            
            
            if OPT == 1 and imagen.find('serie') != -1:
                FF.write("<channel>\n")
                FF.write("    <title><![CDATA[" + TI.encode('utf8') + "]]></title>\n")
                FF.write('    <description><![CDATA[<img src="' + IMAG + '">]]></description>\n')
                FF.write('    <playlist_url><![CDATA[' + EN + ']]></playlist_url>\n')
                FF.write('    <img_src><![CDATA[' + ImgDefinitiva + ']]></img_src>\n')
                FF.write('    <tipo><![CDATA[megadedeCapitulos]]></tipo>\n')
                FF.write('    <historial><![CDATA[' + Categ + ']]></historial>\n')
                FF.write('</channel>\n\n')
            elif OPT == 0 and imagen.find('peli') != -1:
                FF.write("<channel>\n")
                FF.write("    <title><![CDATA[" + TI.encode('utf8') + "]]></title>\n")
                FF.write('    <description><![CDATA[<img src="' + IMAG + '">]]></description>\n')
                FF.write('    <playlist_url><![CDATA[' + EN + ']]></playlist_url>\n')
                FF.write('    <img_src><![CDATA[' + ImgDefinitiva + ']]></img_src>\n')
                FF.write('    <tipo><![CDATA[megadedeEnlaces]]></tipo>\n')
                FF.write('    <historial><![CDATA[' + Categ + ']]></historial>\n')
                FF.write('</channel>\n\n')
            elif OPT == 2:
                FF.write("type=poraa\nname=" + TI +"\nthumb=" + IM + "\nURL=http://www.pordede.com/docu/" + EN + "\ndescription=./description\n\n")
            elif OPT == 3:
                FF.write("type=poraa\nname=" + TI +"\nthumb=" + IM + "\nURL=http://www.pordede.com/tvshow/" + EN + "\ndescription=./description\n\n")
            else:
                pass

        FF.write('<prev_page_url text="CH- ATRAS"><![CDATA[/cosas/megadede.xml]]></prev_page_url>\n</items>')
        FF.close()
            
        return Categ
    except Exception as er:
        print "Error megadede en Busca: " + str(er)
        print "Error megadede en Busca: " + str(er)
        return [1, er]
        
def SacaSinopsis(tipo, enlace):
    try:
        if tipo == "Pelicula":
            enn = enlace + "?language=es-ES"
            req = urllib2.Request(enn)
            req.add_header('User-Agent',user_agent_default)
            Abrir = OP(req, timeout=8)
            data = Abrir.read()
            Abrir.close()
            
            BuscaSinopsis = re.findall(r'og:description"\s+content="(.*?)">', data)
            
            return BuscaSinopsis[0]
        else:
            enn = enlace
            req = urllib2.Request(enn)
            req.add_header('User-Agent',user_agent_default)
            Abrir = OP(req, timeout=8)
            data = Abrir.read()
            Abrir.close()
            
            BuscaSinopsis = re.findall(r'data-language="spa"\s+.+\s+.+\s+.\s+<p>(.*)', data)
            
            return BuscaSinopsis[0]
    except Exception as er:
        return "No hay descripcion"
    
        
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
