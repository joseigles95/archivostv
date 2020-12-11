# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/archivostv/mediaitem.py
from string import *
import sys, os.path
import urllib
import ftplib
import os
import socket
import re, random, string
import shutil

class CMediaItem:
    def __init__(
        self,
        type='unknown',
        version='2',
        name='',
        description='',
        date='',
        thumb='default',
        icon='default',
        URL='',
        DLloc='',
        epgid='',
        player='default',
        processor='',
        playpath='',
        swfplayer='',
        pageurl='',
        referer='',
        agent='',
        background='default',
        rating='',
        infotag='',
        view='default',
        processed=False,
        data={}
    ):
        self.type = type    #(required) type (playlist, image, video, audio, text)
        self.version = version #(optional) playlist version
        self.name = name    #(required) name as displayed in list view
        self.description = description    #(optional) description of this item
        self.date = date    #(optional) release date of this item (yyyy-mm-dd)
        self.thumb = thumb  #(optional) URL to thumb image or 'default'
        self.icon = icon  #(optional) URL to icon image or 'default'
        self.URL = URL      #(required) URL to playlist entry
        self.DLloc = DLloc  #(optional) Download location
        self.epgid = epgid #(opcional) ID del epg del canal
        self.player = player #(optional) player core to use for playback
        self.processor = processor #(optional) URL to mediaitem processing server 
        self.playpath = playpath #(optional) 
        self.swfplayer = swfplayer #(optional)
        self.pageurl = pageurl #(optional)
        self.background = background #(optional) background image
        self.rating = rating #(optional) rating value
        self.infotag = infotag
        self.referer = referer #(optional)
        self.agent = agent #(optional)
        self.view = view #(optional) List view option (list, panel)
        self.processed = processed
        self.data = data #(optional) multi-purpose slot for Python dictionaries
               
    ######################################################################
    # Description: Get mediaitem type.
    # Parameters : field: field to retrieve (type or attributes)
    # Return     : -
    ######################################################################
    def GetType(self, field=0):
        index = self.type.find(':')
        if index != -1:
            if field == 0:
                value = self.type[:index]
            elif field == 1:
                value = self.type[index+1:]
            else: #invalid field
                value == ''
        else:
            if field == 0:
                value = self.type
            elif field == 1:
                value = ''
            else: #invalid field
                value == ''

        return value