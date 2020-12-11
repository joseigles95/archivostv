# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/TSmedia/__init__.py
import ssl
try:
    ssl._create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = ssl._create_unverified_https_context