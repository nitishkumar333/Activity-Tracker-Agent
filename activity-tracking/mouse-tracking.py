import math
import time
from pynput import mouse
# from data import mouse_movement_data
# from data_bot import bot_movement_data
# from temp_data import temp_movement_data

# Longest common subarray algorithm to detect patterns
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
    pattern_len = 200  # Length of sequence to check for repeated patterns
    for i in range(0,len(arr) - 2 * pattern_len,2):
        if findLength(arr[i:i + pattern_len],arr[i + pattern_len:i + 2 * pattern_len]) > 10:
            return True
    return False

def detect_bot_or_human(mouse_data):
    max_straight_line_count = 0
    curr_straight_line_count = 0
    repeated_pattern_count = 0
    movement_pattern = []

    # limits for detection
    straight_line_limit = 200  # Max allowed straight line movement count for bot detection
    pattern_limit = 2  # Max allowed repeated pattern occurrences for bot detection
    
    for i in range(1, len(mouse_data)):
        x_diff = mouse_data[i][0] - mouse_data[i-1][0]     # X movement
        y_diff = mouse_data[i][1] - mouse_data[i-1][1]     # Y movement

        direction = y_diff == 0 or x_diff == 0
        # Calculate angle movement (in radians)
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
    print(max_straight_line_count)
    print(repeated_pattern_count)

    # Set detection logic
    is_bot = False
    if max_straight_line_count > straight_line_limit or repeated_pattern_count > pattern_limit:
        is_bot = True

    return is_bot

mouse_movements = []

def on_move(x, y):
    mouse_movements.append((x, y))
    if len(mouse_movements) >= 500:
        result = detect_bot_or_human(mouse_movements)
        print("Is bot:", result)
        mouse_movements.clear()

listener = mouse.Listener(on_move = on_move)
listener.start()
print("Listening started....")
time.sleep(20)
listener.stop()

