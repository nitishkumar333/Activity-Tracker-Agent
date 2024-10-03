import pytest
from unittest.mock import patch
import math
from mouse_tracking import detect_bot_or_human, detect_pattern, findLength, POINT, get_mouse_position, track_mouse_movement

# Sample mock data for testing
human_mouse_data = [
    (100, 100), (102, 104), (105, 107), (109, 110), (112, 115),
    (115, 120), (120, 125), (125, 130), (130, 135), (135, 140)
]

bot_mouse_data_straight_line = [(100, 100)] + [(100 + i, 100) for i in range(1, 501)]

# Test for findLength (helper function)
def test_findLength():
    nums1 = [1, 2, 3, 4]
    nums2 = [3, 4, 5, 6]
    assert findLength(nums1, nums2) == 2  # Longest common subarray is [3, 4]

# Test for detect_pattern (helper function)
def test_detect_pattern():
    arr = [math.atan2(1, 1)] * 200 + [math.atan2(1, 2)] * 200  # No repetition
    assert detect_pattern(arr) == False

# Test detect_bot_or_human function
def test_detect_bot_or_human():
    # Human-like behavior
    assert detect_bot_or_human(human_mouse_data) == False

    # Straight-line movement bot-like behavior
    assert detect_bot_or_human(bot_mouse_data_straight_line) == True


if __name__ == '__main__':
    pytest.main()
