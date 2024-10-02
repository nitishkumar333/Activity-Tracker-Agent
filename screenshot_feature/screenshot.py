from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.clock import Clock
import pyautogui
import threading
import time
import os
from PIL import Image, ImageFilter

class ScreenshotApp(App):
    def build(self):
        self.is_running = False
        self.screenshot_thread = None
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        directory_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=30)
        directory_layout.add_widget(Label(text="Save Directory:", size_hint_x=0.3))
        self.directory_input = TextInput(text="", multiline=False, size_hint_x=0.7)
        directory_layout.add_widget(self.directory_input)
        layout.add_widget(directory_layout)
        
        interval_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=30)
        interval_layout.add_widget(Label(text="Interval (seconds):", size_hint_x=0.3))
        self.interval_input = TextInput(text="30", multiline=False, size_hint_x=0.7)
        interval_layout.add_widget(self.interval_input)
        layout.add_widget(interval_layout)
        
        blur_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=30)
        blur_layout.add_widget(Label(text="Blur Screenshots:", size_hint_x=0.3))
        self.blur_checkbox = CheckBox(active=False, size_hint_x=0.7)
        blur_layout.add_widget(self.blur_checkbox)
        layout.add_widget(blur_layout)
        
        self.start_stop_button = Button(text="Start", on_press=self.toggle_screenshots)
        layout.add_widget(self.start_stop_button)
        
        self.status_label = Label(text="Ready to start")
        layout.add_widget(self.status_label)
        
        return layout

    def toggle_screenshots(self, instance):
        if self.is_running:
            self.stop_screenshots()
        else:
            self.start_screenshots()

    def start_screenshots(self):
        try:
            interval = float(self.interval_input.text)
            if interval <= 0:
                raise ValueError("Interval must be a positive number")
            
            self.is_running = True
            self.start_stop_button.text = 'Stop'
            self.screenshot_thread = threading.Thread(target=self.take_screenshots)
            self.screenshot_thread.start()
            blur_status = "blurred" if self.blur_checkbox.active else "normal"
            self.status_label.text = f"Taking {blur_status} screenshots every {interval} seconds"
        except ValueError as e:
            self.status_label.text = f"Error: {str(e)}"

    def stop_screenshots(self):
        self.is_running = False
        self.start_stop_button.text = 'Start'
        if self.screenshot_thread:
            self.screenshot_thread.join()
        self.status_label.text = "Screenshot capture stopped"

    def take_screenshots(self):
        directory = self.directory_input.text or '.'
        if not os.path.exists(directory):
            os.makedirs(directory)

        interval = float(self.interval_input.text)
        count = 1
        while self.is_running:
            path = os.path.join(directory, f'screenshot_{count}.png')
            ss = pyautogui.screenshot()
            
            if self.blur_checkbox.active:
                ss = ss.filter(ImageFilter.GaussianBlur(radius=5))
            
            ss.save(path)
            print(f"Screenshot saved: {path}")
            count += 1
            time.sleep(interval)

if __name__ == '__main__':
    ScreenshotApp().run()