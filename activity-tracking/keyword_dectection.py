import keyboard
import time

THRESHOLD = 0.2   # Maximum time between keypresses for automated/scripted input
BUFFER_SIZE = 100         # Number of key presses to analyze

# A buffer to store recent key press timings
key_press_times = []
curr_count = 0
flag = 0
def on_key_event(e):
    global curr_count
    global flag
    current_time = time.time()
    
    # Only consider key down events
    if e.event_type == 'down':
        if key_press_times:
            # Calculate the time difference between the last key press and current one
            time_diff = current_time - key_press_times[-1]
            
            if time_diff < THRESHOLD:
                curr_count += 1
        
        # Add current time to the buffer
        key_press_times.append(current_time)
        flag += 1

        # Keep only the last 100 timings
        if len(key_press_times) >= BUFFER_SIZE:
            if curr_count >= 90 and flag >= 100:
                print("Bot detected!")
                flag = 0
            if key_press_times[0] < THRESHOLD:
                curr_count -= 1
            key_press_times.pop(0)

# Hook the key press event
keyboard.hook(on_key_event)
print("Monitoring keyboard input....")