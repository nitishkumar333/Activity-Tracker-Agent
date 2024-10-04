import threading
import psutil
import time
from tracking_logic import mouse_tracking, mouse_click_tracking, keyboard_tracking, timezone_tracking

def Final_Tracker(bot_activity_detected, stop,Time_pop):
   
    # Start thread for tracking mouse movement
    movement_thread = threading.Thread(target=mouse_tracking.track_mouse_movement, args=(bot_activity_detected,), daemon=True)
    movement_thread.start()

    # Start thread for monitoring keyboard (will not be paused)
    keyboard_thread = threading.Thread(target=keyboard_tracking.monitor_keyboard, args=(bot_activity_detected,), daemon=True)
    keyboard_thread.start()

    # Start thread for detecting time zone changes (will not be paused)
    timezone_thread = threading.Thread(target=timezone_tracking.detect_time_zone_change, args=(stop,Time_pop), daemon=True)
    timezone_thread.start()

    # Detect mouse clicks in its own thread
    click_thread = threading.Thread(target=mouse_click_tracking.detect_clicks, args=(bot_activity_detected,), daemon=True)
    click_thread.start()

    while not stop[0]:  # Run until stop event is set
        continue
  

    movement_thread=None
    keyboard_thread=None
    timezone_thread=None
    click_thread=None
