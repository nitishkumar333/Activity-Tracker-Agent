Here’s a detailed `README.md` file that explains how the different tracking functions work in the **Activity Tracker Agent** project:

---

# 📊 Activity Tracker Agent

## Overview

The **Activity Tracker Agent** is designed to monitor user activity and identify automated/scripted inputs using advanced tracking techniques for mouse movement, mouse clicks, keyboard events, and time zone changes. This document provides a detailed explanation of how each tracking function works within the system.

---

## Features

- **Mouse Movement Tracking**: Detects patterns and differentiates between natural and scripted movements.
- **Mouse Click Tracking**: Flags repetitive clicks without movement as bot-like behavior.
- **Keyboard Tracking**: Analyzes typing speed and patterns to detect unnatural inputs.
- **Time Zone Detection**: Monitors changes in the system time zone and adjusts the logs accordingly.

---

## Tracking Functions

### 1. 🖱️ Mouse Movement Tracking

**File**: `mouse_tracking.py`

This module captures the movement of the mouse in real time, logs the coordinates, and analyzes the movement pattern to detect whether the activity is human or bot-like.

#### Key Components:
- **Movement Data**: The mouse coordinates are captured continuously and stored in a list for analysis.
- **Straight-Line Movement Detection**: It counts the number of consecutive movements in a straight line. If the count exceeds a threshold, it flags the activity as bot-like.
- **Repeated Pattern Detection**: The system compares segments of the movement pattern to detect repetitions, which could indicate automation.

#### Main Function:
```python
def track_mouse_movement():
    mouse_data = []
    start_time = time.time()
    
    while time.time() - start_time < 20:  # Runs for 20 seconds
        x, y = get_mouse_position()
        mouse_data.append((x, y))
        
        if len(mouse_data) > 500:  # Analyze every 500 points
            result = detect_bot_or_human(mouse_data)
            print("Is bot detected: ", result)
            mouse_data.clear()
        
        time.sleep(0.02)
```

#### Detection Logic:
1. **Straight Line Movement**: Continuous movement in a straight line is considered suspicious if it surpasses a threshold.
2. **Pattern Repetition**: Detects if the user repeats the same movement, which is a potential indicator of scripted activity.

---

### 2. 🖱️ Mouse Click Tracking

**File**: `mouse_click_tracking.py`

The mouse click tracking module monitors both clicks and movement. If a certain number of clicks occur at the same position without any mouse movement, the system flags this as potential bot-like activity.

#### Key Components:
- **Click Count**: Counts the number of clicks in the same position.
- **Click Limit**: Once the clicks exceed the limit without any movement, a bot is detected.

#### Main Function:
```python
def detect_clicks():
    def on_click(x, y, button, pressed):
        # Detects click and tracks if the position changes
        if pressed:
            current_position = (x, y)
            if current_position == last_position:
                click_count += 1
            else:
                click_count = 1
                last_position = current_position

            if click_count > CLICK_LIMIT:
                print("Bot detected !")
```

#### Detection Logic:
- **Click without Movement**: If more than `CLICK_LIMIT` clicks occur without any movement, the system flags it as suspicious.
  
---

### 3. ⌨️ Keyboard Tracking

**File**: `keyboard_tracking.py`

This module tracks the timing between key presses to detect automated or scripted keyboard inputs. It identifies bot-like typing based on the speed and consistency of the inputs.

#### Key Components:
- **Timing Buffer**: Stores the timestamps of recent keypresses.
- **Speed Threshold**: If keypresses occur faster than a predefined threshold, they are flagged as suspicious.

#### Main Function:
```python
def on_key_event(e):
    if e.event_type == 'down':
        time_diff = current_time - key_press_times[-1]
        
        if time_diff < THRESHOLD:
            curr_count += 1
        
        key_press_times.append(current_time)

        if len(key_press_times) >= BUFFER_SIZE and curr_count >= 90:
            print("Bot detected!")
            flag = 0
```

#### Detection Logic:
- **Typing Speed**: If keys are pressed too quickly and consistently (based on the threshold), it indicates automated behavior.
- **Keypress Buffer**: Only the last 100 keypresses are analyzed, keeping the system efficient.

---

### 4. 🌍 Time Zone Detection

**File**: `timezone_tracking.py`

This module detects changes in the system's time zone. It checks the current system time zone and compares it with the previously detected one to identify changes in real time.

#### Key Components:
- **Time Zone Detection**: Uses the `tzlocal` and `pytz` libraries to detect the system’s time zone.
- **Real-Time Monitoring**: Continuously monitors the system for changes in the time zone.

#### Main Function:
```python
def detect_time_zone_change():
    previous_tz = get_localzone()
    while True:
        current_tz = get_localzone()
        if current_tz != previous_tz:
            print("Time zone change detected!")
            print_time_in_IST(current_tz)
            previous_tz = current_tz
        time.sleep(10)
```

#### Detection Logic:
- **Time Zone Change**: If the current time zone differs from the previous one, it logs the change and prints the current time in IST.

---

## 📸 Screenshot Capture

The screenshot functionality allows you to capture periodic screenshots and provides options to blur the images for privacy.

**Key Features**:
- **Configurable Intervals**: Users can set the interval at which screenshots are taken.
- **Blur Option**: Screenshots can be blurred to protect sensitive information.

---

## How to Run the Application

### Requirements
- Python 3.x
- Libraries: `pynput`, `keyboard`, `ctypes`, `pytz`, `tzlocal`, `pyautogui`, `Pillow`

### Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/activity-tracker-agent.git
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the main script:**
   ```bash
   python main.py
   ```
---
