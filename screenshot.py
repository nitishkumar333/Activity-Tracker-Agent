import pyautogui
from tkinter import *
import threading
import time
import os
from PIL import Image, ImageFilter

class ScreenshotApp:
    def __init__(self, master):
        self.master = master
        self.master.title('Automatic Screenshot App')
        self.master.geometry('700x500')
        self.master.config(bg='Yellow')
        self.master.resizable(False, False)

        self.is_running = False
        self.screenshot_thread = None
        self.blur_var = IntVar()

        self.setup_ui()

    def setup_ui(self):
        Label(self.master, text="Save Directory:", font=('Time New Roman', 20), bg='yellow').place(x=20, y=20)
        self.directory_entry = Entry(self.master, font=('Time New Roman', 20))
        self.directory_entry.place(x=20, y=60, height=40, width=660)

        Label(self.master, text="Screenshot Interval (seconds):", font=('Time New Roman', 20), bg='yellow').place(x=20, y=120)
        self.interval_entry = Entry(self.master, font=('Time New Roman', 20))
        self.interval_entry.place(x=20, y=160, height=40, width=660)
        self.interval_entry.insert(0, "30")  # Default value

        self.blur_checkbox = Checkbutton(self.master, text="Blur Screenshots", variable=self.blur_var, 
                                        font=('Time New Roman', 16), bg='yellow')
        self.blur_checkbox.place(x=20, y=220)

        self.button = Button(self.master, text='Start', font=('Time New Roman', 40, 'bold'), command=self.toggle_screenshots)
        self.button.place(x=250, y=280, height=100, width=200)

        self.status_label = Label(self.master, text="", font=('Time New Roman', 16), bg='yellow')
        self.status_label.place(x=20, y=400, width=660)

    def toggle_screenshots(self):
        if self.is_running:
            self.stop_screenshots()
        else:
            self.start_screenshots()

    def start_screenshots(self):
        try:
            interval = float(self.interval_entry.get())
            if interval <= 0:
                raise ValueError("Interval must be a positive number")
            
            self.is_running = True
            self.button.config(text='Stop')
            self.screenshot_thread = threading.Thread(target=self.take_screenshots)
            self.screenshot_thread.start()
            blur_status = "blurred" if self.blur_var.get() else "normal"
            self.status_label.config(text=f"Taking {blur_status} screenshots every {interval} seconds")
        except ValueError as e:
            self.status_label.config(text=f"Error: {str(e)}")

    def stop_screenshots(self):
        self.is_running = False
        self.button.config(text='Start')
        if self.screenshot_thread:
            self.screenshot_thread.join()
        self.status_label.config(text="Screenshot capture stopped")

    def take_screenshots(self):
        directory = self.directory_entry.get() or '.'
        if not os.path.exists(directory):
            os.makedirs(directory)

        interval = float(self.interval_entry.get())
        count = 1
        while self.is_running:
            path = os.path.join(directory, f'screenshot_{count}.png')
            ss = pyautogui.screenshot()
            
            if self.blur_var.get():
                ss = ss.filter(ImageFilter.GaussianBlur(radius=5))
            
            ss.save(path)
            print(f"Screenshot saved: {path}")
            count += 1
            time.sleep(interval)

if __name__ == '__main__':
    root = Tk()
    app = ScreenshotApp(root)
    root.mainloop()