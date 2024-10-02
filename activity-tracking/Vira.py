from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox

import pyautogui
import threading
import time
import os
from PIL import Image, ImageFilter


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
    def __init__(self, **kwargs):
        super(ConfigScreen, self).__init__(**kwargs)
        self.is_running = False
        self.screenshot_thread = None

    def toggle_screenshots(self):
        if self.is_running:
            self.stop_screenshots()
        else:
            self.start_screenshots()

    def start_screenshots(self):
        try:
            interval_text = self.ids.interval_input.text
            interval = float(interval_text)
            if interval <= 0:
                raise ValueError("Interval must be a positive number")

            self.is_running = True
            self.ids.start_stop_button.text = 'Stop'
            self.screenshot_thread = threading.Thread(target=self.take_screenshots, daemon=True)
            self.screenshot_thread.start()
            blur_status = "blurred" if self.ids.blur_checkbox.active else "normal"
            self.ids.status_label.text = f"Taking {blur_status} screenshots every {interval} seconds"
        except ValueError as e:
            self.ids.status_label.text = f"Error: {str(e)}"

    def stop_screenshots(self):
        self.is_running = False
        self.ids.start_stop_button.text = 'Start'
        if self.screenshot_thread and self.screenshot_thread.is_alive():
            self.screenshot_thread.join()
        self.ids.status_label.text = "Screenshot capture stopped"

    def take_screenshots(self):
        directory = self.ids.directory_input.text.strip() or '.'
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
            except Exception as e:
                Clock.schedule_once(lambda dt: self.update_status(f"Error creating directory: {str(e)}"))
                return

        try:
            interval = float(self.ids.interval_input.text)
        except ValueError:
            Clock.schedule_once(lambda dt: self.update_status("Invalid interval"))
            return

        count = 1
        while self.is_running:
            path = os.path.join(directory, f'screenshot_{count}.png')
            ss = pyautogui.screenshot()

            if self.ids.blur_checkbox.active:
                ss = ss.filter(ImageFilter.GaussianBlur(radius=5))

            try:
                ss.save(path)
                print(f"Screenshot saved: {path}")
                count += 1
            except Exception as e:
                Clock.schedule_once(lambda dt: self.update_status(f"Error saving screenshot: {str(e)}"))
                break

            time.sleep(interval)

        # Update status when loop ends
        if not self.is_running:
            Clock.schedule_once(lambda dt: self.update_status("Screenshot capture stopped"))

    def update_status(self, message):
        self.ids.status_label.text = message


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
            self.ids.sidebar.size_hint_x = 0.3
            self.ids.VideoBox.size_hint_x = 0.2
        elif width < 550:
            self.ids.VideoBox.size_hint_x = 0.5
            self.ids.Logo.size = self.width * 0.3, self.width * 0.3
        else:
            self.ids.sidebar.size_hint_x = 0.5
            self.ids.VideoBox.size_hint_x = 0.4


class ViraApp(App):
    def build(self):
        return ViraMain()


if __name__ == '__main__':
    ViraApp().run()
