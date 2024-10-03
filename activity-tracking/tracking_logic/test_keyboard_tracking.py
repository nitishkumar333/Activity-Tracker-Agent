import pytest
import time
from unittest.mock import patch, Mock
from keyboard_tracking import on_key_event, monitor_keyboard, key_press_times

# Mock event for keyboard press
class MockEvent:
    def __init__(self, name, event_type='down'):
        self.name = name
        self.event_type = event_type

def test_normal_behavior():
    bot_activity_detected = [False]
    # Simulate key press with a delay larger than the threshold
    with patch('time.time', side_effect=[1, 1.5, 2.1, 2.6]):
        on_key_event(MockEvent('a'), bot_activity_detected)
        on_key_event(MockEvent('b'), bot_activity_detected)
        on_key_event(MockEvent('c'), bot_activity_detected)
        on_key_event(MockEvent('d'), bot_activity_detected)
    assert not bot_activity_detected[0]
    assert len(key_press_times) == 4

# Test case for bot-like behavior (with rapid key presses below the threshold)
def test_bot_behavior():
    bot_activity_detected = [False]
    # Simulate rapid key presses (less than the threshold of 0.2 seconds)

    with patch('time.time', side_effect=[1.5]*110):
        for x in range(0,110):
            on_key_event(MockEvent('a'), bot_activity_detected)

    assert bot_activity_detected[0]
    assert len(key_press_times) > 90

# Test case to ensure the monitoring function works with esc
def test_monitor_keyboard():
    bot_activity_detected = [False]
    with patch('keyboard.on_press') as mock_on_press, patch('keyboard.wait', side_effect=KeyboardInterrupt):
        try:
            monitor_keyboard(bot_activity_detected)
        except KeyboardInterrupt:
            pass

        mock_on_press.assert_called()  # Ensures on_press was set up
