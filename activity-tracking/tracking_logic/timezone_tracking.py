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

def detect_time_zone_change(stop, time_pop):
    while not stop[0]:
        previous_tz = get_localzone()
        try:
            reload_localzone()  # Reload timezone information
        except Exception as e:
            print(f"Error reloading timezone: {e}")

        # Get the current system time zone afresh
        current_tz = get_localzone()  # Get the updated timezone object

        # Check if the time zone has changed
        if current_tz != previous_tz:
            print("TimeZone Change detected")
            time_pop[0] = True  # Update the flag
            print_time_in_IST(current_tz)

            # Update the previous time zone to the current one
            previous_tz = current_tz

        # Sleep for a while before checking again (e.g., 10 seconds)
        time.sleep(10)
