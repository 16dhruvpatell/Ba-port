# ba_meta require api 7
from __future__ import annotations
from typing import TYPE_CHECKING, cast

import ba, _ba, os
from bastd.ui.popup import PopupWindow
from bastd.ui.confirm import ConfirmWindow

if TYPE_CHECKING:
    from typing import Any, Sequence, Callable

words: dict = {
    'require api 6': 'require api 7',
    'on_app_launch': '__init__',
    'ba._enums': 'ba._generated.enums',
    'get_account': 'get_v1_account'}

class ut:
    msg: str = 'bs1.6'
    folder: str = ba.app.python_directory_user
    
    def Lstr(value: str):
        lang = _ba.app.lang.language
        setphrases = {
            "Window.Info":
                {"Spanish": "Es posible que no todos los Plugins\n funcionen correctamente.",
                 "English": "It is possible that not all\n Plugins work correctly.",
                 "Portuguese": "É possível que nem todos os Plugins\n funcionem corretamente."},
            "Window.PluginPorted":
                {"Spanish": "¡Plugin actualizado!",
                 "English": "Updated plugin!",
                 "Portuguese": "Plugin atualizado!"},
            "Window.PluginConfirm":
                {"Spanish": "¿Deseas actualizar este Plugin\n a la versión 1.7+?",
                 "English": "Do you want to update this\n Plugin to version 1.7+?",
                 "Portuguese": "Você deseja atualizar este\n Plugin para a versão 1.7+?"},
            "Found Plugins Message":
                {"Spanish": "Se detectaron Plugins desactualizados.",
                 "English": "Outdated plugins were detected.",
                 "Portuguese": "Foram encontrados plugins desatualizados."},
            }
        language = ["Spanish", "English", "Portuguese"]
        if lang not in language:
            lang = "English"
            
        if value not in setphrases:
            return ba.Lstr(value=value)
        return ba.Lstr(value=setphrases[value][lang])
        
    def open_bs17_window():
        with ba.Context('ui'):
            Port17Window(
                position=(0.0, 0.0),
                size=(2000.0, 1000.0),
                bg_color=(0.3, 0.3, 1.0))

    def found_plugins():
        if len(ut.get_scripts()) > 0:
            ba.timer(1.0, ut.open_bs17_window)
            _ba.screenmessage(ut.Lstr(value='Found Plugins Message'), (0.0, 1.0, 0.0))
            ba.playsound(ba.getsound('ding'))

    def get_scripts():
        files = os.listdir(ut.folder)
        files2 = []
        files3 = []
        
        for f in files:
            if not f.endswith('.py'):
                files2.append(f)
            
        for f2 in files2:
            files.remove(f2)
            
        for f3 in files:
            dir = ut.folder + '/' + f3
            with open(dir) as x:
                lines = x.readlines()
                for line in lines:
                    for w in words:
                        if w in line:
                            if f3 not in files3:
                                files3.append(f3)

        me = __name__ + '.py'
        if me in files3:
            files3.remove(me)

        return files3

# ===== Window ===== #
class Port17Window(PopupWindow):
    def __init__(self, position, size, delegate: ba.Widget = None, **kwargs):
        super().__init__(position, size, **kwargs)
        ba.containerwidget(edit=self.root_widget, scale=0.70)
        
        self._pos = position
        self._size = size
        self._refresh(position, size)

    def _refresh(self, position, size):

        btn_size = (size[0] * 0.8, 100)
        gt = ba.gettexture
        dis = 0.8

        self._width = size[0] * 0.38
        self._height = size[1]
        maxwidth = size[0] * 0.55
        
        self.title_text = ba.textwidget(
            parent=self.root_widget,
            position=(self._width+230, self._height-60),
            size=(0, 0), scale=2.5,
            color=(1.0, 1.0, 1.0),
            maxwidth=maxwidth,
            text='» Mods/Plugins 1.6.X «',
            h_align='center',
            v_align='center')
            
        info_button = ba.buttonwidget(
            position=(self._width*2, self._height-120),
            parent=self.root_widget,
            color=(1.0, 0.4, 0.4),
            button_type='square',
            size=(50, 50),
            label='?',
            scale=1.3)
            
        ba.buttonwidget(
            edit=info_button,
            on_activate_call=ba.Call(
                ConfirmWindow,
                height=100.0+50,
                cancel_button=False,
                origin_widget=info_button,
                text=ut.Lstr(value='Window.Info')))
        
        back_button = b = ba.buttonwidget(
            position=(self._width*0.1, self._height*0.8),
            label=ba.charstr(ba.SpecialChar.BACK),
            on_activate_call=self._back,
            parent=self.root_widget,
            color=(1.0, 0.0, 0.5),
            button_type='square',
            icon=gt('crossOut'),
            iconscale=1.2,
            size=(50, 50),
            scale=1.8)
        ba.containerwidget(edit=self.root_widget,cancel_button=b)
        
        img = ba.imagewidget(
            parent=self.root_widget,
            size=(120, 120),
            texture=ba.gettexture('file'),
            position=(self._width-240, self._height-120))
        
        size = tuple([s*0.8 for s in size])
        self._scrollwidget = ba.scrollwidget(parent=self.root_widget,
                                             position=(position[0] + (19 * 10), position[1]+80),
                                             highlight=False,
                                             size=size)
        self._columnwidget = ba.columnwidget(parent=self._scrollwidget,
                                             border=70, left_border=420)
                                             #margin=50)

        for script in ut.get_scripts():
            wdg = ba.textwidget(
                parent=self._columnwidget,
                size=(size[0] * 0.35, size[1] * 0.05), scale=3.0,
                color=(1.1, 1.1, 1.1),
                maxwidth=maxwidth,
                text=script,
                click_activate=True,
                selectable=True,
                h_align='center',
                v_align='center',
                on_activate_call=ba.Call(self.port_plugin, script))

    def port_plugin(self, file: str) -> None:
        def call(f=file):
            file = ut.folder + '/' + f
    
            if not os.path.exists(file):
                return
    
            with open(file, 'r') as x:
                script = x.read()
    
            for k, v in words.items():
                script = script.replace(k, v)
    
            with open(file, 'w') as x:
                x.write(script)
            
            children = self.root_widget.get_children()
            for child in children:
                child.delete()
            self._refresh(self._pos, self._size)
    
            _ba.screenmessage(ut.Lstr(value='Window.PluginPorted'), (0.0, 1.0, 0.0))
            ba.playsound(ba.getsound('ding'))

        ConfirmWindow(action=call, width=360.0+80, height=100.0+40,
            text=ut.Lstr(value='Window.PluginConfirm'))

    def _back(self) -> None:
        ba.containerwidget(edit=self.root_widget, transition='out_scale')

def new_message(msg, **kwargs):
    call(msg, **kwargs)
    
    if msg.lower() == ut.msg:
        ut.open_bs17_window()

# ba_meta export plugin
class Port17(ba.Plugin):
    def on_app_running(self):
        globals()['call'] = _ba.chatmessage
        _ba.chatmessage = new_message
        _ba.set_party_icon_always_visible(True)
        ba.timer(1.5, ut.found_plugins)
        