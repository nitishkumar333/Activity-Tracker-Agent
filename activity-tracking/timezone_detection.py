import time
import pytz
from datetime import datetime
from tzlocal import get_localzone, reload_localzone

def print_time_in_IST(local_tz):
    local_time = datetime.now(local_tz)
    IST = pytz.timezone('Asia/Kolkata')
    ist_time = local_time.astimezone(IST)
    print("Current time in IST:", ist_time.strftime('%Y-%m-%d %H:%M:%S'))

def detect_time_zone_change():
    previous_tz = get_localzone()
    print(previous_tz)
    while True:
        reload_localzone()
        current_tz = get_localzone()
        print(current_tz)
        if current_tz != previous_tz:
            print("\nTime zone change detected!")
            print_time_in_IST(current_tz)
            previous_tz = current_tz

        time.sleep(10)

if __name__ == "__main__":
    print("Listening for time zone changes...")
    detect_time_zone_change()
