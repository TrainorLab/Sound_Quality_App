from kivy.app import App
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.storage.jsonstore import JsonStore
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
import datetime
import pytz
import os
import platform

class MainScreen(Screen):
    pass

class ConfirmScreen(Screen):
    pass

class ResponseScreen(Screen):
    pass

class ScreenManagerApp(App):
    def build(self):
        
        #huawei sizes (55, 40)
        global_font_size1 = 40
        global_font_size2 = 32
        red = [1, 0, 0, 1] 
        green = [0, 1, 0, 1]

        #Create all text labels and sliders
        self.slider1 = Slider(min=1, max=5, value=3)
        self.slider2 = Slider(min=1, max=5, value=3)
        self.q1_text = Label(text='Please rate the previous 5 minutes on \n "naturalness" on a scale from 1-5', font_size = global_font_size1)     
        self.q1_left_anchor = Label(text='1 (Least Natural)', halign = "left", valign = "bottom", font_size = global_font_size2)
        self.q1_right_anchor = Label(text='5 (Most Natural)', halign = "right", valign = "bottom", font_size = global_font_size2)
        self.q2_text = Label(text='Please rate the previous 5 minutes on \n "sound quality" on a scale from 1-5', font_size = global_font_size1)
        self.q2_left_anchor = Label(text='1 (Worst)', halign = "left", valign = "bottom", font_size = global_font_size2)
        self.q2_right_anchor = Label(text='5 (Best)', halign = "right", valign = "bottom", font_size = global_font_size2)

        #Vertical Layout for Question 1, add to box q1
        self.q1 = BoxLayout(orientation='vertical', size_hint=(1,1))
        self.q1.add_widget(self.q1_text)
        
        #Horizontal layout for q1 anchors, 
        self.q1_anchors = BoxLayout(orientation = 'horizontal', size_hint=(1,.25))   
        self.q1_anchors.add_widget(self.q1_left_anchor)
        self.q1_anchors.add_widget(self.q1_right_anchor)

        self.q1_to_q2 = BoxLayout(orientation = 'vertical', size_hint=(1,1))
        self.q1_to_q2.add_widget(self.slider1)
        self.q1_to_q2.add_widget(self.q2_text)


        self.q2_anchors = BoxLayout(orientation='horizontal', size_hint=(1,.25))
        self.q2_anchors.add_widget(self.q2_left_anchor)
        self.q2_anchors.add_widget(self.q2_right_anchor)

        self.button = Button(text='Submit', on_press=self.go_to_confirm_screen, size_hint = (1,.5), font_size = 100)
        
        self.main_screen = MainScreen(name='main')
        self.main_screen_layout = BoxLayout(orientation='vertical')
        
        
        self.main_screen_layout.add_widget(self.q1)
        self.main_screen_layout.add_widget(self.q1_anchors)
        self.main_screen_layout.add_widget(self.q1_to_q2)
        self.main_screen_layout.add_widget(self.q2_anchors)
        self.main_screen_layout.add_widget(self.slider2)
        self.main_screen_layout.add_widget(self.button)
        
        self.main_screen.add_widget(self.main_screen_layout)

        self.confirm_screen = ConfirmScreen(name='confirm')
        self.confirm_screen_layout = BoxLayout(orientation = 'vertical')
        self.confirm_q = Label(text = "Are you sure you wish to submit your ratings?", font_size = global_font_size1)
        self.confirm_yes_button = Button(text='Yes', on_press=self.submit, size_hint = (.25,.25), background_color = green)
        self.confirm_no_button = Button(text='No', on_press=self.switch_back_to_main_screen, size_hint = (.25,.25), background_color = red)
        
        self.confirm_text_layout = BoxLayout(orientation = 'vertical')
        self.confirm_text_layout.add_widget(self.confirm_q)
        self.confirm_buttons = BoxLayout(orientation = 'horizontal')
        self.confirm_buttons.add_widget(self.confirm_yes_button)
        self.confirm_buttons.add_widget(self.confirm_no_button)
        self.confirm_screen_layout = BoxLayout(orientation = 'vertical')
        self.confirm_screen_layout.add_widget(self.confirm_text_layout)
        self.confirm_screen_layout.add_widget(self.confirm_buttons)
        self.confirm_screen.add_widget(self.confirm_screen_layout)

        self.response_screen = ResponseScreen(name='response')
        self.response_label = Label(text='Thank you for your response. \n Please wait until the rating sliders appear again.', pos_hint={'center_x': 0.5, 'center_y': 0.5}, font_size = global_font_size2, halign = 'center')
        self.response_screen.add_widget(self.response_label)
        self.sm = ScreenManager()
        self.sm.add_widget(self.main_screen)
        self.sm.add_widget(self.confirm_screen)
        self.sm.add_widget(self.response_screen)
        Clock.schedule_once(self.show_app, self.get_next_update_time())
        return self.sm

    def show_app(self, dt):
        Window.show()
        Clock.schedule_once(self.show_app, self.get_next_update_time())

    def submit(self, instance):
        now = datetime.datetime.now(pytz.utc).astimezone(pytz.timezone('US/Eastern'))
        if platform.system() == 'Windows':
            base_dir = 'C:\\AppData\\Android\\SoundQualityApp'
            filename = os.path.join(base_dir, 'responses_{}.json'.format(now.strftime('%Y-%m-%d_%H-%M-%S')))

        elif platform.system() == 'Linux':
            print("<<<<<<<<<<<<<<", platform.system(), ">>>>>>>>>>>>>>>>>>")
            from android.permissions import Permission, request_permissions, check_permission
            from android.storage import app_storage_path, primary_external_storage_path, secondary_external_storage_path

            request_permissions([Permission.WRITE_EXTERNAL_STORAGE])
            print("<<<<<<<<<<<<<<", primary_external_storage_path(), ">>>>>>>>>>>>>>>>>>")
            filename = os.path.join(primary_external_storage_path(), 'responses_{}.json'.format(now.strftime('%Y-%m-%d_%H-%M-%S')))
        else:
            pass

        store = JsonStore(filename)
        store.put('naturalness', value=self.slider1.value)
        store.put('sound_quality', value=self.slider2.value)
        self.sm.current = 'response'
        Clock.schedule_once(self.switch_back_to_main_screen, self.get_next_update_time())
        self.slider1.value = 3
        self.slider2.value = 3


    def on_start(self):
        # Schedule the screen refresh at regular intervals
       Clock.schedule_interval(self.update_screen, 1) # 1 second interval

    def update_screen(self, dt):
        # Update the screen with current time
        now = datetime.datetime.now(pytz.timezone('US/Eastern'))

    def switch_back_to_main_screen(self, dt):
        self.sm.current = 'main'

    def go_to_confirm_screen(self, dt):
        self.sm.current = 'confirm'

    def get_next_update_time(self):
        now = datetime.datetime.now(pytz.utc).astimezone(pytz.timezone('US/Eastern'))
        next_update = now + datetime.timedelta(minutes=5 - now.minute % 5, seconds=-now.second, microseconds=-now.microsecond)
        time_to_next_update = (next_update - now).total_seconds()
        return time_to_next_update
        
if __name__ == '__main__':
    ScreenManagerApp().run()
