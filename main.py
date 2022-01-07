from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from kivymd.uix import button
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineAvatarListItem
from kivy.uix.popup import Popup
from kivy.properties import StringProperty 
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.camera import Camera
from kivy.core.window import Window
from kivy.lang import Builder
from os import mkdir, chdir, startfile, getcwd, listdir, remove
from time import sleep
from qrcode import make
from shutil import copy2
#from cv2 import QRCodeDetector
#from cv2 import imread
from pyzbar.pyzbar import decode
import cv2
import numpy as np
from datetime import date, datetime



code='''
ScreenManager:
	ConvertScreen:
    SaveScreen:
    ScanScreen:
    Save2Screen:
    SavedScreen:
    AboutScreen:

<ConvertScreen>:
	
	name:'conv'
    link:link
	
	MDNavigationLayout:

		ScreenManager:
			Screen:

                MDGridLayout:
                    cols:1

                    MDToolbar:
                        title: "QRGen"
                        elevation: 10
                        left_action_items: [['menu', lambda x: nav_drawer.set_state('toggle')]]
                    
                    MDBoxLayout:
                        orientation: 'vertical'

                        Widget:
                        
                        MDTextField:
                            id:link
                            hint_text:"Link to be Converted in QR Code"
                            size_hint: (0.8,0)
                            pos_hint:{'center_x':0.5, 'center_y':0.5}
                            multiline:False
                            on_text_validate: root.gen()

                    MDFloatLayout:

                        MDBoxLayout:
                            orientation: 'horizontal'
                            pos_hint: {'x':0.28, 'top':1.5}
                            spacing: 25
                            padding: 15

                            MDRectangleFlatButton:
                                text: "Convert"
                                on_release: root.gen()

                            MDRectangleFlatButton:
                                text: "Show"
                                on_release: root.show()

                            MDRectangleFlatButton:
                                text: "Save"
                                on_release: 
                                    app.root.current = 'save'
                                    root.manager.transition.direction = 'left'

        MDNavigationDrawer:
            id: nav_drawer
            MDBoxLayout:
                orientation: 'vertical'
                spacing: 25
                padding: 30

                Widget:

                MDFlatButton:
                    text: "Convert"

                MDRaisedButton:
                    text: "Scan"
                    on_release:
                        app.root.current = 'scan'
                        root.manager.transition.direction = 'up'

                MDRaisedButton:
                    text: "Saved"
                    on_release:
                        app.root.current = 'saved'
                        root.manager.transition.direction = 'up'

                MDRaisedButton:
                    text: "About"

                Widget:
                

<SaveScreen>:

    name:'save'
    nm:nm

    MDNavigationLayout:

        ScreenManager:
			Screen:

                MDGridLayout:
                    cols:1

                    MDToolbar:
                        title: "QRGen"
                        elevation: 10
                        left_action_items: [['menu', lambda x: nav_drawer.set_state('toggle')]]

                    MDBoxLayout:
                        orientation: 'vertical'

                        Widget:
                            
                        MDTextField:
                            id: nm
                            hint_text:"Give Name to Your QR Code"
                            size_hint: (0.8,0)
                            pos_hint:{'center_x':0.5, 'center_y':0.5}
                            multiline:False
                            on_text_validate: root.save()

                    MDBoxLayout:
                        orientation: 'vertical'

                        MDRectangleFlatButton:
                            text: "Save"
                            pos_hint:{'center_x':0.5, 'center_y':0.5}
                            on_release: root.save()

                        Widget:

                        MDIconButton:
                            icon: 'arrow-left-thick'
                            on_release: 
                                app.root.current = 'conv'
                                root.manager.transition.direction = 'right'

        MDNavigationDrawer:
            id: nav_drawer

            MDBoxLayout:
                orientation: 'vertical'
                spacing: 25
                padding: 30

                Widget:

                MDRaisedButton:
                    text: "Convert"
                    on_release:
                        app.root.current = 'conv'
                        root.manager.transition.direction = 'right'

                MDRaisedButton:
                    text: "Scan"
                    on_release:
                        app.root.current = 'scan'
                        root.manager.transition.direction = 'right'

                MDRaisedButton:
                    text: "Saved"
                    on_release:
                        app.root.current = 'saved'
                        root.manager.transition.direction = 'right'

                MDRaisedButton:
                    text: "About"

                Widget:

<ScanScreen>:

    name:'scan'

    MDNavigationLayout:

        ScreenManager:
			Screen:

                MDGridLayout:
                    cols:1

                    MDToolbar:
                        title: "QRGen"
                        elevation: 10
                        left_action_items: [['menu', lambda x: nav_drawer.set_state('toggle')]]

                    Widget:

                    MDBoxLayout:
                        orientation: 'vertical'
                        spacing: 15

                        MDRectangleFlatButton:
                            text: "Scan"
                            pos_hint:{'center_x':0.5}
                            on_release: root.scan()

                        MDRectangleFlatButton:
                            text: "Show"
                            pos_hint:{'center_x':0.5}
                            on_release: root.show()

                        MDRectangleFlatButton:
                            text: "Save"
                            pos_hint:{'center_x':0.5}
                            on_release: 
                                app.root.current = 'save2'
                                root.manager.transition.direction = 'left'

                    Widget:

        MDNavigationDrawer:
            id: nav_drawer

            MDBoxLayout:
                orientation: 'vertical'
                spacing: 25
                padding: 30

                Widget:

                MDRaisedButton:
                    text: "Convert"
                    on_release:
                        app.root.current = 'conv'
                        root.manager.transition.direction = 'down'

                MDFlatButton:
                    text: "Scan"

                MDRaisedButton:
                    text: "Saved"
                    on_release:
                        app.root.current = 'saved'
                        root.manager.transition.direction = 'up'

                MDRaisedButton:
                    text: "About"

                Widget:

<Save2Screen>:

    name:'save2'

    nm:nm

    MDNavigationLayout:

        ScreenManager:
			Screen:

                MDGridLayout:
                    cols:1

                    MDToolbar:
                        title: "QRGen"
                        elevation: 10
                        left_action_items: [['menu', lambda x: nav_drawer.set_state('toggle')]]

                    MDBoxLayout:
                        orientation: 'vertical'

                        Widget:
                            
                        MDTextField:
                            id: nm
                            hint_text:"Give Name to Your Links File"
                            size_hint: (0.8,0)
                            pos_hint:{'center_x':0.5, 'center_y':0.5}
                            multiline:False
                            on_text_validate: root.save2()

                    MDBoxLayout:
                        orientation: 'vertical'

                        MDRectangleFlatButton:
                            text: "Save"
                            pos_hint:{'center_x':0.5, 'center_y':0.5}
                            on_release: root.save2()

                        Widget:

                        MDIconButton:
                            icon: 'arrow-left-thick'
                            on_release: 
                                app.root.current = 'scan'
                                root.manager.transition.direction = 'right'

        MDNavigationDrawer:
            id: nav_drawer

            MDBoxLayout:
                orientation: 'vertical'
                spacing: 25
                padding: 30

                Widget:

                MDRaisedButton:
                    text: "Convert"
                    on_release:
                        app.root.current = 'conv'
                        root.manager.transition.direction = 'right'

                MDRaisedButton:
                    text: "Scan"
                    on_release:
                        app.root.current = 'scan'
                        root.manager.transition.direction = 'right'

                MDRaisedButton:
                    text: "Saved"
                    on_release:
                        app.root.current = 'saved'
                        root.manager.transition.direction = 'right'

                MDRaisedButton:
                    text: "About"

                Widget:

<SavedScreen>:

    name:'saved'

    MDNavigationLayout:

        ScreenManager:
			Screen:

                MDGridLayout:
                    cols:1

                    MDToolbar:
                        title: "QRGen"
                        elevation: 10
                        left_action_items: [['menu', lambda x: nav_drawer.set_state('toggle')]]

                    Widget:

                    MDBoxLayout:
                        orientation: 'vertical'
                        spacing: 15

                        MDRectangleFlatButton:
                            text: "QR Codes"
                            pos_hint:{'center_x':0.5}
                            on_release: root.scan()

                        MDRectangleFlatButton:
                            text: "Links"
                            pos_hint:{'center_x':0.5}
                            on_release: root.show()

                    Widget:

        MDNavigationDrawer:
            id: nav_drawer

            MDBoxLayout:
                orientation: 'vertical'
                spacing: 25
                padding: 30

                Widget:

                MDRaisedButton:
                    text: "Convert"
                    on_release:
                        app.root.current = 'conv'
                        root.manager.transition.direction = 'down'

                MDRaisedButton:
                    text: "Scan"
                    on_release:
                        app.root.current = 'scan'
                        root.manager.transition.direction = 'down'

                MDFlatButton:
                    text: "Saved"

                MDRaisedButton:
                    text: "About"

                Widget:


'''
page = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <center><h1 style="background-color: blue;"><b>Scanned Links</b></h1></center>
    <p>
        <center style="background-color: yellow; padding: 1%; font-size: large;">
           {}
        </center>
    </p>
</body>
</html>
'''

class ConvertScreen(Screen):
    
    def gen(self):

        if 'temp' not in listdir():
            mkdir('temp')
        elif 'qrcode' not in listdir('temp'):
            mkdir('temp/qrcode')
        elif 'qrcode.png' in listdir('temp/qrcode'):
            remove('temp/qrcode/qrcode.png')
        if len(self.link.text) > 0:
            make(self.link.text).save('temp/qrcode/qrcode.png')
        self.link.text = ""

    def show(self):

        if 'temp' not in listdir():
            mkdir('temp')
        elif 'qrcode' not in listdir('temp'):
            mkdir('temp/qrcode')
        elif 'qrcode.png' not in listdir('temp/qrcode'):
            dialog = MDDialog (
                    title = 'Error',
                    text = 'No QR Code Found'
                )
            dialog.open()
        else:
            pop = Popup( title = 'Last Link Converted to QR Code',
            content = Image(source = 'temp/qrcode/qrcode.png'),
            size_hint = (0.7,0.7))
            pop.open()

class SaveScreen(Screen):

        def save(self):

            if 'Saved' not in listdir():
                mkdir('Saved')
            elif 'qrcodes' not in listdir('Saved'):
                mkdir('Saved/qrcodes')
            elif len(self.nm.text) > 0:
                if (self.nm.text+'.png') in listdir('Saved/qrcodes'):
                    dialog = MDDialog (
                            title = 'Error',
                            text = 'QR Code Name Already Taken'
                        )
                    dialog.open()
                else:
                    try:
                        copy2('temp/qrcode/qrcode.png', f'Saved/qrcodes/{self.nm.text}.png')
                        remove('temp/qrcode/qrcode.png')
                        self.nm.text = ""
                        dialog = MDDialog (
                            title = 'Saved',
                            text = 'QR Code Saved Successfully'
                        )
                        dialog.open()
                    except:
                        dialog = MDDialog (
                            title = 'Error',
                            text = 'No QR Code Found'
                        )
                        dialog.open()
            else:
                dialog = MDDialog (
                        title = 'Error',
                        text = 'Give Name to QR Code'
                    )
                dialog.open()
            

class ScanScreen(Screen):

    global mySet
    mySet = set()
    
    def scan(self):

        self.layout = MDBoxLayout( orientation = 'vertical', spacing = 15, padding = 10)

        self.image2 = Image()
        closeButton = MDRaisedButton( text = 'Close', pos_hint = {'center_x':0.5, 'center_y':0.5} )
        
        self.layout.add_widget( self.image2 )
        self.layout.add_widget( closeButton )

        self.pop = Popup( title = 'Scan the QR Code',
        content = self.layout,
        size_hint = (0.9,0.9),
        auto_dismiss = False)
        self.pop.open()

        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.cap.set(3,640)
        self.cap.set(4,480)
        Clock.schedule_interval(self.load_video, 1.0/30.0)

        closeButton.bind( on_press = self.end )

    def load_video(self, *args):

        ret, frame = self.cap.read()

        self.image_frame = frame
        for barcode in decode(frame):
            myData = barcode.data.decode('utf-8')
            pts = np.array([barcode.polygon], np.int32)
            pts = pts.reshape((-1,1,2))
            cv2.polylines(frame, [pts], True, (0,0,255), 2)
            pts2 = barcode.rect
            cv2.putText(frame, myData, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,0,255), 2)
            cv2.waitKey(1)
            mySet.add(myData)

        buffer = cv2.flip(frame, 0).tostring()
        texture = Texture.create(size = (frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
        self.image2.texture = texture

    def end(self, *args):

        Clock.unschedule(self.load_video)
        self.cap.release()
        cv2.destroyAllWindows()
        self.pop.dismiss()
        months = ['January','February','March','April','May','June','July','August','September','October','November','December']
        content = ''
        if len(mySet) > 0:
            for i in mySet:
                content += f'<br><a href="{i}" target="_blank">{i}</a></br>'
        else:
            content += "<br>No link(s) have been scanned</br>"
        content += f'<br>Scanned on {months[date.today().month - 1]} {date.today().day}, {date.today().year} at {datetime.now().hour}:{datetime.now().minute}:{datetime.now().second} by using <b>QRGen Application</b></br>'
        
        if 'temp' not in listdir():
            mkdir('temp')
        elif 'link' not in listdir('temp'):
            mkdir('temp/link')

        with open("temp/link/temp.html", "w") as file:
            file.write(page.format(content))

    def show(self):
        if 'temp' not in listdir():
            mkdir('temp')
        elif 'link' not in listdir('temp'):
            mkdir('temp/link')
        elif 'temp.html' not in listdir('temp/link'):
            dialog = MDDialog (
                    title = 'Error',
                    text = 'No Links File Found'
                )
            dialog.open()
        else:
            startfile(getcwd() + r"\temp\link\temp.html")

class Save2Screen(Screen):
    
    def save2(self):
            if 'Saved' not in listdir():
                mkdir('Saved')
            elif 'links' not in listdir('Saved'):
                mkdir('Saved/links')
            elif len(self.nm.text) > 0:
                if (self.nm.text+'.html') in listdir('Saved/links'):
                    dialog = MDDialog (
                            title = 'Error',
                            text = 'File Name Already Taken'
                        )
                    dialog.open()
                else:
                    try:
                        copy2('temp/link/temp.html', f'Saved/links/{self.nm.text}.html')
                        remove('temp/link/temp.html')
                        self.nm.text = ""
                        dialog = MDDialog (
                            title = 'Saved',
                            text = 'Links File Saved Successfully'
                        )
                        dialog.open()
                    except Exception as e:
                        print(e)
                        dialog = MDDialog (
                            title = 'Error',
                            text = 'No Links File Found'
                        )
                        dialog.open()
            else:
                dialog = MDDialog (
                        title = 'Error',
                        text = 'Give Name to Links File'
                    )
                dialog.open()


class SavedScreen(Screen):
    pass

class AboutScreen(Screen):
    pass
            
sm = ScreenManager()
sm.add_widget(ConvertScreen(name = 'conv'))
sm.add_widget(SaveScreen(name = 'save'))
sm.add_widget(ScanScreen(name = 'scan'))
sm.add_widget(Save2Screen(name = 'save2'))
sm.add_widget(SavedScreen(name = 'saved'))
sm.add_widget(AboutScreen(name = 'about'))


class QRGenApp(MDApp):

	def build(self):
		self.theme_cls = ThemeManager()
		#self.icon="a_icon.png"
		self.theme_cls.primary_palette='DeepPurple'
		self.theme_cls.primary_hue='900'
		self.screen=Builder.load_string(code)
		return self.screen

QRGenApp().run()