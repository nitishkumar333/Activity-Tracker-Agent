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
from plyer import notification
from system_info import get_system_info
from tracking_logic.final import Final_Tracker
from dotenv import load_dotenv
import pyautogui
import threading
import time
import os, uuid, re
from PIL import Image, ImageFilter
import boto3
from io import BytesIO

load_dotenv() # load environment variables

aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
region_name = os.getenv('AWS_REGION')
bucket_name = os.getenv('BUCKET_NAME')

class HomeScreen(Screen):
    timer_text = StringProperty("00:00:00")  

    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.seconds = 0  
        self.timer_event = None
        self.bot_activity_detected=[False]
        self.stop=[True]
        self.stop_event = threading.Event() 
        self.activity_thread = None
        self.stop_thread()

    def start_timer(self):
        if not self.timer_event:  
            self.timer_event = Clock.schedule_interval(self.update_timer, 1)
            self.stop[0]=False
            self.start_thread()  

    def stop_timer(self):
        if self.timer_event:
            self.timer_event.cancel()
            self.timer_event = None
        self.stop[0]=True
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
        self.activity_thread = threading.Thread(target=Final_Tracker, args=(self.bot_activity_detected,self.stop))
        self.activity_Pop_thread = threading.Thread(target=self.monitor_bot_activity)
        self.activity_thread.daemon = True   
        self.activity_Pop_thread.daemon = True  
        self.activity_thread.start()
        self.activity_Pop_thread.start()

    def stop_thread(self):
        self.stop_event.set()  # Set the event to signal the thread to stop 
        if self.activity_thread is not None:
            self.activity_thread.join()

    def monitor_bot_activity(self):
        while not self.stop_event.is_set():  
            if self.bot_activity_detected[0]:
                Clock.schedule_once(self.show_bot_warning, 0)  # Show warning immediately
                self.bot_activity_detected[0] = False  # Reset the flag after detection
            threading.Event().wait(5)
    
    def show_bot_warning(self, dt):
        # Use plyer to show a system notification
        notification.notify(
            title='Warning',
            message='Bot activity detected!',
            timeout=10  # Duration in seconds the notification will be visible
        ) 


class ConfigScreen(Screen):
    mac_address = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    def __init__(self, **kwargs):
        super(ConfigScreen, self).__init__(**kwargs)
        self.is_running = False
        self.screenshot_thread = None
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id = aws_access_key_id,
            aws_secret_access_key = aws_secret_access_key,
            region_name = region_name
        )
        self.bucket_name = bucket_name

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

    def upload_to_s3(self, image):
        # Save screenshot to an in-memory file (BytesIO)
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        tempuuid = str(uuid.uuid4())[0:15] # random string
        # Define S3 file path and upload
        s3_path = f'{self.mac_address}/screenshots/{tempuuid}.png'
        self.s3_client.upload_fileobj(img_byte_arr, self.bucket_name, s3_path)

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
                self.upload_to_s3(ss)
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
    system_info = get_system_info() 
    def __init__(self, **kwargs):
        super(ViraMain, self).__init__(**kwargs)
        Window.set_icon('Images/Viragfadsgfasico.png')
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