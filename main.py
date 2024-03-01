from kivymd.app import MDApp
from kivymd.uix.label import MDLabel

class ZabezpieczDusze(MDApp):
    def build(self):
        
        return MDLabel(text="Witaj 100commitów!", halign="center")
    

ZabezpieczDusze().run()