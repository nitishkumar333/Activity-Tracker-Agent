from Config import initialize
import os
import sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.properties import StringProperty,BooleanProperty
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from tracking_logic.final import Final_Tracker

from plyer import notification
from system_info import get_system_info
import requests
import psutil
from collections import namedtuple
from dotenv import load_dotenv
import pyautogui
import threading
import time, json
from datetime import datetime
import uuid, re
from PIL import Image, ImageFilter
import boto3
from io import BytesIO
from cryptography.fernet import Fernet

#compressed
import gzip
import zipfile

import logging

# Set the global logging level to WARNING to suppress DEBUG and INFO messages
logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.basicConfig(level=logging.WARNING) 

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

load_dotenv() 

aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
region_name = os.getenv('AWS_REGION')
bucket_name = os.getenv('BUCKET_NAME')
key = os.getenv('ENCRYPTION_KEY')
cipher_suite = Fernet(key)

s3_client = boto3.client(
    's3',
    aws_access_key_id = aws_access_key_id,
    aws_secret_access_key = aws_secret_access_key,
    region_name = region_name
)
mac_address = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
#agent 

class AgentConfig:
    global s3_client
    def fetch_data():
        response = s3_client.get_object(Bucket=bucket_name, Key='python_agent_data.json')
        file_content = response['Body'].read().decode('utf-8')

        # Convert JSON to Python dictionary
        data = json.loads(file_content, object_hook = lambda d : namedtuple('X', d.keys())(*d.values()))
        return data

class HomeScreen(Screen):
    timer_text = StringProperty("00:00:00")  
    global mac_address
    global s3_client
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.seconds = 0  
        self.timer_event = None
        self.bot_activity_detected=[False]
        self.stop=[True]
        self.stop_event = threading.Event() 
        self.activity_thread = None
        self.activity_Pop_thread = None
        self.Upload_local_thread = None
        self.screenshot_thread = None  
        self.stop_thread()
        self.percentage = 100
        self.is_plugged = [True]
        self.is_running = False
        AgentData = namedtuple('AgentData', ['interval', 'screenshot', 'blur'])
        self.agent_data = AgentData(interval='600', screenshot=True, blur=True)
        self.file_name_ss = f"{mac_address}/screenshots/"
        self.file_name = f"{mac_address}/bot_detected/"
        self.Upload_local_thread = threading.Thread(target=self.upload_locals,daemon=True)
        self.Upload_local_thread.start()
        self.Time_pop=[False]

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
        self.activity_thread = threading.Thread(target=Final_Tracker, args=(self.bot_activity_detected,self.stop,self.Time_pop), daemon=True)
        self.activity_Pop_thread = threading.Thread(target=self.monitor_bot_activity, args=(self.stop,), daemon=True)
        # Start screenshot thread if screenshot feature is enabled
        if self.agent_data.screenshot and self.agent_data.screenshot == True:
            self.is_running = True
            self.screenshot_thread = threading.Thread(target=self.take_screenshots, args=(self.stop,), daemon=True)
            self.screenshot_thread.start()

        self.activity_thread.start()
        self.activity_Pop_thread.start()
        

    def stop_thread(self):
        self.stop_event.set()
        
        if self.activity_thread is not None:
            self.activity_thread.join()
            self.activity_thread = None  

        if self.activity_Pop_thread is not None:
            self.activity_Pop_thread = None  
        
        if self.Upload_local_thread is not None:
            self.Upload_local_thread = None  

        if self.screenshot_thread and self.screenshot_thread.is_alive():
            self.is_running = False  # This stops the screenshot loop
            self.screenshot_thread.join(timeout=0) # Ensure thread has finished
            self.screenshot_thread = None



    def monitor_bot_activity(self, stop):
        while not stop[0]: 
            Inet = self.check_internet_connection()
            if Inet:
                self.agent_data=AgentConfig.fetch_data()
            # Check for bot activity
            if self.bot_activity_detected[0]:
                log_content, Local_name = self.File_Create()
                if Inet:
                    try:
                        self.upload_log_to_s3(self.file_name + Local_name, log_content)
                    except Exception as e:
                        print(f"Error uploading to S3: {str(e)}")
                else:
                    # Save log locally if there's no internet
                    script_dir = os.path.dirname(os.path.abspath(__file__))
                    directory = os.path.join(script_dir, "Queue", "Activity_Log")
                    try:
                        if not os.path.exists(directory):
                            os.makedirs(directory)

                        # Create the full file path
                        file_path = os.path.join(directory, Local_name)

                        # Save the log content to the file
                        with open(file_path, 'w') as file:
                            file.write(log_content)

                        print(f"Log saved locally at {file_path}")
                    except Exception as e:
                        print(f"Error saving log locally: {str(e)}")

                Clock.schedule_once(self.show_bot_warning, 0)  # Show warning 
                self.bot_activity_detected[0] = False 
                threading.Event().wait(5)  # Wait after logging bot activity

            # Check internet connection and log status
            if self.Time_pop[0]:
                Clock.schedule_once(self.show_Time_warning, 0)
                self.Time_pop[0]=False
    
    def show_bot_warning(self, dt):
        notification.notify(
            title="Warning",
            message="Bot activity detected!",
            timeout=10
        )
    
    def show_Time_warning(self, dt):
        notification.notify(
            title="Warning",
            message="TimeZone Change Detected detected!",
            timeout=10
        )

    def show_Inet_warning(self, dt):
        notification.notify(
            title="Warning",
            message="No Internet Connection Found! Please Connect soon!",
            timeout=10
        )

    def upload_log_to_s3(self, file_name, log_content):
        compressed_log = BytesIO()
        with gzip.GzipFile(fileobj=compressed_log, mode='wb') as gz_file:
            gz_file.write(log_content.encode())
        
        compressed_log.seek(0)
        encrypted_log = cipher_suite.encrypt(compressed_log.getvalue())
        s3_client.put_object(Bucket=bucket_name, Key=file_name, Body=encrypted_log)
        print(f"Compressed and encrypted log uploaded to S3 as {file_name}")

    def File_Create(self):
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_content = f"Bot Detected at {current_datetime}"
        tempuuid = str(datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")) 
        mac_address = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        return log_content,tempuuid+".txt"
    

    def check_internet_connection(self):
        try:
            requests.get("https://www.google.com", timeout=5)
            return True
        except requests.ConnectionError:
            return False



    #ScreenShot Work  
    def upload_SS_to_s3(self, image, file_name, Local):
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        compressed_image = BytesIO()
        with zipfile.ZipFile(compressed_image, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.writestr(f'{file_name}.png', img_byte_arr.getvalue())
        
        compressed_image.seek(0)
        encrypted_image = cipher_suite.encrypt(compressed_image.getvalue())
        encrypted_image_io = BytesIO(encrypted_image)
        s3_client.upload_fileobj(encrypted_image_io, bucket_name, file_name + Local)
        print(f"Compressed and encrypted image uploaded to S3 as {file_name + Local}")


    def File_Create_SS(self):
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tempuuid = str(datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")) 
        mac_address = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        return tempuuid+".png"

    def take_screenshots(self,stop):
        while not stop[0]:
            Inet = self.check_internet_connection()
            if Inet:
                self.agent_data = AgentConfig.fetch_data()
            if self.agent_data.screenshot:
                try:
                    interval = int(self.agent_data.interval)
                except ValueError:
                    return
                while self.is_running:
                    ss = pyautogui.screenshot()
                    # Apply blur if needed
                    if self.agent_data.blur:
                        ss = ss.filter(ImageFilter.GaussianBlur(radius=5))

                    Inet = self.check_internet_connection()
                    Local = self.File_Create_SS()
                    
                    if not Inet:
                        self.save_screenshot_locally(ss, Local)
                        Clock.schedule_once(self.show_Inet_warning, 0)
                    else:
                        try:
                            # Upload the screenshot directly to S3
                            self.upload_SS_to_s3(ss, self.file_name_ss, Local)
                            print("Screenshot uploaded to S3.")
                            # Update agent data from the config
                            self.agent_data = AgentConfig.fetch_data()
                        except Exception as e:
                            print(f"Error uploading screenshot: {str(e)}")
                            self.save_screenshot_locally(ss, Local)
                    threading.Event().wait(interval)
            
    def save_screenshot_locally(self, ss, Local):
        """Save the screenshot locally if there's no internet."""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        directory = os.path.join(script_dir, "Queue", "Screen_Shot")
        
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
            
            file_path = os.path.join(directory, Local)
            ss.save(file_path)
            print(f"Screenshot saved locally at {file_path}")
        except Exception as e:
            print(f"Error saving screenshot locally: {str(e)}")

    def upload_locals(self):
        while True:
            try:
                script_dir = os.path.dirname(os.path.abspath(__file__))

                # Directories for logs and screenshots
                log_directory = os.path.join(script_dir, "Queue", "Activity_Log")
                screenshot_directory = os.path.join(script_dir, "Queue", "Screen_Shot")

                Inet = self.check_internet_connection()  # Check internet connection once per loop
                
                if Inet:
                    # Upload logs
                    if os.path.exists(log_directory):
                        files = os.listdir(log_directory)
                        for Local in files:
                            file_path = os.path.join(log_directory, Local)
                            if os.path.isfile(file_path):
                                try:
                                    with open(file_path, 'r') as file:
                                        log_content = file.read()

                                    # Upload the log file to S3
                                    self.upload_log_to_s3(self.file_name + "-" + Local, log_content)
                                    logging.info(f"Uploaded log {self.file_name + '-' + Local} to S3.")

                                    # Delete the file after successful upload
                                    os.remove(file_path)
                                    logging.info(f"Deleted local log file: {Local}")
                                except Exception as e:
                                    logging.error(f"Error uploading {Local} to S3: {str(e)}")

                    # Upload screenshots
                    if os.path.exists(screenshot_directory):
                        files = os.listdir(screenshot_directory)
                        for Local in files:
                            file_path = os.path.join(screenshot_directory, Local)
                            if os.path.isfile(file_path):
                                try:
                                    # Check if the file is a screenshot (e.g., ends with .png or .jpg)
                                    if Local.lower().endswith(('.png', '.jpg', '.jpeg')):
                                        # Open the image file to upload
                                        with Image.open(file_path) as image:
                                            # Upload the screenshot to S3
                                            self.upload_SS_to_s3(image, self.file_name_ss, Local)  # Use the correct upload function
                                            logging.info(f"Uploaded screenshot {Local} to S3.")
                                        
                                        # Delete the file after successful upload
                                        os.remove(file_path)
                                        logging.info(f"Deleted local screenshot file: {Local}")
                                except Exception as e:
                                    logging.error(f"Error uploading {Local} to S3: {str(e)}")

                threading.Event().wait(30)  # Wait before the next iteration

            except Exception as e:
                logging.error(f"Error during upload process: {str(e)}")

class ConfigScreen(Screen):
    interval = StringProperty('600')  # Default value
    screenshot = BooleanProperty(True)  # Default value
    blur = BooleanProperty(False)  # Default value

    def __init__(self, **kwargs):
        super(ConfigScreen, self).__init__(**kwargs)
        AgentData = namedtuple('AgentData', ['interval', 'screenshot', 'blur'])
        self.agent_data = AgentData(interval='600', screenshot=True, blur=True)
        self.Inet = False 
        self.config_thread = threading.Thread(target=self.Config_Update, daemon=True)
        self.config_thread.start()

    def Config_Update(self):
        while True:
            self.Inet = self.check_internet_connection()
            if self.Inet:
                new_data = AgentConfig.fetch_data()
                # Update properties dynamically which will automatically reflect in the UI
                self.interval = new_data.interval
                self.screenshot = new_data.screenshot
                self.blur = new_data.blur
                time.sleep(10)
            

    def check_internet_connection(self):
        import requests
        try:
            requests.get("https://www.google.com", timeout=5)
            return True
        except requests.ConnectionError:
            return False



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
