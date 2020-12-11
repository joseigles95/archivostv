# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/archivostv/cloutd.py
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.Sources.StaticText import StaticText
from Components.MenuList import MenuList
from enigma import eTimer
import time as Tiempo

def countdown_timer(delay_time):
    if delay_time==0:
        print '0-second delay time specified; returning'
        return True


    secs=0
    while secs<delay_time:
        secs=secs+1
        Tiempo.sleep(1)

    print 'Wait finished'