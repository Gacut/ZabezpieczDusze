from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, InstructionGroup, Line
from kivy.app import App

class NoteWidget(BoxLayout):
    def __init__(self, note_text, **kwargs):
        super(NoteWidget, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = 150  
        self.padding = [30, 5]  # Odstęp widżetu notatek 30px od boków oraz 5px od kolejnego wpisu
        self.add_widget(Label(text=note_text))

        self.bind(pos=self.update_canvas)
        self.bind(size=self.update_canvas)

        self.border = InstructionGroup()
        self.update_canvas()

    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0xc2 / 255, 0xfc / 255, 0xe6 / 255)
            self.border.clear()
            # W tym miejscu jest zdefiniowana ramka wokół wpisów/notatek
            self.border.add(Line(rectangle=(self.x + self.padding[0], self.y + self.padding[1], self.width - 2 * self.padding[0], self.height - 2 * self.padding[1]), width=2))
            self.canvas.before.add(self.border)

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', spacing=5, padding=[0, 20, 0, 0])

        self.notes_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        self.notes_layout.bind(minimum_height=self.notes_layout.setter('height'))
        for i in range(6):
            note = NoteWidget(note_text=f'Notatka tekstowa {i+1}')
            self.notes_layout.add_widget(note)

        scroll_view = ScrollView()
        scroll_view.add_widget(self.notes_layout)

        add_button = Button(text='Dodaj', size_hint=(None, None), size=(100, 50), pos_hint={'right': 1, 'bottom': 1})
        add_button.bind(on_press=self.show_add_popup)

        layout.add_widget(scroll_view)
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
        # TODO: Ekran dodawania notatek wraz ze zdjęciem (lub sam text)
        pass

    def add_video_note(self, instance):
        # TODO: Ekran dodawania notatek wideo oraz tekstu
        pass

class NoteApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))

        with sm.get_screen('main').canvas.before:
            Color(0x07 / 255, 0x15 / 255, 0x22 / 255)
            self.background = Rectangle(size=(Window.width, Window.height), pos=(0, 0))

        return sm

if __name__ == '__main__':
    NoteApp().run()
