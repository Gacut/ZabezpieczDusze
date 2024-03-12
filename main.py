from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, InstructionGroup, Line
from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout

class NoteWidget(BoxLayout):
    def __init__(self, note_text, **kwargs):
        super(NoteWidget, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = 150
        self.padding = [30, 20]   # Odstęp widżetu notatek 30px od boków oraz 5px od kolejnego wpisu
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

        layout = BoxLayout(orientation='vertical', spacing=5, padding=[0, 20, 0, 0])  # Ustawiamy margines górny na 20 pikseli

        self.notes_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        self.notes_layout.bind(minimum_height=self.notes_layout.setter('height'))
        for i in range(6):
            note = NoteWidget(note_text=f'Notatka tekstowa {i+1}')
            self.notes_layout.add_widget(note)

        scroll_view = ScrollView()
        scroll_view.add_widget(self.notes_layout)

        bottom_buttons_layout = BoxLayout(size_hint=(1, None), height=50, spacing=5)
        menu_button = Button(size_hint=(None, None), size=(91, 79), background_normal='grafiki/menu.png', background_down='grafiki/menu2.png')
        bottom_buttons_layout.add_widget(menu_button)

        # zdefiniowanie napisu "Zabezpiecz Duszę" wraz z wycentrowaniem go
        anchor_layout = AnchorLayout(anchor_x='center')
        anchor_layout.add_widget(Label(text='Zabezpiecz Duszę'))
        bottom_buttons_layout.add_widget(anchor_layout)

        add_button = Button(size_hint=(None, None), size=(91, 79), pos_hint={'right': 1}, background_normal='grafiki/dodaj.png', background_down='grafiki/dodaj2.png')
        bottom_buttons_layout.add_widget(add_button)

        layout.add_widget(scroll_view)
        layout.add_widget(bottom_buttons_layout)

        self.add_widget(layout)

        menu_button.bind(on_press=self.show_menu_popup)
        add_button.bind(on_press=self.show_add_popup)

    def show_menu_popup(self, instance):
        content = BoxLayout(orientation='vertical')
        button1 = Button(text='Przycisk 1', size_hint_y=None, height=50)
        button2 = Button(text='Przycisk 2', size_hint_y=None, height=50)
        button3 = Button(text='Przycisk 3', size_hint_y=None, height=50)
        close_button = Button(text='Zamknij', size_hint_y=None, height=50)

        content.add_widget(button1)
        content.add_widget(button2)
        content.add_widget(button3)
        content.add_widget(close_button)

        popup = Popup(title='Menu', content=content, size_hint=(None, None), size=(300, 200))
        close_button.bind(on_press=popup.dismiss)
        popup.open()

    def show_add_popup(self, instance):
        content = BoxLayout(orientation='vertical')
        add_text_button = Button(text='Dodaj notatkę tekstową', size_hint_y=None, height=50)
        add_text_button.bind(on_press=self.add_note_and_close_popup)
        add_video_button = Button(text='Dodaj notatkę wideo', size_hint_y=None, height=50)
        close_button = Button(text='Zamknij', size_hint_y=None, height=50)

        # Dodajemy akcje przycisku "Dodaj notatkę tekstową"
        add_text_button.bind(on_press=self.show_add_note_screen)

        content.add_widget(add_text_button)
        content.add_widget(add_video_button)
        content.add_widget(close_button)

        popup = Popup(title='Dodaj', content=content, size_hint=(None, None), size=(300, 200))
        close_button.bind(on_press=popup.dismiss)
        popup.open()

    def add_note_and_close_popup(self, instance):
        self.show_add_note_screen(instance)
        # Znajdź popup "show_add_popup" i zamknij go
        for widget in instance.walk_reverse():
            if isinstance(widget, Popup):
                widget.dismiss()
                break

    def show_add_note_screen(self, instance):
        self.manager.current = 'add_note'


#Ekran wprowadzania notateek tekstowych
class AddNoteScreen(Screen):
    def __init__(self, **kwargs):
        super(AddNoteScreen, self).__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=1)

        bottom_buttons_layout_text = BoxLayout(size_hint=(1, None), height=70, spacing=5)


        title_label = Label(text='Tytuł notatki:', size_hint_x=None, width=100, size_hint_y=None, height=30)
        self.title_input = TextInput(size_hint_y=None, height=30, size_hint_x=None, width=Window.width / 4)

        content_label = Label(text='Treść notatki:', size_hint_x=None, width=100, size_hint_y=None, height=30)
        self.content_input = TextInput()

        # Przycisk "Dodaj" ustawiony na prawej stronie na dole
        self.add_button = Button(text='Dodaj', size_hint=(None, None), size=(100, 50), pos_hint={'right': 1})
        self.add_button.bind(on_press=self.add_note)

        # Przycisk "Wróć" ustawiony na lewej stronie na dole
        back_button = Button(text='Wróć', size_hint=(None, None), size=(100, 50), pos_hint={'left': 1})
        back_button.bind(on_press=self.go_back)

        layout.add_widget(title_label)
        layout.add_widget(self.title_input)
        layout.add_widget(content_label)
        layout.add_widget(self.content_input)
        layout.add_widget(bottom_buttons_layout_text)

        # Dodanie przycisków "Wróć" oraz "Dodaj" na dole ekranu
        bottom_buttons_layout_text.add_widget(back_button)
        anchor_layout_text = AnchorLayout(anchor_x='center')
        bottom_buttons_layout_text.add_widget(anchor_layout_text) # Kolejny pusty widget żeby zrobić odstęp między przyciskami
        bottom_buttons_layout_text.add_widget(self.add_button)

        
        self.add_text_color_background()
        self.add_widget(layout)

        
    def add_text_color_background(self):
        with self.canvas.before:
            Color(0.027, 0.082, 0.137, 1)  # #071522
            Rectangle(pos=self.pos, size=Window.size)

    def add_note(self, instance):
        title = self.title_input.text
        content = self.content_input.text
        if title.strip() == '' or content.strip() == '':
            popup = Popup(title='Błąd', content=Label(text='Tytuł i treść notatki nie mogą być puste.'),
                          size_hint=(None, None), size=(300, 200))
            popup.open()
        else:
            # Tutaj możesz umieścić kod do zapisu notatki, np. do bazy danych
            self.title_input.text = ''
            self.content_input.text = ''
            popup = Popup(title='Sukces', content=Label(text='Notatka została dodana.'),
                          size_hint=(None, None), size=(300, 200))
            popup.open()

    def go_back(self, instance):
        # Przechodzimy z powrotem do ekranu "MainScreen"
        self.manager.current = 'main'


class NoteApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(AddNoteScreen(name='add_note'))

        # Dynamiczne aktualizowanie rozmiaru tła
        def update_background(instance, value):
            with sm.get_screen('main').canvas.before:
                sm.get_screen('main').background.size = value
        Window.bind(size=update_background)

        with sm.get_screen('main').canvas.before:
            Color(0x07 / 255, 0x15 / 255, 0x22 / 255)
            sm.get_screen('main').background = Rectangle(size=Window.size, pos=(0, 0))

        return sm

if __name__ == '__main__':
    NoteApp().run()
