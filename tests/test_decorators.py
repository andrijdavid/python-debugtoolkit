import gc
import io
import logging
import time
from unittest import mock

from debugtoolkit import (
    log_garbage_collection,
    log_inputs,
    log_time_execution,
    monitor_detailed_resources,
    monitor_resources,
)


def test_log_inputs():
    """Test the log_inputs decorator."""

    @log_inputs
    def add(a, b):
        return a + b

    with mock.patch.object(logging, "info") as mock_log:
        add(1, 2)
        mock_log.assert_called_once_with("Calling add(1, 2)")


def test_log_time_execution():
    """Test the log_time_execution decorator."""

    @log_time_execution(n=3)
    def add(a, b):
        time.sleep(0.1)  # Add delay to simulate function execution time
        return a + b

    with mock.patch.object(logging, "info") as mock_log:
        add(1, 2)

    assert mock_log.call_count == 4  # 3 for each execution and 1 for average
    for i in range(3):
        assert f"Execution {i + 1} of add:" in mock_log.call_args_list[i][0][0]
    assert "Average execution time of add:" in mock_log.call_args_list[3][0][0]


def test_log_garbage_collection():
    """Test the log_garbage_collection decorator."""

    @log_garbage_collection
    def create_objects():
        a = [0] * 10000  # Create a large object
        del a  # Delete the object
        gc.collect()  # Manually trigger garbage collection
        return None

    with mock.patch.object(logging, "info") as mock_log:
        create_objects()

    # Check if garbage collection counts were logged
    assert any(
        "Garbage collection counts changed for create_objects:" in call[0][0]
        for call in mock_log.call_args_list
    )


def test_monitor_detailed_resources():
    # Define a simple function to be decorated
    @monitor_detailed_resources
    def add(a, b):
        time.sleep(1)  # simulate some workload
        return a + b

    # Set up logger to capture log messages
    logger = logging.getLogger()
    logger.level = logging.DEBUG
    log_stream = io.StringIO()
    stream = logging.StreamHandler(log_stream)
    logger.addHandler(stream)
    logging.getLogger()

    # Call the decorated function
    result = add(1, 2)

    # Check the function result
    assert result == 3

    # Check the log messages
    log_messages = log_stream.getvalue()
    assert "Resource usage for add:" in log_messages
    assert "CPU Usage:" in log_messages
    assert "Execution Time:" in log_messages
    assert "Memory Usage: RSS:" in log_messages
    assert "Disk I/O: Read:" in log_messages
    assert "Network I/O: Sent:" in log_messages
    # We can't assert the exact values as they depend on the system and runtime conditions


def test_monitor_resources():
    # Define a simple function to be decorated
    @monitor_resources
    def add(a, b):
        time.sleep(1)  # simulate some workload
        return a + b

    # Set up logger to capture log messages
    logger = logging.getLogger()
    logger.level = logging.DEBUG
    log_stream = io.StringIO()
    stream = logging.StreamHandler(log_stream)
    logger.addHandler(stream)
    logging.getLogger()

    # Call the decorated function
    result = add(1, 2)

    # Check the function result
    assert result == 3

    # Check the log messages
    log_messages = log_stream.getvalue()
    assert "Resource usage for add:" in log_messages
    assert "CPU:" in log_messages
    assert "Memory:" in log_messages
    # We can't assert the exact values as they depend on the system and runtime conditions
