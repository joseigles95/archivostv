# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/archivostv/cosas/Teclado.py
from Components.Language import language
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.MenuList import MenuList
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from enigma import eListboxPythonMultiContent, gFont, RT_HALIGN_CENTER, RT_VALIGN_CENTER
from Screens.Screen import Screen
from Tools.Directories import resolveFilename, SCOPE_CURRENT_SKIN
from Tools.LoadPixmap import LoadPixmap
PLUGIN_PATH = '/usr/lib/enigma2/python/Plugins/Extensions/archivostv'

class VirtualKeyBoardList(MenuList):

    def __init__(self, list, enableWrapAround = False):
        MenuList.__init__(self, list, enableWrapAround, eListboxPythonMultiContent)
        self.l.setFont(0, gFont('Regular', 28))
        self.l.setItemHeight(45)


def VirtualKeyBoardEntryComponent(keys, selectedKey, shiftMode = False):
    global PLUGIN_PATH
    key_backspace = LoadPixmap(cached=True, path='%s/img/vkey_backspace.png' % PLUGIN_PATH)
    key_bg = LoadPixmap(cached=True, path='%s/img/vkey_bg.png' % PLUGIN_PATH)
    key_clr = LoadPixmap(cached=True, path='%s/img/vkey_clr.png' % PLUGIN_PATH)
    key_esc = LoadPixmap(cached=True, path='%s/img/vkey_esc.png' % PLUGIN_PATH)
    key_ok = LoadPixmap(cached=True, path='%s/img/vkey_ok.png' % PLUGIN_PATH)
    key_sel = LoadPixmap(cached=True, path='%s/img/vkey_sel.png' % PLUGIN_PATH)
    key_shift = LoadPixmap(cached=True, path='%s/img/vkey_shift.png' % PLUGIN_PATH)
    key_shift_sel = LoadPixmap(cached=True, path='%s/img/vkey_shift_sel.png' % PLUGIN_PATH)
    key_space = LoadPixmap(cached=True, path='%s/img/vkey_space.png' % PLUGIN_PATH)
    res = [keys]
    x = 0
    count = 0
    if shiftMode:
        shiftkey_png = key_shift_sel
    else:
        shiftkey_png = key_shift
    for key in keys:
        width = None
        if key == 'EXIT':
            width = key_esc.size().width()
            res.append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, 45), png=key_esc))
        elif key == 'BACKSPACE':
            width = key_backspace.size().width()
            res.append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, 45), png=key_backspace))
        elif key == 'CLEAR':
            width = key_clr.size().width()
            res.append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, 45), png=key_clr))
        elif key == 'SHIFT':
            width = shiftkey_png.size().width()
            res.append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, 45), png=shiftkey_png))
        elif key == 'SPACE':
            width = key_space.size().width()
            res.append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, 45), png=key_space))
        elif key == 'OK':
            width = key_ok.size().width()
            res.append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, 45), png=key_ok))
        else:
            width = key_bg.size().width()
            res.extend((MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, 45), png=key_bg), MultiContentEntryText(pos=(x, 0), size=(width, 45), font=0, text=key.encode('utf-8'), flags=RT_HALIGN_CENTER | RT_VALIGN_CENTER)))
        if selectedKey == count:
            width = key_sel.size().width()
            res.append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, 45), png=key_sel))
        if width is not None:
            x += width
        else:
            x += 45
        count += 1

    return res
    
IMAGENCAPTCHA = ""

def Introducido(self, texx):
    print texx
    print "jajajajaj "

    
def Testealo(self, img):
    global IMAGENCAPTCHA
    IMAGENCAPTCHA = img
    print "Vale Entramos en el TeclaPlusdede"
    #TecladoVirtualPlusdede("Testeandoooo")
    #XXX = self.session.open(TecladoVirtualPlusdede)
    Lanzalo = self.session.openWithCallback(Introducido, TecladoVirtualPlusdede, title="Escribe los numeros: ", text=IMAGENCAPTCHA)
    
class TecladoVirtualPlusdede(Screen):
    global IMAGENCAPTCHA
    skin = '\n\t<screen name="TecladoVirtualPlusdede"  position="center,center" size="560,350" zPosition="99" title="Escribe los numeros: " flags="wfNoBorder">\n\t\t<ePixmap name="imagen" position="8,349" zPosition="0" size="542,183" pixmap="' + IMAGENCAPTCHA + '" transparent="1" alphatest="on" />\n\t\t<ePixmap pixmap="skin_default/vkey_text.png" position="9,35" zPosition="-4" size="542,52" alphatest="on" />\n\t\t<widget name="header" position="10,10" size="500,20" font="Regular;20" transparent="1" noWrap="1" />\n\t\t<widget name="text" position="12,35" size="536,44" font="Regular;40" transparent="1" noWrap="1" halign="right" />\n\t\t<widget name="list" position="10,100" size="540,225" selectionDisabled="1" transparent="0" />\n\t</screen>'

    def __init__(self, session, title = '', text = '', imagen=''):
        Screen.__init__(self, session)
        self.skin = '\n\t<screen name="TecladoVirtualPlusdede"  position="center,center" size="560,425" zPosition="99" title="Escribe los numeros: " flags="wfNoBorder">\n\t\t<ePixmap name="imagen" position="10,335" zPosition="0" size="348,111" pixmap="' + imagen + '" transparent="1" alphatest="on" />\n\t\t<ePixmap pixmap="skin_default/vkey_text.png" position="9,35" zPosition="-4" size="542,52" alphatest="on" />\n\t\t<widget name="header" position="10,10" size="500,20" font="Regular;20" transparent="1" noWrap="1" />\n\t\t<widget name="text" position="12,35" size="536,44" font="Regular;40" transparent="1" noWrap="1" halign="right" />\n\t\t<widget name="list" position="10,100" size="540,225" selectionDisabled="1" transparent="0" />\n\t</screen>'
        #self.skin = TecladoVirtualPlusdede.skin
        self.keys_list = []
        self.shiftkeys_list = []
        self.lang = language.getLanguage()
        self.keys_list = [[u'EXIT',
          u'1',
          u'2',
          u'3',
          u'4',
          u'5',
          u'6',
          u'7',
          u'8',
          u'9',
          u'0',
          u'BACKSPACE'],
         [u'q',
          u'w',
          u'e',
          u'r',
          u't',
          u'y',
          u'u',
          u'i',
          u'o',
          u'p',
          u'?',
          u'#'],
         [u'a',
          u's',
          u'd',
          u'f',
          u'g',
          u'h',
          u'j',
          u'k',
          u'l',
          u"'",
          u';',
          u':'],
         [u'>',
          u'z',
          u'x',
          u'c',
          u'v',
          u'b',
          u'n',
          u'm',
          u'<',
          u'+',
          u'-',
          u'CLEAR'],
         [u'SHIFT', u'SPACE', u'OK']]
        self.shiftkeys_list = [[u'EXIT',
          u'!',
          u'"',
          u'\xa7',
          u'$',
          u'%',
          u'&',
          u'/',
          u'(',
          u')',
          u'=',
          u'BACKSPACE'],
         [u'Q',
          u'W',
          u'E',
          u'R',
          u'T',
          u'Z',
          u'U',
          u'I',
          u'O',
          u'P',
          u'?',
          u'#'],
         [u'A',
          u'S',
          u'D',
          u'F',
          u'G',
          u'H',
          u'J',
          u'K',
          u'L',
          u"'",
          u';',
          u':'],
         [u'>',
          u'Y',
          u'X',
          u'C',
          u'V',
          u'B',
          u'N',
          u'M',
          u'<',
          u'+',
          u'_',
          u'CLEAR'],
         [u'SHIFT', u'SPACE', u'OK']]
        self.shiftMode = False
        self.text = text
        self.selectedKey = 0
        self['header'] = Label(title)
        self['text'] = Label(self.text)
        self['list'] = VirtualKeyBoardList([])
        self['actions'] = ActionMap(['OkCancelActions', 'WizardActions', 'ColorActions'], {'ok': self.okClicked,
         'cancel': self.exit,
         'left': self.left,
         'right': self.right,
         'up': self.up,
         'down': self.down,
         'red': self.exit,
         'yellow': self.backClicked,
         'green': self.ok,
         'blue': self.shiftClicked}, -2)
        self.onLayoutFinish.append(self.buildVirtualKeyBoard)
        self.max_key = 47 + len(self.keys_list[4])

    def shiftClicked(self):
        if self.shiftMode:
            self.shiftMode = False
        else:
            self.shiftMode = True
        self.buildVirtualKeyBoard(self.selectedKey)

    def buildVirtualKeyBoard(self, selectedKey = 0):
        list = []
        if self.shiftMode:
            self.k_list = self.shiftkeys_list
            for keys in self.k_list:
                if selectedKey < 12 and selectedKey > -1:
                    list.append(VirtualKeyBoardEntryComponent(keys, selectedKey, True))
                else:
                    list.append(VirtualKeyBoardEntryComponent(keys, -1, True))
                selectedKey -= 12

        else:
            self.k_list = self.keys_list
            for keys in self.k_list:
                if selectedKey < 12 and selectedKey > -1:
                    list.append(VirtualKeyBoardEntryComponent(keys, selectedKey))
                else:
                    list.append(VirtualKeyBoardEntryComponent(keys, -1))
                selectedKey -= 12

        self['list'].setList(list)

    def backClicked(self):
        self.text = self['text'].getText()
        self.text = unicode(self.text)[:-1]
        self.text = self.text.encode('utf-8')
        self['text'].setText(self.text)

    def okClicked(self):
        if self.shiftMode:
            list = self.shiftkeys_list
        else:
            list = self.keys_list
        selectedKey = self.selectedKey
        text = None
        for x in list:
            if selectedKey < 12:
                if selectedKey < len(x):
                    text = x[selectedKey]
                break
            else:
                selectedKey -= 12

        if text is None:
            return
        else:
            text = text.encode('utf-8')
            if text == 'EXIT':
                self.close(None)
            elif text == 'BACKSPACE':
                self.text = self['text'].getText()
                self.text = unicode(self.text)[:-1]
                self.text = self.text.encode('utf-8')
                self['text'].setText(self.text)
            elif text == 'CLEAR':
                self.text = ''
                self['text'].setText(self.text)
            elif text == 'SHIFT':
                if self.shiftMode:
                    self.shiftMode = False
                else:
                    self.shiftMode = True
                self.buildVirtualKeyBoard(self.selectedKey)
            elif text == 'SPACE':
                self.text += ' '
                self['text'].setText(self.text)
            elif text == 'OK':
                self.close(self['text'].getText())
            else:
                self.text = self['text'].getText()
                self.text += text
                self['text'].setText(self.text)
            return

    def ok(self):
        self.close(self['text'].getText())

    def exit(self):
        self.close(None)
        return

    def left(self):
        self.selectedKey -= 1
        if self.selectedKey == -1:
            self.selectedKey = 11
        elif self.selectedKey == 11:
            self.selectedKey = 23
        elif self.selectedKey == 23:
            self.selectedKey = 35
        elif self.selectedKey == 35:
            self.selectedKey = 47
        elif self.selectedKey == 47:
            self.selectedKey = self.max_key
        self.showActiveKey()

    def right(self):
        self.selectedKey += 1
        if self.selectedKey == 12:
            self.selectedKey = 0
        elif self.selectedKey == 24:
            self.selectedKey = 12
        elif self.selectedKey == 36:
            self.selectedKey = 24
        elif self.selectedKey == 48:
            self.selectedKey = 36
        elif self.selectedKey > self.max_key:
            self.selectedKey = 48
        self.showActiveKey()

    def up(self):
        self.selectedKey -= 12
        if self.selectedKey < 0 and self.selectedKey > self.max_key - 60:
            self.selectedKey += 48
        elif self.selectedKey < 0:
            self.selectedKey += 60
        self.showActiveKey()

    def down(self):
        self.selectedKey += 12
        if self.selectedKey > self.max_key and self.selectedKey > 59:
            self.selectedKey -= 60
        elif self.selectedKey > self.max_key:
            self.selectedKey -= 48
        self.showActiveKey()

    def showActiveKey(self):
        self.buildVirtualKeyBoard(self.selectedKey)
        
class TecladoVirtualA(Screen):
    skin = '\n\t<screen name="TecladoVirtualA"  position="center,center" size="560,350" zPosition="99" title="Teclado Virtual" flags="wfNoBorder">\n\t\t<ePixmap pixmap="skin_default/vkey_text.png" position="9,35" zPosition="-4" size="542,52" alphatest="on" />\n\t\t<widget name="header" position="10,10" size="500,20" font="Regular;20" transparent="1" noWrap="1" />\n\t\t<widget name="text" position="12,35" size="536,44" font="Regular;40" transparent="1" noWrap="1" halign="right" />\n\t\t<widget name="list" position="10,100" size="540,225" selectionDisabled="1" transparent="0" />\n\t</screen>'

    def __init__(self, session, title = '', text = ''):
        Screen.__init__(self, session)
        self.skin = TecladoVirtualA.skin
        self.keys_list = []
        self.shiftkeys_list = []
        self.lang = language.getLanguage()
        self.keys_list = [[u'EXIT',
          u'1',
          u'2',
          u'3',
          u'4',
          u'5',
          u'6',
          u'7',
          u'8',
          u'9',
          u'0',
          u'BACKSPACE'],
         [u'q',
          u'w',
          u'e',
          u'r',
          u't',
          u'y',
          u'u',
          u'i',
          u'o',
          u'p',
          u'?',
          u'#'],
         [u'a',
          u's',
          u'd',
          u'f',
          u'g',
          u'h',
          u'j',
          u'k',
          u'l',
          u"'",
          u';',
          u':'],
         [u'>',
          u'z',
          u'x',
          u'c',
          u'v',
          u'b',
          u'n',
          u'm',
          u'<',
          u'+',
          u'-',
          u'CLEAR'],
         [u'SHIFT', u'SPACE', u'OK']]
        self.shiftkeys_list = [[u'EXIT',
          u'!',
          u'"',
          u'\xa7',
          u'$',
          u'%',
          u'&',
          u'/',
          u'(',
          u')',
          u'=',
          u'BACKSPACE'],
         [u'Q',
          u'W',
          u'E',
          u'R',
          u'T',
          u'Z',
          u'U',
          u'I',
          u'O',
          u'P',
          u'?',
          u'#'],
         [u'A',
          u'S',
          u'D',
          u'F',
          u'G',
          u'H',
          u'J',
          u'K',
          u'L',
          u"'",
          u';',
          u':'],
         [u'>',
          u'Y',
          u'X',
          u'C',
          u'V',
          u'B',
          u'N',
          u'M',
          u'<',
          u'+',
          u'_',
          u'CLEAR'],
         [u'SHIFT', u'SPACE', u'OK']]
        self.shiftMode = False
        self.text = text
        self.selectedKey = 0
        self['header'] = Label(title)
        self['text'] = Label(self.text)
        self['list'] = VirtualKeyBoardList([])
        self['actions'] = ActionMap(['OkCancelActions', 'WizardActions', 'ColorActions'], {'ok': self.okClicked,
         'cancel': self.exit,
         'left': self.left,
         'right': self.right,
         'up': self.up,
         'down': self.down,
         'red': self.exit,
         'yellow': self.backClicked,
         'green': self.ok,
         'blue': self.shiftClicked}, -2)
        self.onLayoutFinish.append(self.buildVirtualKeyBoard)
        self.max_key = 47 + len(self.keys_list[4])

    def shiftClicked(self):
        if self.shiftMode:
            self.shiftMode = False
        else:
            self.shiftMode = True
        self.buildVirtualKeyBoard(self.selectedKey)

    def buildVirtualKeyBoard(self, selectedKey = 0):
        list = []
        if self.shiftMode:
            self.k_list = self.shiftkeys_list
            for keys in self.k_list:
                if selectedKey < 12 and selectedKey > -1:
                    list.append(VirtualKeyBoardEntryComponent(keys, selectedKey, True))
                else:
                    list.append(VirtualKeyBoardEntryComponent(keys, -1, True))
                selectedKey -= 12

        else:
            self.k_list = self.keys_list
            for keys in self.k_list:
                if selectedKey < 12 and selectedKey > -1:
                    list.append(VirtualKeyBoardEntryComponent(keys, selectedKey))
                else:
                    list.append(VirtualKeyBoardEntryComponent(keys, -1))
                selectedKey -= 12

        self['list'].setList(list)

    def backClicked(self):
        self.text = self['text'].getText()
        self.text = unicode(self.text)[:-1]
        self.text = self.text.encode('utf-8')
        self['text'].setText(self.text)

    def okClicked(self):
        if self.shiftMode:
            list = self.shiftkeys_list
        else:
            list = self.keys_list
        selectedKey = self.selectedKey
        text = None
        for x in list:
            if selectedKey < 12:
                if selectedKey < len(x):
                    text = x[selectedKey]
                break
            else:
                selectedKey -= 12

        if text is None:
            return
        else:
            text = text.encode('utf-8')
            if text == 'EXIT':
                self.close(None)
            elif text == 'BACKSPACE':
                self.text = self['text'].getText()
                self.text = unicode(self.text)[:-1]
                self.text = self.text.encode('utf-8')
                self['text'].setText(self.text)
            elif text == 'CLEAR':
                self.text = ''
                self['text'].setText(self.text)
            elif text == 'SHIFT':
                if self.shiftMode:
                    self.shiftMode = False
                else:
                    self.shiftMode = True
                self.buildVirtualKeyBoard(self.selectedKey)
            elif text == 'SPACE':
                self.text += ' '
                self['text'].setText(self.text)
            elif text == 'OK':
                self.close(self['text'].getText())
            else:
                self.text = self['text'].getText()
                self.text += text
                self['text'].setText(self.text)
            return

    def ok(self):
        self.close(self['text'].getText())

    def exit(self):
        self.close(None)
        return

    def left(self):
        self.selectedKey -= 1
        if self.selectedKey == -1:
            self.selectedKey = 11
        elif self.selectedKey == 11:
            self.selectedKey = 23
        elif self.selectedKey == 23:
            self.selectedKey = 35
        elif self.selectedKey == 35:
            self.selectedKey = 47
        elif self.selectedKey == 47:
            self.selectedKey = self.max_key
        self.showActiveKey()

    def right(self):
        self.selectedKey += 1
        if self.selectedKey == 12:
            self.selectedKey = 0
        elif self.selectedKey == 24:
            self.selectedKey = 12
        elif self.selectedKey == 36:
            self.selectedKey = 24
        elif self.selectedKey == 48:
            self.selectedKey = 36
        elif self.selectedKey > self.max_key:
            self.selectedKey = 48
        self.showActiveKey()

    def up(self):
        self.selectedKey -= 12
        if self.selectedKey < 0 and self.selectedKey > self.max_key - 60:
            self.selectedKey += 48
        elif self.selectedKey < 0:
            self.selectedKey += 60
        self.showActiveKey()

    def down(self):
        self.selectedKey += 12
        if self.selectedKey > self.max_key and self.selectedKey > 59:
            self.selectedKey -= 60
        elif self.selectedKey > self.max_key:
            self.selectedKey -= 48
        self.showActiveKey()

    def showActiveKey(self):
        self.buildVirtualKeyBoard(self.selectedKey)


class Teclado_FIXED(Screen):
    skin = '\n\t<screen name="Teclado_FIXED"  position="center,center" size="560,350" zPosition="99" title="Virtual KeyBoard" flags="wfNoBorder">\n\t\t<ePixmap pixmap="skin_default/vkey_text.png" position="9,35" zPosition="-4" size="542,52" alphatest="on" />\n\t\t<widget name="header" position="10,10" size="500,20" font="RegularIPTV;20" transparent="1" noWrap="1" />\n\t\t<widget name="text" position="12,35" size="536,44" font="RegularIPTV;40" transparent="1" noWrap="1" halign="right" />\n\t\t<widget name="list" position="10,100" size="540,225" selectionDisabled="1" transparent="0" />\n\t</screen>'

    def __init__(self, session, title = '', text = ''):
        Screen.__init__(self, session)
        self.skin = Teclado_FIXED.skin
        self.keys_list = []
        self.shiftkeys_list = []
        self.lang = language.getLanguage()
        self.keys_list = [[u'EXIT',
          u'1',
          u'2',
          u'3',
          u'4',
          u'5',
          u'6',
          u'7',
          u'8',
          u'9',
          u'0',
          u'BACKSPACE'],
         ['\xd0\x90',
          '\xd0\x91',
          '\xd0\x92',
          '\xd0\x93',
          '\xd0\x94',
          '\xd0\x95',
          '\xd0\x96',
          '\xd0\x97',
          '\xd0\x98',
          '\xd0\x99',
          '\xd0\x9a',
          '\xd0\x9b'],
         ['\xd0\x9c',
          '\xd0\x9d',
          '\xd0\x9e',
          '\xd0\x9f',
          '\xd0\xa0',
          '\xd0\xa1',
          '\xd0\xa2',
          '\xd0\xa3',
          '\xd0\xa4',
          '\xd0\xa5',
          '\xd0\xa6',
          '\xd0\xa7'],
         ['\xd0\xa8',
          '\xd0\xa9',
          '\xd0\xaa',
          '\xd0\xab',
          '\xd0\xac',
          '\xd0\xad',
          '\xd0\xae',
          '\xd0\xaf',
          u'.',
          u',',
          u'*',
          u'CLEAR'],
         [u'SHIFT', u'SPACE', u'OK']]
        self.shiftkeys_list = [[u'EXIT',
          u'!',
          u'"',
          u'\xa7',
          u'$',
          u'%',
          u'&',
          u'/',
          u'(',
          u')',
          u'=',
          u'BACKSPACE'],
         [u'Q',
          u'W',
          u'E',
          u'R',
          u'T',
          u'Z',
          u'U',
          u'I',
          u'O',
          u'P',
          u'?',
          u'#'],
         [u'A',
          u'S',
          u'D',
          u'F',
          u'G',
          u'H',
          u'J',
          u'K',
          u'L',
          u"'",
          u';',
          u':'],
         [u'>',
          u'Y',
          u'X',
          u'C',
          u'V',
          u'B',
          u'N',
          u'M',
          u'<',
          u'+',
          u'-',
          u'CLEAR'],
         [u'SHIFT', u'SPACE', u'OK']]
        self.shiftMode = False
        self.text = text
        self.selectedKey = 0
        self['header'] = Label(title)
        self['text'] = Label(self.text)
        self['list'] = VirtualKeyBoardList([])
        self['actions'] = ActionMap(['OkCancelActions', 'WizardActions', 'ColorActions'], {'ok': self.okClicked,
         'cancel': self.exit,
         'left': self.left,
         'right': self.right,
         'up': self.up,
         'down': self.down,
         'red': self.exit,
         'yellow': self.backClicked,
         'green': self.ok,
         'blue': self.shiftClicked}, -2)
        self.onLayoutFinish.append(self.buildVirtualKeyBoard)
        self.max_key = 47 + len(self.keys_list[4])

    def shiftClicked(self):
        if self.shiftMode:
            self.shiftMode = False
        else:
            self.shiftMode = True
        self.buildVirtualKeyBoard(self.selectedKey)

    def buildVirtualKeyBoard(self, selectedKey = 0):
        list = []
        if self.shiftMode:
            self.k_list = self.shiftkeys_list
            for keys in self.k_list:
                if selectedKey < 12 and selectedKey > -1:
                    list.append(VirtualKeyBoardEntryComponent(keys, selectedKey, True))
                else:
                    list.append(VirtualKeyBoardEntryComponent(keys, -1, True))
                selectedKey -= 12

        else:
            self.k_list = self.keys_list
            for keys in self.k_list:
                if selectedKey < 12 and selectedKey > -1:
                    list.append(VirtualKeyBoardEntryComponent(keys, selectedKey))
                else:
                    list.append(VirtualKeyBoardEntryComponent(keys, -1))
                selectedKey -= 12

        self['list'].setList(list)

    def backClicked(self):
        self.text = self['text'].getText()
        self.text = unicode(self.text)[:-1]
        self.text = self.text.encode('utf-8')
        self['text'].setText(self.text)

    def okClicked(self):
        if self.shiftMode:
            list = self.shiftkeys_list
        else:
            list = self.keys_list
        selectedKey = self.selectedKey
        text = None
        for x in list:
            if selectedKey < 12:
                if selectedKey < len(x):
                    text = x[selectedKey]
                break
            else:
                selectedKey -= 12

        if text is None:
            return
        else:
            text = text.encode('utf-8')
            if text == 'EXIT':
                self.close(None)
            elif text == 'BACKSPACE':
                self.text = self['text'].getText()
                self.text = unicode(self.text)[:-1]
                self.text = self.text.encode('utf-8')
                self['text'].setText(self.text)
            elif text == 'CLEAR':
                self.text = ''
                self['text'].setText(self.text)
            elif text == 'SHIFT':
                if self.shiftMode:
                    self.shiftMode = False
                else:
                    self.shiftMode = True
                self.buildVirtualKeyBoard(self.selectedKey)
            elif text == 'SPACE':
                self.text += ' '
                self['text'].setText(self.text)
            elif text == 'OK':
                self.close(self['text'].getText())
            else:
                self.text = self['text'].getText()
                self.text += text
                self['text'].setText(self.text)
            return

    def ok(self):
        self.close(self['text'].getText())

    def exit(self):
        self.close(None)
        return

    def left(self):
        self.selectedKey -= 1
        if self.selectedKey == -1:
            self.selectedKey = 11
        elif self.selectedKey == 11:
            self.selectedKey = 23
        elif self.selectedKey == 23:
            self.selectedKey = 35
        elif self.selectedKey == 35:
            self.selectedKey = 47
        elif self.selectedKey == 47:
            self.selectedKey = self.max_key
        self.showActiveKey()

    def right(self):
        self.selectedKey += 1
        if self.selectedKey == 12:
            self.selectedKey = 0
        elif self.selectedKey == 24:
            self.selectedKey = 12
        elif self.selectedKey == 36:
            self.selectedKey = 24
        elif self.selectedKey == 48:
            self.selectedKey = 36
        elif self.selectedKey > self.max_key:
            self.selectedKey = 48
        self.showActiveKey()

    def up(self):
        self.selectedKey -= 12
        if self.selectedKey < 0 and self.selectedKey > self.max_key - 60:
            self.selectedKey += 48
        elif self.selectedKey < 0:
            self.selectedKey += 60
        self.showActiveKey()

    def down(self):
        self.selectedKey += 12
        if self.selectedKey > self.max_key and self.selectedKey > 59:
            self.selectedKey -= 60
        elif self.selectedKey > self.max_key:
            self.selectedKey -= 48
        self.showActiveKey()

    def showActiveKey(self):
        self.buildVirtualKeyBoard(self.selectedKey)