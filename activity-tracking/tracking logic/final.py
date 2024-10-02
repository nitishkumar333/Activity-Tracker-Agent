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

    keyboard_thread = threading.Thread(target=timezone_tracking.detect_time_zone_change)
    keyboard_thread.start()

    mouse_click_tracking.detect_clicks()

if __name__ == "__main__":
    main()