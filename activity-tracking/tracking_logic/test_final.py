import threading
import pytest
from unittest.mock import patch

# Import the Final_Tracker function from the module
from final import Final_Tracker

@patch('mouse_tracking.track_mouse_movement')
@patch('mouse_click_tracking.detect_clicks')
@patch('keyboard_tracking.monitor_keyboard')
@patch('timezone_tracking.detect_time_zone_change')
def test_final_tracker(mock_detect_time_zone_change, mock_monitor_keyboard, mock_detect_clicks, mock_track_mouse_movement):
    # Define mock arguments to pass to the threads
    bot_activity_detected = threading.Event()
    stop = threading.Event()
    percentage = 50
    is_plugged = False

    # Call the Final_Tracker function
    Final_Tracker(bot_activity_detected, stop, percentage, is_plugged)

    # Assert that each of the tracking functions was called correctly
    mock_track_mouse_movement.assert_called_once_with(bot_activity_detected)
    mock_monitor_keyboard.assert_called_once_with(bot_activity_detected)
    mock_detect_time_zone_change.assert_called_once_with(stop)
    mock_detect_clicks.assert_called_once_with(bot_activity_detected)

    # Optionally, check if threads were created (to ensure threading is invoked)
    assert threading.active_count() >= 1  # Ensures that threads are running

# Run the tests using pytest in the command line
# pytest -v
