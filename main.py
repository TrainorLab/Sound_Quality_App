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

class ResponseScreen(Screen):
    pass

class ScreenManagerApp(App):
    def build(self):
        
        
        self.slider1 = Slider(min=1, max=5, value=3)
        self.slider2 = Slider(min=1, max=5, value=3)
        self.q1_text = Label(text='Please rate the previous 5 minutes on "naturalness" on a scale from 1-5', size_hint_y=None, height=20)     
        self.q1_left_anchor = Label(text='1 (Least Natural)', halign = "left")
        self.q1_right_anchor = Label(text='5 (Most Natural)', halign = "right")
        self.q2_text = Label(text='Please rate the previous 5 minutes on "sound quality" on a scale from 1-5', size_hint_y=None, height=20)
        self.q2_left_anchor = Label(text='1 (Worst)', halign = "left", valign = "bottom")
        self.q2_right_anchor = Label(text='5 (Best)', halign = "right", valign = "bottom")

        self.q1 = BoxLayout(orientation='vertical', size_hint_y=None, height=30)
        self.q1.add_widget(self.q1_text)
        
        self.q1_anchors = BoxLayout(orientation = 'horizontal', size_hint_y=None, height=10)   
        self.q1_anchors.add_widget(self.q1_left_anchor)
        self.q1_anchors.add_widget(self.q1_right_anchor)

        self.q1_to_q2 = BoxLayout(orientation = 'vertical')
        self.q1_to_q2.add_widget(self.slider1)
        self.q1_to_q2.add_widget(self.q2_text)


        self.q2_anchors = BoxLayout(orientation='horizontal', size_hint_y=None, height=30)
        self.q2_anchors.add_widget(self.q2_left_anchor)
        self.q2_anchors.add_widget(self.q2_right_anchor)

        
        self.button = Button(text='Submit', on_press=self.submit)
        self.main_screen = MainScreen(name='main')
        self.main_screen_layout = BoxLayout(orientation='vertical', spacing=10)
        
        
        self.main_screen_layout.add_widget(self.q1)
        self.main_screen_layout.add_widget(self.q1_anchors)
        self.main_screen_layout.add_widget(self.q1_to_q2)
        self.main_screen_layout.add_widget(self.q2_anchors)
        self.main_screen_layout.add_widget(self.slider2)
        self.main_screen_layout.add_widget(self.button)
        
        self.main_screen.add_widget(self.main_screen_layout)
        self.response_screen = ResponseScreen(name='response')
        self.response_label = Label(text='Thank you for your response.', size_hint=(0.5, 0.5), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.response_screen.add_widget(self.response_label)
        self.sm = ScreenManager()
        self.sm.add_widget(self.main_screen)
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

        elif platform.system() == 'Android':
            base_dir = '\\Internal storage\\Android\\'
        else:
            print("<<<<<<<<<<<<<<", platform.system(), ">>>>>>>>>>>>>>>>>>")
            from android.permissions import Permission, request_permissions, check_permission
            from android.storage import app_storage_path, primary_external_storage_path, secondary_external_storage_path

            request_permissions([Permission.WRITE_EXTERNAL_STORAGE])
            print("<<<<<<<<<<<<<<", primary_external_storage_path(), ">>>>>>>>>>>>>>>>>>")
            filename = os.path.join(primary_external_storage_path(), 'responses_{}.json'.format(now.strftime('%Y-%m-%d_%H-%M-%S')))
            pass

        store = JsonStore(filename)
        store.put('naturalness', value=self.slider1.value)
        store.put('sound_quality', value=self.slider2.value)
        self.sm.current = 'response'
        Clock.schedule_once(self.switch_back_to_main_screen, self.get_next_update_time())

    def on_start(self):
        # Schedule the screen refresh at regular intervals
       Clock.schedule_interval(self.update_screen, 1) # 1 second interval

    def update_screen(self, dt):
        # Update the screen with current time
        now = datetime.datetime.now(pytz.timezone('US/Eastern'))

    def switch_back_to_main_screen(self, dt):
        self.sm.current = 'main'

    def get_next_update_time(self):
        now = datetime.datetime.now(pytz.utc).astimezone(pytz.timezone('US/Eastern'))
        next_update = now + datetime.timedelta(minutes=5 - now.minute % 5, seconds=-now.second, microseconds=-now.microsecond)
        time_to_next_update = (next_update - now).total_seconds()
        return time_to_next_update

if __name__ == '__main__':
    ScreenManagerApp().run()
