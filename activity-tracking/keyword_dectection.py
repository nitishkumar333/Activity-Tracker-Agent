import keyboard
import time

THRESHOLD = 0.2
BUFFER_SIZE = 100

key_press_times = []
curr_count = 0
flag = 0
def on_key_event(e):
    global curr_count
    global flag
    current_time = time.time()
    
    if e.event_type == 'down':
        if key_press_times:
            time_diff = current_time - key_press_times[-1]
            
            if time_diff < THRESHOLD:
                curr_count += 1
        
        key_press_times.append(current_time)
        flag += 1

        if len(key_press_times) >= BUFFER_SIZE:
            if curr_count >= 90 and flag >= 100:
                print("Bot detected!")
                flag = 0
            if key_press_times[0] < THRESHOLD:
                curr_count -= 1
            key_press_times.pop(0)

keyboard.hook(on_key_event)
print("Monitoring keyboard input....")
keyboard.wait('esc')