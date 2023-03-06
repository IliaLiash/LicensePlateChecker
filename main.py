from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.metrics import dp
import random
import string
from kivymd.uix.list import ThreeLineListItem
from paddle_test import paddle_ocr_recognition_img
from kivymd.uix.menu import MDDropdownMenu


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
            left_action_items: [["menu", lambda x: print('Entering menu')]]

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
                        #     resolution: (640, 480)
                        #     allow_stretch: True
                        #     keep_ratio: True
                        #     play: True
                        ToggleButton:
                            text: 'Play'
                            size_hint_y: None
                            height: '48dp'
                            size_hint_y: None
                            on_press: camera.play = not camera.play
                            # on_press: app.capture()
                        Button:
                            text: 'Capture'
                            size_hint_y: None
                            height: '48dp'
                            on_press: app.capture()                    
            
            
            MDBottomNavigationItem:
                name: 'image'
                text: 'Detection'
                icon: 'text-recognition'
                on_tab_press: print('Detected image')     

                DetectedImage:
                    FitImage:
                        source: './result.jpg'                    
            
            
            MDBottomNavigationItem:
                name: 'history_nav'
                text: 'History'
                icon: 'history'
                on_tab_press: print('Entering HistoryList')

                HistoryList:
                    name: 'history'

            MDBottomNavigationItem:
                name: 'notes'
                text: 'Notes'
                icon: 'note-text-outline'
                on_tab_press: app.call_history_list()     

                Notes:
                    name: 'last_winner'  

                    ScrollView:
                        MDList:
                            theme_text_color: "Custom"
                            id: container
                            
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
                                                                        
                        MDRaisedButton:
                            text: 'CHECK NUMBER'
                            on_press: app.get_plate_number()
                            pos_hint: {'center_x': .5, 'center_y': .5}  
                            
                        MDRaisedButton:
                            id: select_recognition_button
                            text: 'SELECT DETECTION'
                            pos_hint: {'center_x': .75, 'center_y': .75}  
                            on_release: app.menu.open() if app.menu else app.create_fake_menu()
                        
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
                            text: 'NEW CAPTURE'
                            on_press: app.change_screen_item('camera')      
                            pos_hint: {'center_x': .5, 'center_y': .75}  
                        
                    # MDRaisedButton:
                    #     id: plate_hide_button
                    #     text: 'Hide plate'
                    #     pos_hint: {'center_x': .75, 'center_y': .75}  
                    #     on_release: app.clear_image()
            
                      
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
        return Builder.load_string(KV)

    def call_history_list(self):
        plate_len = (7, 8)
        for i in range(20):
            plate_number = ''.join(random.choice(string.digits) for _ in range(random.choice(plate_len)))
            plate_status = random.choice(('OK', 'OUT OF DATE'))
            text_color = [.2, .4, .6, 1]

            if len(plate_number) == 7:
                text = '{}-{}-{}'.format(plate_number[:2], plate_number[2:5], plate_number[5:])
            elif len(plate_number) == 8:
                text = '{}-{}-{}'.format(plate_number[:3], plate_number[3:5], plate_number[5:])
            else:
                text = plate_number

            self.root.get_screen('main_screen').ids.container.add_widget(
                ThreeLineListItem(text=text,
                                  secondary_text=plate_status,
                                  tertiary_text="bla_bla_bla",
                                  text_color=text_color)
            )

    def change_screen_item(self, nav_item):
        s = self.root.get_screen('main_screen')
        s.ids.bottom_nav.switch_tab(nav_item)
        self.root.current = 'main_screen'

    def get_plate_number(self):
        recognition_result = paddle_ocr_recognition_img("temp_plate.png")
        filtered_result = [res for res in recognition_result if len(res) >= 1]

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

    def set_item(self, text__item):
        self.root.get_screen('main_screen').ids.plate_label_label.text = text__item
        self.menu.dismiss()

    def create_fake_menu(self):
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

    def check_plate_number(self):
        pass

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
        self.change_screen_item('search')


if __name__ == "__main__":
    TestChecker().run()
