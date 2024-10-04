# 📊 **Activity Tracker Agent**

The **Activity Tracker Agent** is a Python-based desktop application designed to monitor user activity and distinguish between genuine user behavior and automated/scripted inputs.


| **Working** |
|:------------:|
| ![Configuration Interface](public/charts_whitebg.gif) |

## ✨ **Features**

### 🔍 **Activity Tracking**
- 🖱️ **Mouse Tracking**: Identifies patterns in cursor moving.
- 👆 **Mouse Click Tracking**: Track if mouse is clicking without movement.
- ⌨️ **Keyboard Tracking**: Monitors key press intverals and analysis them.

### 🕑 **Time Zone Management**
- 🌍 **Time Zone Detection**: Automatically detects system time zone changes in system and report timestamps.

### 📸 **Screenshot Capture**
- ⏱️ **Configurable Intervals**: Set screenshot intervals, through the web app.
- 😶‍🌫️ **Optional Blur**: Enable/disable blurring for privacy, via the web app.
- ☁️ **Cloud Storage Upload**: Uploads screenshots to Amazon S3.
  
### 📸 **No internet connection**
- 🫸 **Queue Management**: stores the files in the queue if no internet connection, then after connectivity uploads to S3.
- ☁️ **Amazon S3 Upload**: Uploads screenshots to Amazon S3 after connection establish.

#

### 🌐 **Web Application**
This allows users to configure settings like screenshot interval, enable/disable screenshots, blur.

## 📸 **App Preview**

| **App Landing**  | **Enabled Settings**                           |
|------------------------------------------------------|---------------------------------------------------------|
| ![Configuration Interface](public/vira_landing.png)  | ![Blurred Screenshot](public/vira_config.png) |

## 🌐 **Web App Preview**

| **User Login**  | **Configuration Module**                           |
|------------------------------------------------------|---------------------------------------------------------|
| ![Configuration Interface](public/web_login.png)  | ![Configuration Module](public/web_configure.png) |

## 🛠️ **Working**

### 🧑‍💻 **Main Workflow**
The application starts by initializing 🖱️ **mouse**, ⌨️ **keyboard**, and 🌍 **time zone tracking** on separate threads to continuously monitor activity. Based on the captured data, the system detects patterns of human activity and flags bot-like behavior using advanced algorithms. Users can configure settings such as screenshot intervals, blurring options, and more via the accompanying web app.

#### 🖥️ **Code Overview**
```python
import threading
import mouse_tracking
import mouse_click_tracking
import keyboard_tracking
import timezone_tracking

def main():
    movement_thread = threading.Thread(target=mouse_tracking.track_mouse_movement)
    movement_thread.start()

    keyboard_thread = threading.Thread(target=keyboard_tracking.monitor_keyboard)
    keyboard_thread.start()

    timezone_thread = threading.Thread(target=timezone_tracking.detect_time_zone_change)
    timezone_thread.start()

    mouse_click_tracking.detect_clicks()

if __name__ == "__main__":
    main()
```

### 🖱️ **Mouse Tracking**
Captures mouse movement patterns and analyzes them to distinguish between natural human behavior and automated inputs.

### ⌨️ **Keyboard Tracking**
Monitors key press events and flags suspicious typing patterns that indicate bot-like activity.

```python
def monitor_keyboard():
    keyboard.hook(on_key_event)
    keyboard.wait('esc')
```

### 🌍 **Time Zone Tracking**
Real-time detection of time zone changes, logging every modification.

```python
def detect_time_zone_change():
    # Listens for system time zone changes and adjusts logs accordingly
    ...
```

### 👆 **Mouse Click Tracking**
Detects repeated clicks without mouse movement and flags it as automated if the frequency exceeds a certain threshold.

```python
def detect_clicks():
    with mouse.Listener(on_click=on_click, on_move=on_move) as listener:
        listener.join()
```

### 🕒 **Inactivity Detection**
Tracks idle time when there is no user activity and logs it as inactivity once a defined threshold is reached.

## 📂 **Setup and Installation**

1. **Clone the repository**:
   ```bash
   git clone https://github.com/nitishkumar333/Activity-Tracker-Agent.git
   ```

2. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   Required libraries include:
   - `pynput`
   - `pytz`
   - `ctypes`
   - `keyboard`
   - `pyautogui`
   - `Pillow`

3. **Run the application**:
   ```bash
   python final.py
   ```

## 🎯 **Future Enhancements**
- 🔍 **Advanced Filtering**: Implement more sophisticated algorithms for detecting automated user behavior.
- 🔔 **Custom Alerts**: Expand alert options for more scenarios, such as extended user inactivity or high bot-like activity.

## 👥 **Contributors**
This project was developed by:
- [Nitish Kumar](https://github.com/nitishkumar333)
- [Ayush Sharma](https://github.com/ayusharma03)
- [Abhishek Dixit](https://github.com/Adixit8604)
- [Nimisha](https://github.com/)

--- 

This enhanced README makes the app visually engaging and interactive with the help of emojis while maintaining all the important information.