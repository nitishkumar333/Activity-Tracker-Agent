from pynput import mouse
import math
# from data import mouse_movement_data
# from data_bot import bot_movement_data
# from temp_data import temp_movement_data


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

def detect_pattern(arr):
    pattern_len = 200
    for i in range(0,len(arr) - 2 * pattern_len,2):
        if findLength(arr[i:i + pattern_len],arr[i + pattern_len:i + 2 * pattern_len]) > 10:
            return True
    return False

def detect_bot_or_human(mouse_data):
    max_straight_line_count = 0
    curr_straight_line_count = 0
    repeated_pattern_count = 0
    movement_pattern = []

    straight_line_limit = 200
    pattern_limit = 2
    
    for i in range(1, len(mouse_data)):
        x_diff = mouse_data[i][0] - mouse_data[i-1][0]
        y_diff = mouse_data[i][1] - mouse_data[i-1][1]

        direction = y_diff == 0 or x_diff == 0
        pattern = math.atan2(y_diff, x_diff)
        movement_pattern.append(pattern)

        if direction:
            curr_straight_line_count += 1
        else:
            max_straight_line_count = max(curr_straight_line_count, max_straight_line_count)
            curr_straight_line_count = 0

        if detect_pattern(movement_pattern):
            repeated_pattern_count += 1
    max_straight_line_count = max(curr_straight_line_count, max_straight_line_count) + 1
    print(max_straight_line_count)
    print(repeated_pattern_count)
    is_bot = False
    if max_straight_line_count > straight_line_limit or repeated_pattern_count > pattern_limit:
        is_bot = True

    return is_bot

temp_movement_data = []
result = detect_bot_or_human(temp_movement_data)
print("Is bot:", result)

