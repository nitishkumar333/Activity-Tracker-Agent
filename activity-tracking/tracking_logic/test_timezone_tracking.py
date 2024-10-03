import pytest
import time
from unittest.mock import patch, MagicMock
from datetime import datetime
import pytz

from timezone_tracking import print_time_in_IST  # Import your functions

# Mock time zone for testing
IST = pytz.timezone('Asia/Kolkata')

# Helper function to mock datetime.now
def mock_datetime_now(tz):
    return datetime(2024, 10, 1, 12, 0, 0, tzinfo=tz)

# Test print_time_in_IST function
@patch('timezone_tracking.datetime')  # Mock datetime to control the current time
@patch('timezone_tracking.pytz.timezone')  # Mock timezone conversion
def test_print_time_in_IST(mock_timezone, mock_datetime, capsys):
    # Setup mocks
    mock_datetime.now.return_value = mock_datetime_now(pytz.utc)  # Simulate UTC time
    mock_timezone.return_value = IST

    # Call the function
    print_time_in_IST(pytz.utc)

    # Capture printed output
    captured = capsys.readouterr()
    
    # Check the output contains the expected IST time (converted from UTC)
    assert "Current time in IST" in captured.out
    assert "2024-10-01" in captured.out  # Check the correct date
    assert "17:30:00" in captured.out  # Check if time is correctly converted to IST (UTC+5:30)