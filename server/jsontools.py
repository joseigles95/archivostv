# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/archivostv/jsontools.py
# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------------
# json_tools - JSON load and parse functions with library detection
# --------------------------------------------------------------------------------

import traceback

try:
    import json
except:
    print "json incluido en el interprete **NO** disponible"

    try:
        import simplejson as json
    except:
        print "simplejson incluido en el interprete **NO** disponible"
        try:
            from lib import simplejson as json
        except:
            print "simplejson en el directorio lib **NO** disponible"
            print "No se ha encontrado un parser de JSON valido"
            json = None
        else:
            print "Usando simplejson en el directorio lib"
    else:
        print "Usando simplejson incluido en el interprete"
else:
    print "Usando json incluido en el interprete"


def load(*args, **kwargs):
    if "object_hook" not in kwargs:
        kwargs["object_hook"] = to_utf8

    try:
        value = json.loads(*args, **kwargs)
    except:
        print "**NO** se ha podido cargar el JSON"
        print traceback.format_exc()
        value = {}

    return value


def dump(*args, **kwargs):
    if not kwargs:
        kwargs = {"indent": 4, "skipkeys": True, "sort_keys": True, "ensure_ascii": False}

    try:
        value = json.dumps(*args, **kwargs)
    except:
        print "**NO** se ha podido cargar el JSON" 
        print traceback.format_exc() 
        value = ""
    return value


def to_utf8(dct):
    if isinstance(dct, dict):
        return dict((to_utf8(key), to_utf8(value)) for key, value in dct.iteritems())
    elif isinstance(dct, list):
        return [to_utf8(element) for element in dct]
    elif isinstance(dct, unicode):
        return dct.encode('utf-8')
    else:
        return dct