import pytest
from unittest.mock import patch, call
from pynput.mouse import Button

# Import the function to be tested
from mouse_click_tracking import detect_clicks  # Replace 'your_module' with the actual module name

@pytest.fixture
def bot_activity_detected():
    # Fixture to initialize bot_activity_detected list
    return [False]

def test_click_detection_without_movement(bot_activity_detected):
    # Simulate multiple clicks without movement
    with patch('pynput.mouse.Listener') as mock_listener:
        detect_clicks(bot_activity_detected)  # Run the function
        
        # Simulate 11 clicks at the same position without movement
        on_click = mock_listener.call_args[1]['on_click']
        for _ in range(11):
            on_click(100, 200, Button.left, True)  # Click at position (100, 200)
        
        # Verify that bot activity is detected
        assert bot_activity_detected[0] is True

def test_click_detection_with_movement(bot_activity_detected):
    # Simulate clicks with movement in between
    with patch('pynput.mouse.Listener') as mock_listener:
        detect_clicks(bot_activity_detected)  # Run the function
        
        on_click = mock_listener.call_args[1]['on_click']
        on_move = mock_listener.call_args[1]['on_move']
        
        # Simulate click, move, click, move, etc.
        on_click(100, 200, Button.left, True)  # Click at position (100, 200)
        on_move(120, 220)  # Move the mouse
        on_click(120, 220, Button.left, True)  # Click at new position
        
        # Simulate movement and reset
        assert bot_activity_detected[0] is False  # No bot activity should be detected

def test_click_detection_reset_on_movement(bot_activity_detected):
    # Simulate clicks with a reset due to movement
    with patch('pynput.mouse.Listener') as mock_listener:
        detect_clicks(bot_activity_detected)  # Run the function
        
        on_click = mock_listener.call_args[1]['on_click']
        on_move = mock_listener.call_args[1]['on_move']
        
        # Simulate 5 clicks at the same position
        for _ in range(5):
            on_click(100, 200, Button.left, True)  # Click at position (100, 200)
        
        # Simulate mouse movement (this should reset the click count)
        on_move(150, 250)
        
        # Simulate 6 more clicks at the new position
        for _ in range(6):
            on_click(150, 250, Button.left, True)
        
        # Verify that bot activity is still not detected due to movement
        assert bot_activity_detected[0] is False

def test_click_detection_exactly_at_limit(bot_activity_detected):
    # Simulate exactly 10 clicks at the same position (at the limit)
    with patch('pynput.mouse.Listener') as mock_listener:
        detect_clicks(bot_activity_detected)  # Run the function
        
        on_click = mock_listener.call_args[1]['on_click']
        
        # Simulate exactly 10 clicks at the same position (not over the limit)
        for _ in range(10):
            on_click(100, 200, Button.left, True)  # Click at position (100, 200)
        
        # Verify that bot activity is not yet detected (since limit is 10)
        assert bot_activity_detected[0] is False
