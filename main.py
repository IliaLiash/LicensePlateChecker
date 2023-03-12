from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.uix.list import TwoLineListItem
from paddle_test import put_boxes_opencv
from kivymd.uix.menu import MDDropdownMenu
from db_request import get_plate_status
from kivy.uix.textinput import TextInput

KV = '''
ScreenManager:
    id: screen_manager

    MainScreen:
    HistoryList:
    Notes:
    Search:
    DetectedImage:

<MainScreen>:
    name: 'main_screen'
    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: f'Test Checker'
            # left_action_items: [["menu", lambda x: print('Entering menu')]]

        MDBottomNavigation:
            id: bottom_nav
            MDBottomNavigationItem:
                name: 'camera'
                text: 'Camera'
                icon: 'camera-metering-center'
                on_tab_press: print('Entering Camera')         

                MDScreen:
                    MDBoxLayout:
                        orientation: 'vertical'
                        md_bg_color: [.119, .136, .153, 1]                            
                        # Camera:
                        #     id: camera
                        #     resolution: (1280, 720)
                        #     allow_stretch: True
                        #     keep_ratio: True
                        #     play: True
                        # ToggleButton:
                        #     text: 'Play'
                        #     size_hint_y: None
                        #     height: '48dp'
                        #     size_hint_y: None
                        #     on_press: camera.play = not camera.play
                        #     # on_press: app.capture()
                        ToggleButton:
                            text: 'Capture'
                            size_hint_y: None
                            height: '48dp'
                            on_press: app.capture()                    
            
            
            MDBottomNavigationItem:
                name: 'detection'
                text: 'Detection'
                icon: 'text-recognition'
                # on_tab_press: print('Detected image')     

                DetectedImage:
                    FitImage:
                        id: detected_image
                        source: './result.jpg'
                        
                MDRaisedButton:
                    text: 'PROCEED'
                    on_press: app.change_screen_item('search') 
                    pos_hint: {'center_x': .93, 'center_y': .1}  
                            
                MDRaisedButton:
                    text: 'BACK TO CAPTURE'
                    on_press: app.change_screen_item('camera') 
                    pos_hint: {'center_x': .1, 'center_y': .1}                     
            
            MDBottomNavigationItem:
                name: 'search'
                text: 'Search'
                icon: 'car-search'

                Search:
                    id: 'search'
                    name: 'search' 
                
                    # FitImage:
                    #     source: "result.jpg"
                    #     # size_hint_y: .35
                    #     # pos_hint: {"top": 1}
                    #     size_hint: 1, 1
                    #     size: root.size

                    MDBoxLayout:
                        orientation: "vertical"
                        pos_hint: {'center_y':0.5}
                        adaptive_height: True
                        spacing: 20  
                        padding: 20              

                        MDRaisedButton:
                            text: 'NEW CAPTURE'
                            on_press: app.change_screen_item('camera')      
                            pos_hint: {'center_x': .5, 'center_y': .75}  

                        MDTextField:
                            id: plate_label_label
                            hint_text: "Enter the vehicle plate number..."
                            helper_text: "You can put the plate number manually or capture it"
                            helper_text_mode: "on_focus"
                            pos_hint: {'center_x': .5, 'center_y': .5}
                            color_mode: 'accent'
                            halign: 'center'
                            size_hint_x: None
                            width: 300                            

                        MDRaisedButton:
                            id: select_recognition_button
                            text: 'SELECT DETECTION'
                            pos_hint: {'center_x': .5, 'center_y': .5}
                            md_bg_color: [0.255, 0.209, 0.82, 1]
                            on_release: app.menu.open() if app.menu else app.create_fake_menu()

                        MDRaisedButton:
                            text: 'CHECK NUMBER'
                            on_press: app.check_plate_number()
                            pos_hint: {'center_x': .5, 'center_y': .5}  
                            
                        FitImage:
                            id: result_png
                            size_hint: None, None
                            pos_hint: {'center_x': .5}  
                            source: ''
                        
                        MDLabel:
                            id: result_label
                            text: ''
                            halign: "center"
                            
                                                    
                    # MDRaisedButton:
                    #     id: plate_hide_button
                    #     text: 'Hide plate'
                    #     pos_hint: {'center_x': .75, 'center_y': .75}  
                    #     on_release: app.clear_image()
            
            MDBottomNavigationItem:
                name: 'history_nav'
                text: 'History'
                icon: 'history'
                on_tab_press: app.call_history_list()

                HistoryList:
                    name: 'history'
                    
                    ScrollView:
                        MDList:
                            id: container
                            theme_text_color: "Custom"

            MDBottomNavigationItem:
                name: 'notes'
                text: 'Notes'
                icon: 'note-text-outline'
                on_tab_press: app.pre_fill_notes()      
                
                MDBoxLayout:
                    orientation: "vertical"
                    pos_hint: {'center_y':0.5}
                    # adaptive_height: True
                    spacing: 20
                    padding: 20     
                               
                    TextInput:
                        id: notes_input
                        hint_text:'Enter text'
                        pos_hint: {'center_x': .5, 'center_y': .5}
                        size_hint: 0.95, 0.5
                        # on_text: app.process()  
                        
                    MDRaisedButton:
                        text: 'SAVE'                       
                        pos_hint: {'center_x': .5, 'center_y': .5} 
                        md_bg_color: [0.255, 0.209, 0.82, 1]
                        on_release: app.write_notes()   
                        halign: 'center'
                        size_hint_x: None
'''


class MainScreen(Screen):
    pass


class HistoryList(Screen):
    pass


class Notes(Screen):
    pass


class Search(Screen):
    pass


class DetectedImage(Screen):
    pass


class TestChecker(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu = None
        self.plate_number = None

    def build(self):
        self.root = Builder.load_string(KV)
        # self.root.get_screen('main_screen').ids.select_recognition_button.md_bg_color = [1, 1, 1, 1]
        return Builder.load_string(KV)

    def call_history_list(self):
        with open('history.csv', 'r') as csv:
            lines = csv.readlines()
            for index, line in reversed(list(enumerate(lines, start=1))):
                line = line.split(',')
                plate_number = line[0]
                plate_status = line[1].strip()
                text_color = [.2, .4, .6, 1]

                if len(plate_number) == 7:
                    text = '{}. {}-{}-{}'.format(index, plate_number[:2], plate_number[2:5], plate_number[5:])
                elif len(plate_number) == 8:
                    text = '{}. {}-{}-{}'.format(index, plate_number[:3], plate_number[3:5], plate_number[5:])
                else:
                    text = f'{index}. {plate_number}'

                self.root.get_screen('main_screen').ids.container.add_widget(
                    TwoLineListItem(text=text,
                                    secondary_text=plate_status,
                                    text_color=text_color),
                )
                self.root.get_screen('main_screen').ids.container.add_widget(
                    TextInput(font_size=15,
                              size_hint_y=None,
                              height=30)
                )

    @staticmethod
    def write_history_log(license_plate_number, status):
        if status != 'Incorrect License number':
            with open('history.csv', 'a', encoding='utf-8') as csv:
                csv.write(f"{license_plate_number}, {status}\n")

    def pre_fill_notes(self):
        hint_text = ''

        with open('notes.csv', 'r') as csv:
            lines = csv.readlines()

            for line in lines:
                hint_text += line

        self.root.get_screen('main_screen').ids.notes_input.text = hint_text
        self.root.get_screen('main_screen').ids.notes_input.cursor = (0, 0)

    def write_notes(self):
        notes_text = self.root.get_screen('main_screen').ids.notes_input.text
        with open('notes.csv', 'w', encoding='utf-8') as csv:
            csv.write(f"{notes_text}")

    def check_plate_number(self):
        self.plate_number = self.root.get_screen('main_screen').ids.plate_label_label.text
        res = get_plate_status(self.plate_number)
        if not res:
            self.root.get_screen('main_screen').ids.result_label.text = 'Not Valid'
            self.root.get_screen('main_screen').ids.result_png.source = 'status_bad.png'
        elif res == 'Incorrect License number':
            self.root.get_screen('main_screen').ids.result_label.text = 'Incorrect License number'
            self.root.get_screen('main_screen').ids.result_png.source = 'question_face.png'
        elif isinstance(res[0], str) and 'recycle' in res:
            self.root.get_screen('main_screen').ids.result_label.text = res
            self.root.get_screen('main_screen').ids.result_png.source = 'status_bad.png'
        elif res:
            self.root.get_screen('main_screen').ids.result_label.text = f'{res[1]}. Valid, till {res[0]}'
            self.root.get_screen('main_screen').ids.result_png.source = 'status_ok.png'
        else:
            self.root.get_screen('main_screen').ids.result_label.text = str(res)
        self.root.get_screen('main_screen').ids.result_png.reload()
        self.write_history_log(str(self.plate_number), str(self.root.get_screen('main_screen').ids.result_label.text))

    def change_screen_item(self, nav_item):
        s = self.root.get_screen('main_screen')
        s.ids.bottom_nav.switch_tab(nav_item)
        self.root.current = 'main_screen'

    def get_plate_number(self):
        recognition_result = put_boxes_opencv(img="./plates/close.jpg")
        filtered_result = [res for res in recognition_result if len(res) >= 7]
        filtered_result = [''.join(filter(str.isdigit, license_number)) for license_number in filtered_result]

        if len(filtered_result) > 0:
            menu_items = [
                {
                    "viewclass": "OneLineListItem",
                    # "icon": "git",
                    "height": dp(56),
                    "text": f"{filtered_result[i]}",
                    "on_release": lambda x=f"{filtered_result[i]}": self.set_item(x),
                } for i in range(len(filtered_result))]

            self.menu = MDDropdownMenu(
                caller=self.root.get_screen('main_screen').ids.select_recognition_button,
                items=menu_items,
                position="bottom",
                width_mult=4,
            )

        self.plate_number = ', '.join(filtered_result) if filtered_result else 'Plate number not detected'
        self.root.get_screen('main_screen').ids.plate_label_label.text = self.plate_number
        self.root.get_screen('main_screen').ids.detected_image.reload()

    def set_item(self, text__item):
        self.root.get_screen('main_screen').ids.plate_label_label.text = text__item
        self.menu.dismiss()

    def create_fake_menu(self):
        try:
            self.get_plate_number()
        except:
            menu_items = [
                {
                    "viewclass": "OneLineListItem",
                    # "icon": "git",
                    "height": dp(40),
                    "text": f"No captured data"
                }]

            self.menu = MDDropdownMenu(
                caller=self.root.get_screen('main_screen').ids.select_recognition_button,
                items=menu_items,
                position="bottom",
                width_mult=4,
            )

    def clear_image(self):
        if self.root.get_screen('main_screen').ids.img.source == '':
            self.root.get_screen('main_screen').ids.plate_hide_button.text = 'Hide results'
            self.root.get_screen('main_screen').ids.img.source = './result.jpg'
        else:
            self.root.get_screen('main_screen').ids.img.source = ''
            self.root.get_screen('main_screen').ids.plate_hide_button.text = 'Show results'
            self.root.get_screen('main_screen').ids.img.reload()

    def capture(self):
        camera = self.root.get_screen('main_screen').ids['camera']
        camera.export_to_png("temp_plate.png")
        self.get_plate_number()
        self.change_screen_item('detection')


if __name__ == "__main__":
    TestChecker().run()
