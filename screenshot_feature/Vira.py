from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivy.uix.camera import Camera


class HomeScreen(Screen):
    timer_text = StringProperty("00:00:00")  

    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.seconds = 0  
        self.timer_event = None

    def start_timer(self):
        if not self.timer_event:  # Only start if not already started
            self.timer_event = Clock.schedule_interval(self.update_timer, 1)

    def stop_timer(self):
        if self.timer_event:
            self.timer_event.cancel()
            self.timer_event = None
        self.seconds = 0  # Reset seconds
        self.timer_text = "00:00:00"  # Reset timer display

    def update_timer(self, dt):
        self.seconds += 1
        hours, remainder = divmod(self.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.timer_text = f"{hours:02}:{minutes:02}:{seconds:02}"          

class ConfigScreen(Screen):
    pass

class AboutScreen(Screen):
    pass

class ViraMain(BoxLayout):
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
            self.ids.VideoBox.size_hint_x  = 0.5
            self.ids.Logo.size  = self.parent.width * 0.3, self.parent.width * 0.3
        else:
            self.ids.sidebar.size_hint_x = 0.5
            self.ids.VideoBox.size_hint_x  = 0.4

class ViraApp(App):
    def build(self):
        return ViraMain()

if __name__ == '__main__':
    ViraApp().run()  
