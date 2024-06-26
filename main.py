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
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp
from kivy.uix.filechooser import FileChooserIconView
from shutil import copyfile
from kivy.uix.image import Image
from kivy.uix.spinner import Spinner
# import threading
# import sounddevice as sd
# import numpy as np
import json
import os


layout = GridLayout(cols=1, spacing=dp(10), padding=[dp(10), dp(20)])  # Ustawiamy margines górny na 20 pikseli

def create_empty_json(file_name):
    # Ustawia ścieżkę pliku taką samą, w jakiej znajduje się aplikacja
    app_folder = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(app_folder, file_name)

    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            json.dump([], file)

def load_notes_from_json(file_path):
    notes = []
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            try:
                notes_data = json.load(file)
            except json.decoder.JSONDecodeError:
                notes_data = []
        for note in notes_data:
            notes.append(note)
    return notes

def clear_main_screen():
    main_screen = App.get_running_app().root.get_screen('main')
    main_screen.notes_layout.clear_widgets()

def update_main_screen_notes():
    clear_main_screen()
    notes = load_notes_from_json('notes.json')
    main_screen = App.get_running_app().root.get_screen('main')
    for note in notes:
        note_widget = NoteWidget(note)
        main_screen.notes_layout.add_widget(note_widget)


if not os.path.exists("notes.json'"):
    create_empty_json("notes.json")

class NoteWidget(BoxLayout):
    def __init__(self, note_data, **kwargs):
        super(NoteWidget, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = Window.height * 0.2
        self.padding = [30, 6]   
        self.note_data = note_data
        notatka = Label(text=note_data['title'])
        self.add_widget(notatka)

        if self.note_data.get('picpath') and 'grafiki' not in self.note_data.get('picpath'):
            self.add_widget(Label(text='Zdjecia', font_size='11sp'))
            
        if self.note_data.get('tag'):
            self.add_widget(Label(text=str(self.note_data.get('tag')), font_size='11sp'))

        else:
            pass

        self.bind(on_touch_down=self.on_click)

        self.bind(pos=self.update_canvas)
        self.bind(size=self.update_canvas)

        self.border = InstructionGroup()
        self.update_canvas()

    def on_click(self, instance, touch):
        if self.collide_point(*touch.pos):
            app = App.get_running_app()
            app.root.current = 'note_details'
            note_details_screen = app.root.get_screen('note_details')
            note_details_screen.display_note_details(self.note_data, self.note_data.get('picpath', None))

    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0xc2 / 255, 0xfc / 255, 0xe6 / 255)
            self.border.clear()
            # W tym miejscu jest zdefiniowana ramka wokół wpisów/notatek
            self.border.add(Line(rectangle=(self.x + self.padding[0], self.y + self.padding[1], self.width - 2 * self.padding[0], self.height - 2 * self.padding[1]), width=2))
            self.canvas.before.add(self.border)


#ekran główny
class MainScreen(Screen):
    global load_notes_from_json, layout

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.notes_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        self.notes_layout.bind(minimum_height=self.notes_layout.setter('height'))

        notes = load_notes_from_json('notes.json')
        for note in notes:
            note_widget = NoteWidget(note)
            self.notes_layout.add_widget(note_widget)

        scroll_view = ScrollView()
        scroll_view.add_widget(self.notes_layout)

        bottom_buttons_layout = BoxLayout(size_hint_max=(None, dp(0.01)), spacing=5)

        # Dodanie przycisków do bottom_buttons_layout
        menu_button = Button(size_hint=(None, None), size_hint_min=(None, None), size_hint_max=(None, None),
                            height=dp(80), width=dp(100),
                            background_normal='grafiki/menu.png', background_down='grafiki/menu2.png')
        add_button = Button(size_hint=(None, None), size_hint_min=(None, None), size_hint_max=(None, None),
                            height=dp(80), width=dp(100),
                            background_normal='grafiki/dodaj.png', background_down='grafiki/dodaj2.png')

        bottom_buttons_layout.add_widget(menu_button)
        bottom_buttons_layout.add_widget(Label())
        bottom_buttons_layout.add_widget(add_button)

        layout.add_widget(scroll_view)
        layout.add_widget(bottom_buttons_layout)

        self.add_widget(layout)

        menu_button.bind(on_release=self.show_menu_popup)
        add_button.bind(on_release=self.show_add_popup)

    def refresh_notes(self):
        # Wczytaj notatki z pliku notes.json
        with open('notes.json', 'r') as file:
            notes = json.load(file)

        # Usuń istniejące notatki z GridLayout
        self.notes_layout.clear_widgets()

        # Dodaj nowe notatki do GridLayout
        for note in notes:
            note_widget = NoteWidget(note)
            self.notes_layout.add_widget(note_widget)

    def show_menu_popup(self, instance):
        content = GridLayout(cols=1, rows=4, spacing=5)
        button1 = Button(text='Import/Export do pliku', size_hint_y=None, height=dp(50))
        button2 = Button(text='Szukaj(??)', size_hint_y=None, height=dp(50))
        button3 = Button(text='Creditsy', size_hint_y=None, height=dp(50))
        close_button = Button(size_hint=(None, None), size=(dp(80), dp(50)), background_normal='grafiki/zamknij.png', background_down='grafiki/zamknij2.png')
        close_button_bar_menu = BoxLayout(orientation='horizontal')

        content.add_widget(button1)
        content.add_widget(button2)
        content.add_widget(button3)
        close_button_bar_menu.add_widget(BoxLayout())
        close_button_bar_menu.add_widget(close_button)
        close_button_bar_menu.add_widget(BoxLayout())
        content.add_widget(close_button_bar_menu)

        popup = Popup(title='Menu', content=content, size_hint=(None, None), size=(dp(200), dp(360)))
        # popup.size_hint = (0.4, 0.7)
        close_button.bind(on_release=popup.dismiss)
        popup.open()

    def show_add_popup(self, instance):
        content = BoxLayout(orientation='vertical')
        add_text_button = Button(size_hint_y=None, height=dp(80), background_normal='grafiki/dodajnotatketext.png', background_down='grafiki/dodajnotatketext2.png')
        add_text_button.bind(on_release=self.add_note_and_close_popup)
        add_video_button = Button(size_hint_y=None, height=dp(80), background_normal='grafiki/dodajnotatkewideo.png', background_down='grafiki/dodajnotatkewideo2.png')
        add_video_button.bind(on_release=self.add_video_and_close_popup)
        add_audio_button = Button(text='Dodaj notatkę audio', size_hint_y=None, height=80)
        add_audio_button.bind(on_release=self.add_audio_and_close_popup)
        close_button = Button(size_hint=(None, None), size=(dp(80), dp(50)), background_normal='grafiki/zamknij.png', background_down='grafiki/zamknij2.png')
        close_button_bar_add = BoxLayout(orientation='horizontal')

        # Dodajemy akcje przycisku "Dodaj notatkę tekstową" oraz "Dodaj notatkę video"
        add_text_button.bind(on_release=self.show_add_note_screen)
        add_video_button.bind(on_release=self.show_add_video_screen)
        add_audio_button.bind(on_release=self.show_add_audio_screen)

        close_button_bar_add.add_widget(BoxLayout())
        close_button_bar_add.add_widget(close_button)
        close_button_bar_add.add_widget(BoxLayout())  
        content.add_widget(add_text_button)
        content.add_widget(add_video_button)
        content.add_widget(add_audio_button)
        content.add_widget(close_button_bar_add)

        popup = Popup(title="Jaką notatkę dziś chcesz dodać?", content=content, size_hint=(None, None), size=(dp(200), dp(360)))
        close_button.bind(on_release=popup.dismiss)
        popup.open()

    def add_note_and_close_popup(self, instance):
        self.show_add_note_screen(instance)
        # Znajdź popup "show_add_note_screen" i zamknij go
        for widget in instance.walk_reverse():
            if isinstance(widget, Popup):
                widget.dismiss()
                break

    def add_video_and_close_popup(self, instance):
        self.show_add_video_screen(instance)
        # Znajdź popup "show_add_video_screen" i zamknij go
        for widget in instance.walk_reverse():
            if isinstance(widget, Popup):
                widget.dismiss()
                break

    def add_audio_and_close_popup(self, instance):
        self.show_add_audio_screen(instance)
        # Znajdź popup "show_add_audio_screen" i zamknij go
        for widget in instance.walk_reverse():
            if isinstance(widget, Popup):
                widget.dismiss()
                break

    def show_add_note_screen(self, instance):
        self.manager.current = 'add_note'

    def show_add_video_screen(self, instance):
        self.manager.current = 'add_video_note'

    def show_add_audio_screen(self, instance):
        self.manager.current = 'add_audio_note'

#Ekran wprowadzania notatek tekstowych
class AddNoteScreen(Screen):
    global load_notes_from_json, notes_layout
    def __init__(self, **kwargs):
        super(AddNoteScreen, self).__init__(**kwargs)

        self.picture_folder = "pictures"
 
        if not os.path.exists(self.picture_folder):
            os.makedirs(self.picture_folder)

        options = ['Wspomnienie', 'Marzenia', 'Przeżycia', 'Opis Dnia', 'Światopogląd', 'Polityka']
        
        #layouty
        title_layout = GridLayout(cols=2, size_hint_y=dp(20))
        layout = GridLayout(cols=1, padding=[dp(10), dp(20), dp(10), dp(50)])
        bottom_buttons_layout_text = GridLayout(cols=4, size_hint_y=None, height=dp(60), spacing=dp(5))
        
        title_label = Label(text='Tytuł notatki:',size_hint_x=None, width=dp(100), size_hint_y=None, height=dp(30))
        
        self.title_input = TextInput(size_hint_y=None, height=dp(30), 
                                     size_hint_x=None, width=(Window.width - dp(220)), multiline=False)

        content_label = Label(text='Treść notatki:', size_hint_x=None, width=dp(100), size_hint_y=None, height=dp(30))
        self.content_input = TextInput(size_hint_x=None, width=(Window.width - dp(20)), size_hint_y=None, height=(Window.height - dp(250)))

        self.spinner = Spinner(text='Wybierz rodzaj notatki', values=options, size_hint=(None, None), size=(dp(200), dp(50)))
        # spinner.bind(text=self.on_spinner_select)

        # Przycisk "Dodaj" ustawiony na prawej stronie na dole
        self.add_button = Button(text='Dodaj', size_hint=(None, None), size=(dp(100), dp(50)))
        self.add_button.bind(on_release=self.add_note)

        self.picture_button = Button(text='Dołącz zdjęcie', size_hint=(None, None), size=(dp(100), dp(50)), pos_hint={'right': 1})

        # Przycisk "Wróć" ustawiony na lewej stronie na dole
        back_button = Button(text='Wróć', size_hint=(None, None), size=(dp(100), dp(50)))
        back_button.bind(on_release=self.go_back)

        # Dodanie przycisków "Wróć", "Dołącz zdjęcie" oraz "Dodaj" na dole ekranu
        bottom_buttons_layout_text.add_widget(back_button)
        anchor_layout_text = AnchorLayout(anchor_x='center')
        bottom_buttons_layout_text.add_widget(anchor_layout_text) # Kolejny pusty widget żeby zrobić odstęp między przyciskami
        bottom_buttons_layout_text.add_widget(self.picture_button)
        bottom_buttons_layout_text.add_widget(self.add_button)

        title_layout.add_widget(title_label)
        title_layout.add_widget(Label())
        title_layout.add_widget(self.title_input)
        title_layout.add_widget(Label())
        title_layout.add_widget(self.spinner)
        layout.add_widget(title_layout)
        layout.add_widget(Label())
        layout.add_widget(content_label)
        layout.add_widget(self.content_input)
        layout.add_widget(Label(size_hint_max=(None, dp(0.01))))
        layout.add_widget(bottom_buttons_layout_text)
        

        self.add_text_color_background()
        self.add_widget(layout)

        self.picture_button.bind(on_release=self.choose_picture)

    def choose_picture(self, instance):
        file_chooser = FileChooserIconView()
        file_chooser.bind(on_submit=self.copy_picture)
        popup = Popup(title="Wybierz zdjęcie", content=file_chooser, size_hint=(None, None), size=(400, 400))
        popup.open()

    def copy_picture(self, instance, file_path, touch):
        filename = os.path.basename(file_path[0])
        dest_path = os.path.join(self.picture_folder, filename)
        copyfile(file_path[0], dest_path)
        self.picture_button.text = filename
        self.picpath = dest_path
        
    def add_text_color_background(self):
        with self.canvas.before:
            Color(0.027, 0.082, 0.137, 1)  #071522
            Rectangle(pos=self.pos, size=Window.size)

    def add_note_to_json(self, file_path, title, content, tag, picpath=None):
        note = {'title': title, 'content': content,'tag': tag,  'picpath': picpath, }
        if picpath != None:
            note['picpath'] = picpath

        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                notes = json.load(file)
        else:
            notes = []
        notes.append(note)

        with open(file_path, 'w') as file:
            json.dump(notes, file)

        popup = Popup(title='Sukces', content=Label(text='Notatka została dodana.'),
                    size_hint=(None, None), size=(dp(200), dp(200)))
        self.picture_button.text = "Dołącz zdjęcie"
        popup.open()

    def add_note(self, instance):
        title = self.title_input.text
        content = self.content_input.text
        picpath = "pictures/" + str(self.picture_button.text)
        tag = self.spinner.text

        notes_file = "notes.json"
        popup_height = Window.height * 0.2
        popup_width = Window.width * 0.4

        if title.strip() == '' or content.strip() == '':
            popup = Popup(title='Błąd', content=Label(text='Tytuł i treść notatki nie mogą być puste.'),
                        size_hint=(None, None), size=(popup_width, popup_height))
            popup.open()

        if tag == 'Wybierz rodzaj notatki':
            popup = Popup(title='Błąd', content=Label(text='Musisz wybrać rodzaj notatki'),
                        size_hint=(None, None), size=(popup_width, popup_height))
            popup.open()
        
        else:
            if "Dołącz" in picpath:
                self.add_note_to_json(notes_file, title, content, tag)
            else:
                self.add_note_to_json(notes_file, title, content, tag, picpath)
            self.title_input.text = ''
            self.content_input.text = ''

    def go_back(self, instance):
        self.manager.current = 'main'
        update_main_screen_notes()

#Ekran wprowadzania notatek video
class AddVideoNoteScreen(Screen):
    def __init__(self, **kwargs):
        super(AddVideoNoteScreen, self).__init__(**kwargs)

        options = ['Wspomnienie', 'Marzenia', 'Przeżycia', 'Opis Dnia', 'Światopogląd', 'Polityka']
        
        main_layout = GridLayout(cols=1, padding=[dp(10), dp(20), dp(10), dp(50)])
        layout_video = GridLayout(cols=2)
        add_video_with_label = GridLayout(cols=2)
        bottom_buttons_layout_video = GridLayout(cols=3, size_hint_y=None, height=dp(70), spacing=dp(5))
        title_layout = GridLayout(cols=2)

        title_video_label = Label(text='Tytuł:', size_hint_x=None, width=dp(50), size_hint_y=None, height=dp(10), padding=[dp(20), dp(50), dp(20), dp(80)])
        self.spinner = Spinner(text='Wybierz rodzaj notatki', values=options, size_hint=(None, None), size=(dp(200), dp(50)))
        self.title_input = TextInput(size_hint_y=None, height=dp(30), 
                                     size_hint_x=None, width=dp(Window.width / 2), multiline=False, padding=[dp(20), dp(50), dp(20), dp(80)])
        self.add_video_button = Button(text='Dodaj Wideo', size_hint=(None, None), size=(dp(100), dp(50)))
        multimedia_label = Label(text='Ścieżka pliku wideo:', size_hint=(None, None), size=(dp(150), dp(30)))
        record_video_button = Button(text='Nagraj wideo', size_hint=(None, None), size=(dp(100), dp(50)))

        content_video_label = Label(text='Treść notatki:', width=dp(100), size_hint_y=None, height=(30))
        self.content_video_input = TextInput(size_hint_x=None, width=(Window.width - dp(20)), size_hint_y=None, height=(Window.height - dp(410)))

        self.add_multimedia_button = Button(text='Dodaj', size_hint=(None, None), size=(dp(100), dp(50)), pos_hint={'right': 1})
        self.add_multimedia_button.bind(on_release=self.add_video_note)

        back_video_button = Button(text='Wróć', size_hint=(None, None), size=(dp(100), dp(50)), pos_hint={'left': 1})
        back_video_button.bind(on_release=self.go_back)

        bottom_buttons_layout_video.add_widget(back_video_button)
        anchor_layout_text = AnchorLayout(anchor_x='center')
        bottom_buttons_layout_video.add_widget(anchor_layout_text)
        bottom_buttons_layout_video.add_widget(self.add_multimedia_button)

        add_video_with_label.add_widget(self.add_video_button)
        add_video_with_label.add_widget(multimedia_label)
        add_video_with_label.add_widget(record_video_button)
        add_video_with_label.add_widget(Label())

        title_layout.add_widget(self.title_input)
        title_layout.add_widget(Label())
        title_layout.add_widget(self.spinner)
        title_layout.add_widget(Label())
        title_layout.add_widget(add_video_with_label)

        layout_video.add_widget(title_video_label)
        layout_video.add_widget(Label())
        layout_video.add_widget(title_layout)
        layout_video.add_widget(Label())
        # layout_video.add_widget(add_video_with_label)
        # layout_video.add_widget(Label())
        layout_video.add_widget(content_video_label)
        layout_video.add_widget(Label())
        layout_video.add_widget(self.content_video_input)
        
        main_layout.add_widget(layout_video)
        main_layout.add_widget(bottom_buttons_layout_video)

        self.add_text_color_background()
        self.add_widget(main_layout)


    def add_text_color_background(self):
        with self.canvas.before:
            Color(0.027, 0.082, 0.137, 1)  # #071522
            Rectangle(pos=self.pos, size=Window.size)

    def add_note_to_json(self, file_path, title, content, tag, vidpath):
        note = {'title': title, 'content': content,'tag': tag,  'vidpath': vidpath, }
        if vidpath == None:
            popup = Popup(title='Błąd', content=Label(text='Dodaj wideo lub nagraj je. W przeciwnym wypadku skorzystaj z notatki textowej'),
                        size_hint=(None, None), size=(dp(200), dp(200)))
            popup.open()

        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                notes = json.load(file)
        else:
            notes = []
        notes.append(note)

        with open(file_path, 'w') as file:
            json.dump(notes, file)

        popup = Popup(title='Sukces', content=Label(text='Notatka została dodana.'),
                    size_hint=(None, None), size=(dp(200), dp(200)))
        self.add_video_button.text = "Dodaj Wideo"
        popup.open()

    def add_video_note(self, instance):
        title = self.title_input.text
        content = self.content_video_input.text
        popup_height = Window.height * 0.2
        popup_width = Window.width * 0.4
        vidpath = "videos/" + str(self.add_video_button.text)
        tag = self.spinner.text

        notes_file = "notes.json"
        popup_height = Window.height * 0.2
        popup_width = Window.width * 0.4

        if title.strip() == '' or content.strip() == '':
            popup = Popup(title='Błąd', content=Label(text='Tytuł i treść notatki nie mogą być puste.'),
                        size_hint=(None, None), size=(popup_width, popup_height))
            popup.open()

        if tag == 'Wybierz rodzaj notatki':
            popup = Popup(title='Błąd', content=Label(text='Musisz wybrać rodzaj notatki'),
                        size_hint=(None, None), size=(popup_width, popup_height))
            popup.open()
        
        else:
            if "Dołącz" in vidpath:
                self.add_note_to_json(notes_file, title, content, tag)
            else:
                self.add_note_to_json(notes_file, title, content, tag, vidpath)
            self.title_input.text = ''
            self.content_video_label.text = ''

    def go_back(self, instance):
        self.manager.current = 'main'
        update_main_screen_notes()

#ekran wprowadzenia notatki audio
class AddAudioScreen(Screen):
    def __init__(self, **kwargs):
        super(AddAudioScreen, self).__init__(**kwargs)

        self.is_recording = False
        self.recording_thread = None
        self.audio_data = []

        # Layouty
        bottom_buttons_layout_audio = GridLayout(cols=3, size_hint_y=None, height=dp(70), spacing=dp(5))
        title_layout = GridLayout(cols=2)
        record_buttons_layout = GridLayout(cols=4, row_default_height=3, row_force_default=True)
        layout = GridLayout(cols=1, spacing=-20, padding=[dp(10), dp(80), dp(10), dp(50)])

        add_audio_button = Button(text='Dodaj', size_hint=(None, None), size=(dp(100), dp(50)), pos_hint={'right': 1})
        back_audio_button = Button(text='Wróć', size_hint=(None, None), size=(dp(100), dp(50)), pos_hint={'left': 1})
        back_audio_button.bind(on_release=self.go_back)

        title_label = Label(text='Tytuł notatki:', size_hint=(None, None), height=dp(30))
        self.title_input = TextInput(size_hint=(0.7, None), height=dp(30), multiline=False)

        self.record_button = Button(text='Nagraj', size_hint=(1, None), size=(dp(100), dp(50)))
        # self.record_button.bind(on_release=self.start_recording)
        self.stop_button = Button(text='Zatrzymaj', size_hint=(1, None), size=(dp(100), dp(50)))
        # self.stop_button.bind(on_release=self.stop_recording)

        bottom_buttons_layout_audio.add_widget(back_audio_button)
        bottom_buttons_layout_audio.add_widget(Label(size_hint=(1, None)))
        bottom_buttons_layout_audio.add_widget(add_audio_button)

        title_layout.add_widget(title_label)
        title_layout.add_widget(self.title_input)

        record_buttons_layout.add_widget(Label())
        record_buttons_layout.add_widget(self.record_button)
        record_buttons_layout.add_widget(self.stop_button)
        record_buttons_layout.add_widget(Label())

        layout.add_widget(title_layout)
        layout.add_widget(record_buttons_layout)
        layout.add_widget(bottom_buttons_layout_audio)
        self.add_color_background()
        self.add_widget(layout)


    def add_color_background(self):
        with self.canvas.before:
            Color(0.027, 0.082, 0.137, 1)  # #071522
            Rectangle(pos=self.pos, size=Window.size)

    def go_back(self, instance):
        self.manager.current = 'main'
        update_main_screen_notes()

    #Coś nie działa. Sprawdzić jak debugger na androidzie zacznie działać
    
    # def start_recording(self, instance):
    #     if not self.is_recording:
    #         self.is_recording = True
    #         self.audio_data = []
    #         self.recording_thread = threading.Thread(target=self.record)
    #         self.recording_thread.start()

    # def record(self):
    #     with sd.InputStream(callback=self.audio_callback):
    #         while self.is_recording:
    #             sd.sleep(100)

    # def stop_recording(self, instance):
    #     if self.is_recording:
    #         self.is_recording = False
    #         self.recording_thread.join()
    #         self.save_audio()

    # def save_audio(self):
    #     audio_array = np.concatenate(self.audio_data, axis=0)

#ekran widoku notatki
class NoteDetailsScreen(Screen):
    def __init__(self, **kwargs):
        super(NoteDetailsScreen, self).__init__(**kwargs)
        delete_layout = GridLayout(cols=4, padding=[dp(40)])
        layout_main = GridLayout(cols=2, padding=[dp(40)])
        layout = GridLayout(cols=1)

        self.title_label = Label(text='', size_hint=(1, None), height=dp(50))
        self.content_scrollview = ScrollView()
        self.content_label = Label(text='', size_hint_y=None, font_size=dp(16), padding=(dp(10), dp(10)))
        self.content_label.bind(size=self.update_text_size)
        self.content_scrollview.add_widget(self.content_label)
        self.image_widget = Image(source='', size_hint=(1, 1))
        self.back_button = Button(text="Wróć", size_hint=(None, None), size=(dp(100), dp(50)))
        self.back_button.bind(on_release=self.go_back)
        self.delete_button = Button(text="Usuń", size_hint=(None, None), size=(dp(100), dp(50)))
        self.delete_button.bind(on_release=self.delete_note)

        layout.add_widget(Label(size_hint=(0.01, 0.20)))
        layout.add_widget(self.title_label)
        layout.add_widget(self.content_scrollview)
        layout.add_widget(self.back_button)
        delete_layout.add_widget(Label())
        delete_layout.add_widget(Label())
        delete_layout.add_widget(Label())
        delete_layout.add_widget(self.delete_button)
        layout_main.add_widget(layout)
        layout_main.add_widget(self.image_widget)
        self.add_widget(delete_layout)
        self.add_widget(layout_main)
        self.add_color_background()



    def delete_note(self, instance):
            title = self.title_label.text

            with open('notes.json', 'r') as file:
                notes = json.load(file)

            for note in notes:
                if note['title'] == title:
                    notes.remove(note)
                    break

            with open('notes.json', 'w') as file:
                json.dump(notes, file)

            self.manager.current = 'main'

            self.manager.get_screen('main').refresh_notes()


    def update_text_size(self, *args):
        self.content_label.text_size = (self.content_label.width, self.content_label.height)

    def display_note_details(self, note_data, picpath=None):
        self.title_label.text = note_data['title']
        self.content_label.text = note_data['content']
        if picpath is None:
            self.image_widget.source = 'grafiki/nophoto.jpg'
        else:
            self.image_widget.source = picpath

    def add_color_background(self):
        with self.canvas.before:
            Color(0.027, 0.082, 0.137, 1)  # #071522
            Rectangle(pos=self.pos, size=Window.size)

    def go_back(self, instance):
        self.manager.current = 'main'
        update_main_screen_notes()


class NoteApp(App):
    def build(self):
        sm = ScreenManager()
        main_screen = MainScreen(name='main')
        sm.add_widget(main_screen)
        sm.add_widget(AddNoteScreen(name='add_note'))
        sm.add_widget(AddVideoNoteScreen(name='add_video_note'))
        sm.add_widget(AddAudioScreen(name='add_audio_note'))
        note_details_screen = NoteDetailsScreen(name='note_details')
        sm.add_widget(note_details_screen)

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
