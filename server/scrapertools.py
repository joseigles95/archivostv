# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/archivostv/scrapertools.py
import urlparse, urllib2, urllib
import time
import os
import re
import socket

def get_match(data, patron, index = 0):
    matches = re.findall(patron, data, flags=re.DOTALL)
    return matches[index]


def find_single_match(data, patron, index = 0):
    try:
        matches = re.findall(patron, data, flags=re.DOTALL)
        return matches[index]
    except:
        return ''


def find_multiple_matches(text, pattern):
    return re.findall(pattern, text, re.DOTALL)


def htmlclean(cadena):
    cadena = re.compile('<!--.*?-->', re.DOTALL).sub('', cadena)
    cadena = cadena.replace('<center>', '')
    cadena = cadena.replace('</center>', '')
    cadena = cadena.replace('<cite>', '')
    cadena = cadena.replace('</cite>', '')
    cadena = cadena.replace('<em>', '')
    cadena = cadena.replace('</em>', '')
    cadena = cadena.replace('<u>', '')
    cadena = cadena.replace('</u>', '')
    cadena = cadena.replace('<li>', '')
    cadena = cadena.replace('</li>', '')
    cadena = cadena.replace('<turl>', '')
    cadena = cadena.replace('</tbody>', '')
    cadena = cadena.replace('<tr>', '')
    cadena = cadena.replace('</tr>', '')
    cadena = cadena.replace('<![CDATA[', '')
    cadena = cadena.replace('<Br />', ' ')
    cadena = cadena.replace('<BR />', ' ')
    cadena = cadena.replace('<Br>', ' ')
    cadena = re.compile('<br[^>]*>', re.DOTALL).sub(' ', cadena)
    cadena = re.compile('<script.*?</script>', re.DOTALL).sub('', cadena)
    cadena = re.compile('<option[^>]*>', re.DOTALL).sub('', cadena)
    cadena = cadena.replace('</option>', '')
    cadena = re.compile('<button[^>]*>', re.DOTALL).sub('', cadena)
    cadena = cadena.replace('</button>', '')
    cadena = re.compile('<i[^>]*>', re.DOTALL).sub('', cadena)
    cadena = cadena.replace('</iframe>', '')
    cadena = cadena.replace('</i>', '')
    cadena = re.compile('<table[^>]*>', re.DOTALL).sub('', cadena)
    cadena = cadena.replace('</table>', '')
    cadena = re.compile('<td[^>]*>', re.DOTALL).sub('', cadena)
    cadena = cadena.replace('</td>', '')
    cadena = re.compile('<div[^>]*>', re.DOTALL).sub('', cadena)
    cadena = cadena.replace('</div>', '')
    cadena = re.compile('<dd[^>]*>', re.DOTALL).sub('', cadena)
    cadena = cadena.replace('</dd>', '')
    cadena = re.compile('<b[^>]*>', re.DOTALL).sub('', cadena)
    cadena = cadena.replace('</b>', '')
    cadena = re.compile('<font[^>]*>', re.DOTALL).sub('', cadena)
    cadena = cadena.replace('</font>', '')
    cadena = re.compile('<strong[^>]*>', re.DOTALL).sub('', cadena)
    cadena = cadena.replace('</strong>', '')
    cadena = re.compile('<small[^>]*>', re.DOTALL).sub('', cadena)
    cadena = cadena.replace('</small>', '')
    cadena = re.compile('<span[^>]*>', re.DOTALL).sub('', cadena)
    cadena = cadena.replace('</span>', '')
    cadena = re.compile('<a[^>]*>', re.DOTALL).sub('', cadena)
    cadena = cadena.replace('</a>', '')
    cadena = re.compile('<p[^>]*>', re.DOTALL).sub('', cadena)
    cadena = cadena.replace('</p>', '')
    cadena = re.compile('<ul[^>]*>', re.DOTALL).sub('', cadena)
    cadena = cadena.replace('</ul>', '')
    cadena = re.compile('<h1[^>]*>', re.DOTALL).sub('', cadena)
    cadena = cadena.replace('</h1>', '')
    cadena = re.compile('<h2[^>]*>', re.DOTALL).sub('', cadena)
    cadena = cadena.replace('</h2>', '')
    cadena = re.compile('<h3[^>]*>', re.DOTALL).sub('', cadena)
    cadena = cadena.replace('</h3>', '')
    cadena = re.compile('<h4[^>]*>', re.DOTALL).sub('', cadena)
    cadena = cadena.replace('</h4>', '')
    cadena = re.compile('<!--[^-]+-->', re.DOTALL).sub('', cadena)
    cadena = re.compile('<img[^>]*>', re.DOTALL).sub('', cadena)
    cadena = re.compile('<object[^>]*>', re.DOTALL).sub('', cadena)
    cadena = cadena.replace('</object>', '')
    cadena = re.compile('<param[^>]*>', re.DOTALL).sub('', cadena)
    cadena = cadena.replace('</param>', '')
    cadena = re.compile('<embed[^>]*>', re.DOTALL).sub('', cadena)
    cadena = cadena.replace('</embed>', '')
    cadena = re.compile('<title[^>]*>', re.DOTALL).sub('', cadena)
    cadena = cadena.replace('</title>', '')
    cadena = re.compile('<link[^>]*>', re.DOTALL).sub('', cadena)
    cadena = cadena.replace('\t', '')
    cadena = entityunescape(cadena)
    return cadena


def entityunescape(cadena):
    return unescape(cadena)


def unescape(text):
    """Removes HTML or XML character references
       and entities from a text string.
       keep &amp;, &gt;, &lt; in the source code.
    from Fredrik Lundh
    http://effbot.org/zone/re-sub.htm#unescape-html
    """

    def fixup(m):
        text = m.group(0)
        if text[:2] == '&#':
            try:
                if text[:3] == '&#x':
                    return unichr(int(text[3:-1], 16)).encode('utf-8')
                return unichr(int(text[2:-1])).encode('utf-8')
            except ValueError:
                logger.info('error de valor')

        else:
            try:
                import htmlentitydefs
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]]).encode('utf-8')
            except KeyError:
                logger.info('keyerror')
            except:
                pass

        return text

    return re.sub('&#?\\w+;', fixup, text)