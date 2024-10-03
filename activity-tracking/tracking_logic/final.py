import threading
from tracking_logic import mouse_tracking
from tracking_logic import mouse_click_tracking
from tracking_logic import keyboard_tracking
from tracking_logic import timezone_tracking

def Final_Tracker(bot_activity_detected, stop, percentage, is_plugged):

    # Start thread for tracking mouse movement
    movement_thread = threading.Thread(target=mouse_tracking.track_mouse_movement, args=(bot_activity_detected,))
    movement_thread.start()

    # Start thread for monitoring keyboard
    keyboard_thread = threading.Thread(target=keyboard_tracking.monitor_keyboard, args=(bot_activity_detected,))
    keyboard_thread.start()

    # Start thread for detecting time zone changes
    timezone_thread = threading.Thread(target=timezone_tracking.detect_time_zone_change, args=(stop,))
    timezone_thread.start()

    # Detect mouse clicks in its own thread
    click_thread = threading.Thread(target=mouse_click_tracking.detect_clicks, args=(bot_activity_detected,))
    click_thread.start()

    