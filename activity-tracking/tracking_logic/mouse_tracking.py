import time
from pynput import mouse
import numpy as np
import ctypes
import math

# Helper function for finding the longest common subarray
def findLength(nums1, nums2):
    n, m = len(nums1), len(nums2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    ans = 0
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if nums1[i - 1] == nums2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                ans = max(ans, dp[i][j])
    return ans

# Helper function to detect repeated patterns in movement direction
def detect_pattern(arr):
    pattern_len = 250  # Length of sequence to check for repeated patterns
    for i in range(0, len(arr) - 2 * pattern_len, 2):
        if findLength(arr[i:i + pattern_len], arr[i + pattern_len:i + 2 * pattern_len]) > 10:
            return True
    return False

# Main function to analyze mouse data and detect bot/human activity
def detect_bot_or_human(mouse_data):
    max_straight_line_count = 0
    curr_straight_line_count = 0
    repeated_pattern_count = 0
    movement_pattern = []

    # Thresholds for detection
    straight_line_limit = 200  # Max allowed straight line movement count for bot detection
    pattern_limit = 3  # Max allowed repeated pattern occurrences for bot detection
    
    for i in range(1, len(mouse_data)):
        x_diff = mouse_data[i][0] - mouse_data[i - 1][0]  # X movement
        y_diff = mouse_data[i][1] - mouse_data[i - 1][1]  # Y movement

        # Calculate direction (in radians)
        direction = y_diff == 0 or x_diff == 0
        pattern = math.atan2(y_diff, x_diff)
        movement_pattern.append(pattern)

        # Check for straight line movement
        if direction:
            curr_straight_line_count += 1
        else:
            max_straight_line_count = max(curr_straight_line_count, max_straight_line_count)
            curr_straight_line_count = 0

        # Check for repeated movement patterns
        if detect_pattern(movement_pattern):
            repeated_pattern_count += 1
    
    max_straight_line_count = max(curr_straight_line_count, max_straight_line_count) + 1

    # Set detection logic
    is_bot = False
    if max_straight_line_count > straight_line_limit or repeated_pattern_count > pattern_limit:
        is_bot = True

    return is_bot

# Get mouse position using ctypes
class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

def get_mouse_position():
    pt = POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y

# Function to track mouse movements and detect bot/human behavior
def track_mouse_movement(bot_activity_detected):
    print("mouse Motion  detection Go!.....\n")
    mouse_data = []
    start_time = time.time()
    
    while time.time() - start_time < 20:  # Run for 20 seconds
        x, y = get_mouse_position()
        temp = (x, y)
        if not mouse_data or mouse_data[-1] != temp:
            mouse_data.append(temp)

        if len(mouse_data) > 500:
            result = detect_bot_or_human(mouse_data)
            if result:
                bot_activity_detected[0]=True 
            mouse_data.clear()
        
        time.sleep(0.02)
