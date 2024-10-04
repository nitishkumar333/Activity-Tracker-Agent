from pynput import keyboard
import time

# Thresholds for detecting automation
THRESHOLD = 0.2   # Maximum time between keypresses for automated/scripted input
BUFFER_SIZE = 100  # Number of key presses to analyze

# A buffer to store recent key press timings
key_press_times = []
curr_count = 0
flag = 0

# Function to handle keyboard events and detect bot-like behavior
def on_key_event(event, bot_activity_detected):
    global curr_count
    global flag
    current_time = time.time()

    # Only consider key down events
    if event:
        if key_press_times:
            # Calculate the time difference between the last key press and current one
            time_diff = current_time - key_press_times[-1]

            if time_diff < THRESHOLD:
                curr_count += 1

        # Add current time to the buffer
        key_press_times.append(current_time)
        flag += 1

        # Keep only the last few timings
        if len(key_press_times) >= BUFFER_SIZE:
            if curr_count >= 90 and flag >= 100:
                bot_activity_detected[0]=True
                flag = 0
            if key_press_times[0] < THRESHOLD:
                curr_count -= 1
            key_press_times.pop(0)

# Function to start monitoring the keyboard
def monitor_keyboard(bot_activity_detected):
    listn = keyboard.Listener(lambda event: on_key_event(event, bot_activity_detected))
    # keyboard.on_press(lambda event: on_key_event(event, bot_activity_detected))
    listn.start()
    listn.join()

if __name__ == "__main__":
    # minimum log level which is what you need to not see kivy's default info logs
    bot_activity = [False]
    monitor_keyboard(bot_activity)
