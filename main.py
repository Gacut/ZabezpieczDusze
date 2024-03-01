from kivymd.app import MDApp
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivymd.uix.floatlayout import FloatLayout


class ZabezpieczDusze(MDApp):
    def build(self):
        background = Image(source='grafiki/bg1.jpg', allow_stretch=True, keep_ratio=False)
        layout = FloatLayout()
        label = Label(text="Witaj 100commitów!", color=[156, 17, 149, 1])
        label.halign="right"
        layout.add_widget(background)
        layout.add_widget(label)


        return layout
    

ZabezpieczDusze().run()
