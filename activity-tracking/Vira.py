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
from tracking_logic.final import Final_Tracker

from plyer import notification
from system_info import get_system_info
import requests
import psutil
import sys

from dotenv import load_dotenv
import pyautogui
import threading
import time
import os, uuid, re
from PIL import Image, ImageFilter
import boto3
from io import BytesIO

def check_if_already_running(script_name):
    current_pid = os.getpid()
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        cmdline = proc.info['cmdline']
        if cmdline and script_name in cmdline and proc.info['pid'] != current_pid:
            print(f"Another instance of {script_name} is already running.")
            sys.exit()

def run_in_thread(script_name):
    check_thread = threading.Thread(target=check_if_already_running, args=(script_name,))
    check_thread.daemon = True  # Daemon threads automatically close when the program exits
    check_thread.start()

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
        self.activity_Pop_thread = None
        self.battery_thread = None
        self.stop_thread()
        self.percentage = 100
        self.is_plugged = [True]

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
        self.stop_event.clear()  
        self.activity_thread = threading.Thread(target=Final_Tracker, args=(self.bot_activity_detected,self.stop,self.percentage,self.is_plugged
        ), daemon=True)
        self.activity_Pop_thread = threading.Thread(target=self.monitor_bot_activity, args=(self.stop,), daemon=True)
        self.battery_thread = threading.Thread(target=self.check_battery_status, args=(self.stop,), daemon=True)
        self.battery_thread.start()
        self.activity_thread.start()
        self.activity_Pop_thread.start()

    def stop_thread(self):
        self.stop_event.set()
        if self.activity_thread is not None:
            self.activity_thread.join()
            self.activity_thread = None  
        
        if self.activity_Pop_thread is not None:
            self.activity_Pop_thread = None  
        
        if self.battery_thread is not None:
            self.battery_thread = None  


    def monitor_bot_activity(self, stop):
        while not stop[0]: 
            Inet = self.check_internet_connection()
            if not Inet:
                Clock.schedule_once(self.show_Inet_warning, 0)
                threading.Event().wait(5)
            elif self.bot_activity_detected[0]:
                Clock.schedule_once(self.show_bot_warning, 0)  # Show warning immediately
                self.bot_activity_detected[0] = False 
                threading.Event().wait(5)  
            
            threading.Event().wait(5)  # Wait for 5 seconds

    def check_battery_status(self, stop):
        while not stop[0]:
            battery = psutil.sensors_battery()  # Get battery status
            if battery is not None:
                self.percentage = battery.percent
                self.is_plugged = [battery.power_plugged]
            threading.Event().wait(600)  
            

    def show_bot_warning(self, dt):
        # Use plyer to show a system notification
        notification.notify(
            title='Warning',
            message='Bot activity detected!',
            timeout=10 ) 
    
    def show_Inet_warning(self, dt):
        notification.notify(
            title='Warning',
            message='No Internet Connection Found! Please Connect soon!',
            timeout=10  )# Duration in seconds the notification will be visible

    def check_internet_connection(self):
        try:
            requests.get("https://www.google.com", timeout=5)
            return True
        except requests.ConnectionError:
            return False
        


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
    run_in_thread('Vira.py')
    ViraApp().run()
