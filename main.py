from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.metrics import dp

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        layout = BoxLayout(orientation='vertical')
        add_button = Button(text='Dodaj', size_hint=(None, None), size=(100, 50), pos_hint={'right': 0.95, 'bottom': 0.05})
        add_button.bind(on_press=self.show_add_popup)

        layout.add_widget(add_button)

        self.add_widget(layout)

    def show_add_popup(self, instance):
        content = BoxLayout(orientation='vertical')
        add_text_button = Button(text='Dodaj notatkę tekstową', size_hint_y=None, height=50, on_press=self.add_text_note)
        add_video_button = Button(text='Dodaj notatkę wideo', size_hint_y=None, height=50, on_press=self.add_video_note)
        close_button = Button(text='Zamknij', size_hint_y=None, height=50)

        content.add_widget(add_text_button)
        content.add_widget(add_video_button)
        content.add_widget(close_button)

        popup = Popup(title='Dodaj notatkę', content=content, size_hint=(None, None), size=(300, 200))
        close_button.bind(on_press=popup.dismiss)
        popup.open()

    def add_text_note(self, instance):
        # Implementacja dodawania notatki tekstowej
        pass

    def add_video_note(self, instance):
        # Implementacja dodawania notatki wideo
        pass

class ZabezpieczDusze(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        return sm

if __name__ == '__main__':
    ZabezpieczDusze().run()
