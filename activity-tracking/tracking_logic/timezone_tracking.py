import time
import pytz
from datetime import datetime
from tzlocal import get_localzone, reload_localzone

def print_time_in_IST(local_tz):
    # Get the current time in the local time zone
    local_time = datetime.now(local_tz)

    # Define IST time zone
    IST = pytz.timezone('Asia/Kolkata')

    # Convert the local time to IST
    ist_time = local_time.astimezone(IST)
    print("Current time in IST:", ist_time.strftime('%Y-%m-%d %H:%M:%S'))

def detect_time_zone_change(stop):
    # Get the initial system time zone
    previous_tz = get_localzone()  # Convert to string for easier comparison
    while not stop[0]:
        reload_localzone()
        # Get the current system time zone afresh
        current_tz = get_localzone()  # Convert to string for easier comparison
        # Check if the time zone has changed
        if current_tz != previous_tz:
            print("\nTime zone change detected!")
            print_time_in_IST(current_tz)

            # Update the previous time zone to the current one
            previous_tz = current_tz

        # Sleep for a while before checking again (e.g., 10 seconds)
        time.sleep(10)
