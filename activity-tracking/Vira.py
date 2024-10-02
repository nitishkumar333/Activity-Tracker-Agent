from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivy.uix.popup import Popup
import threading
import random
from system_info import get_system_info

class HomeScreen(Screen):
    timer_text = StringProperty("00:00:00")  

    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.seconds = 0  
        self.timer_event = None
        self.stop_event = threading.Event() 
        

    def start_timer(self):
        if not self.timer_event:  
            self.timer_event = Clock.schedule_interval(self.update_timer, 1)
            self.start_thread()  

    def stop_timer(self):
        if self.timer_event:
            self.timer_event.cancel()
            self.timer_event = None
        self.seconds = 0  # Reset seconds
        self.timer_text = "00:00:00"  # Reset timer display
        self.stop_thread()  # Stop the bot activity monitoring thread

    def update_timer(self, dt):
        self.seconds += 1
        hours, remainder = divmod(self.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.timer_text = f"{hours:02}:{minutes:02}:{seconds:02}" 

    
    def start_thread(self):
        self.stop_event.clear()  # Clear the stop event
        self.activity_thread = threading.Thread(target=self.monitor_bot_activity)
        self.activity_thread.daemon = True  
        self.activity_thread.start()

    def stop_thread(self):
        self.stop_event.set()  # Set the event to signal the thread to stop

    def monitor_bot_activity(self):
        while not self.stop_event.is_set():  # Check if the stop event is set
            # Simulate bot detection logic (replace this with actual logic)
            self.bot_activity_detected = random.choice([False, True])  # Randomly simulate detection
            
            if self.bot_activity_detected:
                Clock.schedule_once(self.show_bot_warning, 0)  # Show warning immediately
                self.bot_activity_detected = False  # Reset the flag after detection
            
            # Sleep for a while (e.g., 1 second) to avoid spamming
            threading.Event().wait(10)
    
    def show_bot_warning(self, dt):
        popup = Popup(title='Warning',
                      content=Label(text='Bot activity detected!'),
                      size_hint=(0.6, 0.3))
        popup.open()
        Clock.schedule_once(lambda dt: popup.dismiss(), 5)  

class ConfigScreen(Screen):
    pass

class AboutScreen(Screen):
    pass

class ViraMain(BoxLayout):
    system_info = get_system_info() 

    def __init__(self, **kwargs):
        super(ViraMain, self).__init__(**kwargs)
        Window.set_icon('Images/Viraico.png')
        Window.minimum_width = 550
        Window.minimum_height = 500
        Window.bind(on_resize=self.on_window_resize)
        

    def on_window_resize(self, instance, width, height):
        if width > 1000:  
            self.ids.sidebar.size_hint_x  = 0.3
            self.ids.VideoBox.size_hint_x  = 0.2
        elif width < 550:
            self.ids.Logo.size  = self.parent.width * 0.3, self.parent.width * 0.3
        else:
            self.ids.sidebar.size_hint_x = 0.5

    

class ViraApp(App):
    def build(self):
        return ViraMain()

if __name__ == '__main__':
    ViraApp().run()
