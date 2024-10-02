import time
from tzlocal import get_localzone

def detect_time_zone_change():
    previous_tz = get_localzone()
    print(previous_tz)
    while True:
        current_tz = get_localzone()
        print(current_tz)
        if current_tz != previous_tz:
            print("\nTime zone change detected!")

        time.sleep(10)

if __name__ == "__main__":
    print("Listening for time zone changes...")
    detect_time_zone_change()
